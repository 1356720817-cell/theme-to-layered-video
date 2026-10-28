import argparse,hashlib,json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--previous',required=True);args=parser.parse_args();previous=Path(args.previous).resolve()
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
shots=load(root/'public/shots.json');old=load(previous/'public/shots.json');project=load(root/'public/project.json');old_project=load(previous/'public/project.json')
main=[s for s in shots if s['section']=='main'];assert len(main)==24
records=load(root/'public/poems.json')['poems'];assert len(records)==24
old_by_id={s['id']:s for s in old}
for s in shots:
 before=old_by_id[s['id']]
 assert all(s[k]==before[k] for k in ['start','end','layers','camera','transition','title','subtitle']),s['id']
 if s['section']=='main':
  p=s['poem'];assert p['lines'] and p['author'] and p['work'] and p['sourceUrl']
  assert p['cueFrame']<s['end']-s['start']
  assert max(len(line) for line in p['lines'])<=7
  if s['end']-s['start']<=90:assert len(p['lines'])==1
  assert p['lines']==records[s['index']-1]['excerpt'].rstrip('��').split('��')
assert len({'|'.join(s['poem']['lines']) for s in main})==24
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audio=digest(root/'public'/project['audio']['file']);previous_audio=digest(previous/'public'/old_project['audio']['file']);assert audio==previous_audio
def packet_hash(video):
 return subprocess.run(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],check=True,capture_output=True,text=True).stdout.strip()
assert packet_hash(root/'outputs/final.mp4')==packet_hash(previous/'outputs/final.mp4')
report={'main_terms_with_poetry':24,'independent_poem_entries':24,'single_line_short_shots':sum(len(s['poem']['lines'])==1 for s in main),'unchanged_scene_times_layers_cameras_transitions_and_original_text':True,'unchanged_approved_audio_file_sha256':audio,'final_audio_packets_match_v4':True,'poetry_source_index':'poetry-sources.md','source_review_note':'Verse text and attribution were reviewed against the recorded sources; this script checks coverage, timing and consistency, not literary authorship.','visual_layout_review_required':True,'human_full_listening_review':False}
(root/'work/poetry-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True,indent=2))
