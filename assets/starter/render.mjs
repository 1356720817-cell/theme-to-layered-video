import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia} from '@remotion/renderer';
import {spawnSync} from 'node:child_process';
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
const draft=process.argv.includes('--draft');const at=process.argv.indexOf('--output');
const output=path.resolve(at>=0?process.argv[at+1]:'outputs/master-silent.mp4');
const audit=spawnSync(process.env.PYTHON_BIN||'python',['-I','scripts/audit_project.py','.',...(draft?['--allow-draft']:[])],{stdio:'inherit'});
if(audit.error)throw audit.error;if(audit.status!==0)process.exit(audit.status||1);
function fingerprint(){const r=spawnSync(process.env.PYTHON_BIN||'python',['-I','scripts/production_gate.py','fingerprint','.'],{encoding:'utf8'});if(r.error)throw r.error;if(r.status!==0)throw Error(r.stdout||r.stderr);return JSON.parse(r.stdout).production_fingerprint;}
if(!draft){const g=spawnSync(process.env.PYTHON_BIN||'python',['-I','scripts/production_gate.py','check','.', '--stage','render'],{stdio:'inherit'});if(g.error)throw g.error;if(g.status!==0)process.exit(g.status||1);}
const productionFingerprint=fingerprint();
if(!draft){const lint=process.platform==='win32'?spawnSync(process.env.ComSpec||'cmd.exe',['/d','/s','/c','npm run lint'],{encoding:'utf8'}):spawnSync('npm',['run','lint'],{encoding:'utf8'});if(lint.stdout)process.stdout.write(lint.stdout);if(lint.stderr)process.stderr.write(lint.stderr);if(lint.error)throw lint.error;if(lint.status!==0)process.exit(lint.status||1);await fs.mkdir('work',{recursive:true});await fs.writeFile('work/lint-report.json',JSON.stringify({passed:true,production_fingerprint:productionFingerprint,command:'npm run lint',output:lint.stdout},null,2));}
await fs.mkdir(path.dirname(output),{recursive:true});await fs.mkdir('work',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),rspack:true,outDir:path.resolve('work/render-bundle')});
const browser=await openBrowser('chrome',{browserExecutable:process.env.BROWSER_EXECUTABLE||undefined,chromiumOptions:process.platform==='win32'?{gl:'angle'}:{},logLevel:'error'});
try{const composition=await selectComposition({serveUrl,id:'ThemeVideo',puppeteerInstance:browser});let last=-1;
 const result=await renderMedia({composition,serveUrl,codec:'h264',muted:true,outputLocation:output,crf:18,x264Preset:'medium',pixelFormat:'yuv420p',imageFormat:'jpeg',jpegQuality:92,concurrency:4,puppeteerInstance:browser,overwrite:true,logLevel:'error',onProgress:p=>{const step=Math.floor(p.renderedFrames/100);if(step!==last){last=step;process.stdout.write(`${p.renderedFrames}/${composition.durationInFrames}\n`);}}});
 if(fingerprint()!==productionFingerprint)throw Error('Production inputs changed while rendering. Render again.');
 const outputSha256=createHash('sha256').update(await fs.readFile(output)).digest('hex');
 await fs.writeFile('work/render-report.json',JSON.stringify({output,draft,production_fingerprint:productionFingerprint,output_sha256:outputSha256,width:composition.width,height:composition.height,fps:composition.fps,frames:composition.durationInFrames,slowestFrames:result.slowestFrames},null,2));
}finally{await browser.close({silent:true});}
