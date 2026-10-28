import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const p=JSON.parse(fs.readFileSync('public/project.json','utf8')),audio=p.audio??{};
const digest=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
function fingerprint(){const r=spawnSync(process.env.PYTHON_BIN||'python',['-I','scripts/production_gate.py','fingerprint','.'],{encoding:'utf8'});if(r.error)throw r.error;if(r.status!==0)throw Error(r.stdout||r.stderr);return JSON.parse(r.stdout).production_fingerprint;}
fs.mkdirSync('outputs',{recursive:true});fs.mkdirSync('work',{recursive:true});
const render=JSON.parse(fs.readFileSync('work/render-report.json','utf8'));
const input=render.output,fp=fingerprint();
if(render.production_fingerprint!==fp||render.output_sha256!==digest(input))throw Error('Render inputs/file changed. Render again before mux.');
if(!audio.file){if(audio.required!==false)throw Error('Project audio is missing.');fs.copyFileSync(input,'outputs/final.mp4');}
else{
 // A needless input -ss 0 drops negative-PTS AAC priming packets; preserve a baked master at zero offset.
 const seek=(audio.offsetSeconds??0)>0?['-ss',String(audio.offsetSeconds)]:[];
 const args=['-v','error','-y','-i',input,...seek,'-i',path.resolve('public',audio.file),'-map','0:v:0','-map','1:a:0','-c:v','copy',...(audio.copy?['-c:a','copy']:['-c:a','aac','-b:a','192k']),...(!audio.copy&&audio.allowPad?['-af','apad']:[]),'-t',String(p.durationFrames/p.fps),'-movflags','+faststart','outputs/final.mp4'];
 const result=spawnSync(process.env.FFMPEG_BIN||'ffmpeg',args,{stdio:'inherit'});if(result.error)throw result.error;if(result.status!==0)process.exit(result.status||1);
}
if(fingerprint()!==fp)throw Error('Inputs changed while muxing.');
fs.writeFileSync('work/audio-mux.json',JSON.stringify({file:audio.file,copy:!!audio.copy,offsetSeconds:audio.offsetSeconds??0,durationSeconds:p.durationFrames/p.fps,production_fingerprint:fp,render_sha256:render.output_sha256,final_sha256:digest('outputs/final.mp4')},null,2));
