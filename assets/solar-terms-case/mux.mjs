import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const p=JSON.parse(fs.readFileSync('public/project.json','utf8'));const audio=p.audio??{};
fs.mkdirSync('outputs',{recursive:true});fs.mkdirSync('work',{recursive:true});
if(!audio.file){if(audio.required!==false)throw Error('Project audio is missing.');fs.copyFileSync('outputs/master-silent.mp4','outputs/final.mp4');process.exit(0);}
const offsetArgs=Number(audio.offsetSeconds??0)!==0?['-ss',String(audio.offsetSeconds)]:[];
const args=['-v','error','-y','-i','outputs/master-silent.mp4',...offsetArgs,'-i',path.resolve('public',audio.file),'-map','0:v:0','-map','1:a:0','-c:v','copy',...(audio.copy?['-c:a','copy']:['-c:a','aac','-b:a','192k']),'-af',...(audio.copy?[]:['apad']),'-t',String(p.durationFrames/p.fps),'-movflags','+faststart','outputs/final.mp4'];
// Audio filtering is incompatible with stream copy.
if(audio.copy)args.splice(args.indexOf('-af'),1);
const result=spawnSync(process.env.FFMPEG_BIN||'ffmpeg',args,{stdio:'inherit'});if(result.error)throw result.error;if(result.status!==0)process.exit(result.status||1);
fs.writeFileSync('work/audio-mux.json',JSON.stringify({file:audio.file,copy:!!audio.copy,offsetSeconds:audio.offsetSeconds??0,durationSeconds:p.durationFrames/p.fps},null,2));
