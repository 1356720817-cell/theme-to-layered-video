import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia} from '@remotion/renderer';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const go=(args)=>{const r=spawnSync('ffmpeg',['-v','error','-y',...args],{stdio:'inherit'});if(r.status!==0)throw Error('FFmpeg failed');};
const original='work/master-before-prefix-fix.mp4';
if(fs.existsSync(original))throw Error('Prefix repair already started; preserve the previous work.');
fs.copyFileSync('outputs/master-silent.mp4',original);
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),rspack:true,outDir:path.resolve('work/prefix-fix-bundle')});
const browser=await openBrowser('chrome',{chromiumOptions:process.platform==='win32'?{gl:'angle'}:{},logLevel:'error'});
try{
 const composition=await selectComposition({serveUrl,id:'ThemeVideo',puppeteerInstance:browser});
 await renderMedia({composition,serveUrl,codec:'h264',muted:true,outputLocation:path.resolve('work/prefix-fixed.mp4'),frameRange:[0,249],crf:18,x264Preset:'medium',pixelFormat:'yuv420p',imageFormat:'jpeg',jpegQuality:92,concurrency:4,puppeteerInstance:browser,overwrite:true,logLevel:'error'});
}finally{await browser.close({silent:true});}
// The retained tail starts at an observed IDR frame (250 / 30 seconds).
go(['-ss',String(250/30),'-i',original,'-map','0:v:0','-c:v','copy','work/unchanged-tail.mp4']);
fs.writeFileSync('work/prefix-concat.txt',"file 'prefix-fixed.mp4'\nfile 'unchanged-tail.mp4'\n");
go(['-f','concat','-safe','0','-i','work/prefix-concat.txt','-map','0:v:0','-c:v','copy','-movflags','+faststart','outputs/master-silent.mp4']);
fs.writeFileSync('work/prefix-fix-report.json',JSON.stringify({reason:'Hide opening title during its image-only dissolve tail.',renderedFrames:[0,249],retainedOriginalFrames:[250,3599],tailStartsAtObservedIDR:true,tailVideoStreamCopied:true,needsFullDecodeAndFrameCountVerification:true},null,2));
console.log('Opening title tail repaired; unchanged tail copied at IDR boundary.');
