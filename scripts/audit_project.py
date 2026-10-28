import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path

MOVES={'still','push','pull-back','track-left','track-right','tilt-up','tilt-down','reveal-hold','diagonal'}
CUTS={'cut','dissolve','wipe-left','wipe-right','rise','focus','match-in'}
def audit(root,allow_draft=False):
 root=Path(root).resolve();public=root/'public';errors=[];warnings=[]
 try:
  project=json.loads((public/'project.json').read_text(encoding='utf-8'));shots=json.loads((public/'shots.json').read_text(encoding='utf-8'));assets=json.loads((public/'assets.json').read_text(encoding='utf-8'))['assets']
 except (OSError,KeyError,ValueError) as e:return {'passed':False,'errors':[str(e)],'warnings':[]}
 if project.get('status')!='ready' and not allow_draft:errors.append('Project is draft; final rendering requires status=ready.')
 duration=project.get('durationFrames');fps=project.get('fps')
 if not isinstance(duration,int) or duration<=0:errors.append('durationFrames must be a positive integer.')
 if not isinstance(fps,(int,float)) or fps<=0:errors.append('fps must be positive.')
 if not shots:errors.append('No shots.')
 records={};files={}
 for asset in assets:
  aid=asset.get('id')
  if not aid or aid in records:errors.append('Missing or duplicated asset id: '+str(aid));continue
  records[aid]=asset
  if asset.get('kind','image')!='image':errors.append('Starter supports image layers; implement the requested media renderer before export: '+aid)
  path=(public/asset.get('file','')).resolve()
  if not path.is_relative_to(public.resolve()):errors.append('Asset escapes public directory: '+aid);continue
  if not path.is_file():errors.append('Asset file missing: '+aid);continue
  files[aid]=hashlib.sha256(path.read_bytes()).hexdigest()
  if asset.get('alpha'):
   try:
    from PIL import Image
    with Image.open(path) as image:
     alpha=image.convert('RGBA').getchannel('A')
     low,high=alpha.getextrema()
     if low==255 or high==0:errors.append('Declared transparent asset lacks usable actual alpha: '+aid)
   except ImportError:errors.append('Pillow is required to verify declared alpha, not just its metadata: '+aid)
   except (OSError,ValueError):errors.append('Cannot decode declared transparent asset: '+aid)
  if asset.get('status')!='ready' and not allow_draft:errors.append('Asset not ready: '+aid)
  if not asset.get('rights'):warnings.append('Record asset rights/source status: '+aid)
  if asset.get('depiction')=='generated' and not asset.get('prompt'):warnings.append('Generated asset prompt missing: '+aid)
 expected=0;ids=set();seen={};used=set();push_run=0
 for i,shot in enumerate(shots):
  sid=shot.get('id');start=shot.get('start');end=shot.get('end')
  if not sid or sid in ids:errors.append('Missing or duplicated shot id: '+str(sid))
  ids.add(sid)
  if not isinstance(start,int) or not isinstance(end,int) or end<=start:errors.append('Invalid frame range: '+str(sid));continue
  if start!=expected:errors.append(f'Timeline gap/overlap before {sid}: expected {expected}, got {start}.')
  expected=end
  cam=shot.get('camera',{}).get('type','still');cut=shot.get('transition',{});frames=cut.get('frames',0)
  if cam not in MOVES:errors.append('Unknown camera move: '+str(cam))
  if cut.get('type','cut') not in CUTS:errors.append('Unknown transition: '+str(cut))
  if not isinstance(frames,int) or frames<0 or frames>end-start:errors.append('Invalid transition length: '+str(sid))
  if i==0 and frames:errors.append('The first shot cannot require a previous shot for transition coverage.')
  push_run=push_run+1 if cam=='push' else 0
  if push_run==3:warnings.append('Three consecutive push-ins; review camera fatigue at '+str(sid))
  layers=shot.get('layers',[])
  if not layers and not allow_draft:errors.append('No implemented visual layers: '+str(sid))
  in_shot=set()
  for layer in layers:
   aid=layer.get('assetId');used.add(aid)
   if aid not in records:errors.append('Unknown asset '+str(aid)+' in '+str(sid));continue
   if aid not in files:continue
   h=files[aid]
   repeat_allowed=shot.get('section') in ['recap','ending']
   if aid not in in_shot:
    if h in seen and seen[h]!=sid and not repeat_allowed:errors.append(f'Repeated image content in {sid}; first owned by {seen[h]} ({aid}).')
    if not repeat_allowed and records[aid].get('ownerShot')!=sid:errors.append('Asset ownerShot mismatch: '+aid+' -> '+str(sid))
    if h not in seen:seen[h]=sid
   in_shot.add(aid)
   if layer.get('role')=='foreground' and not records[aid].get('alpha'):warnings.append('Foreground transparency needs visual review: '+aid)
  for word in shot.get('words',[]):
   if not isinstance(word.get('frame'),int) or not 0<=word['frame']<end-start:errors.append('Word cue outside shot: '+str(sid))
  for cue in shot.get('accentFrames',[]):
   if not isinstance(cue,int) or not 0<=cue<end-start:errors.append('Accent cue outside shot: '+str(sid))
  poem=shot.get('poem')
  if poem:
   if not poem.get('lines') or not all(isinstance(line,str) and line.strip() for line in poem['lines']) or not all(poem.get(k) for k in ['author','work','sourceUrl']):errors.append('Incomplete quote text/attribution/source: '+str(sid))
   cue=poem.get('cueFrame');stagger=poem.get('lineStaggerFrames',0);source_cue=poem.get('attributionCueFrame')
   if not all(isinstance(v,int) and v>=0 for v in [cue,stagger,source_cue]) or (isinstance(cue,int) and isinstance(stagger,int) and cue+max(0,len(poem.get('lines',[]))-1)*stagger>=end-start) or (isinstance(source_cue,int) and source_cue>=end-start):errors.append('Quote cue outside readable shot duration: '+str(sid))
 if expected!=duration:errors.append(f'Timeline ends at {expected}, expected {duration}.')
 audio=project.get('audio',{})
 if audio.get('required',True) and not audio.get('file') and not allow_draft:errors.append('Audio is required but missing.')
 if audio.get('file'):
  ap=(public/audio['file']).resolve()
  if not ap.is_relative_to(public.resolve()) or not ap.is_file():errors.append('Audio file missing or outside public.')
  if not audio.get('source') or not audio.get('rights'):warnings.append('Audio source/rights record is incomplete.')
  if ap.is_file() and fps and duration:
   try:
    probe=subprocess.run([os.environ.get('FFPROBE_BIN','ffprobe'),'-v','error','-show_format','-of','json',str(ap)],check=True,capture_output=True,text=True)
    available=float(json.loads(probe.stdout)['format']['duration'])-float(audio.get('offsetSeconds',0))
    if available+.1<duration/fps:
     if audio.get('allowPad'):warnings.append('Audio is intentionally padded; review the silent tail.')
     else:errors.append('Audio is shorter than the film; adjust timing or explicitly authorize padding.')
   except (OSError,ValueError,KeyError,subprocess.CalledProcessError):errors.append('Cannot verify the actual audio duration with ffprobe.')
 return {'passed':not errors,'topic':project.get('topic'),'shot_count':len(shots),'asset_count':len(assets),'used_asset_count':len(used),'timeline_frames':duration,'unique_image_hashes':len(seen),'errors':errors,'warnings':warnings,'scope':'Schema, continuity and byte-identical image reuse; composition, factual accuracy, near-duplicate visuals and listening require review.'}
def main():
 p=argparse.ArgumentParser();p.add_argument('project');p.add_argument('--allow-draft',action='store_true');a=p.parse_args()
 result=audit(a.project,a.allow_draft);output=Path(a.project)/'work';output.mkdir(exist_ok=True);(output/'project-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=True,indent=2));sys.exit(0 if result['passed'] else 1)
if __name__=='__main__':main()
