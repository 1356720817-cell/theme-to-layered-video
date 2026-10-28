import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill} from '@remotion/renderer';
import fs from 'node:fs/promises';
import path from 'node:path';
const shots=JSON.parse(await fs.readFile('public/shots.json','utf8'));
const frames=process.argv.slice(2).map(Number);const targets=frames.length?frames:shots.map(s=>Math.floor((s.start+s.end)/2));
await fs.mkdir('work/preview-stills',{recursive:true});
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts'),rspack:true,outDir:path.resolve('work/preview-bundle')});
const browser=await openBrowser('chrome',{browserExecutable:process.env.BROWSER_EXECUTABLE||undefined,chromiumOptions:process.platform==='win32'?{gl:'angle'}:{},logLevel:'error'});
try{const composition=await selectComposition({serveUrl,id:'ThemeVideo',puppeteerInstance:browser});let i=0;
 async function worker(){while(i<targets.length){const frame=targets[i++];await renderStill({serveUrl,composition,puppeteerInstance:browser,frame,output:path.resolve(`work/preview-stills/frame-${String(frame).padStart(5,'0')}.jpg`),imageFormat:'jpeg',jpegQuality:92,scale:.5,logLevel:'error'});process.stdout.write(`checked ${frame}\n`);}}
 await Promise.all([worker(),worker()]);
}finally{await browser.close({silent:true});}
