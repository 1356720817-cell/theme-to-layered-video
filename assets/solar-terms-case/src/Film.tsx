import React from 'react';
import {AbsoluteFill,Audio,Img,Sequence,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import projectJson from '../public/project.json';
import shotsJson from '../public/shots.json';
import assetsJson from '../public/assets.json';

type Motion={x0?:number;x1?:number;y0?:number;y1?:number;scale0?:number;scale1?:number;sway?:number};
type Layer={assetId:string;role:string;x:number;y:number;w:number;h:number;fit?:'cover'|'contain';parallax?:number;opacity?:number;motion?:Motion};
type Poem={lines:string[];author:string;work:string;sourceUrl:string;cueFrame:number;lineStaggerFrames:number;attributionCueFrame:number;placement:string;top?:number};
type Shot={id:string;index?:number;start:number;end:number;section:string;chapter:string;title:string;subtitle:string;kicker:string;theme:string;layout?:string;visual?:string;weather?:string;camera:{type:string;amount?:number};transition:{type:string;frames:number};layers:Layer[];accentFrames?:number[];accentStrength?:number;labelCueFrames?:{kicker:number;title:number;subtitle:number};poem?:Poem};
type Asset={id:string;file:string;alpha?:boolean};
export const project=projectJson;
export const shots=shotsJson as Shot[];
const assets=new Map((assetsJson.assets as Asset[]).map(a=>[a.id,a]));
const clamp=(n:number,a=0,b=1)=>Math.max(a,Math.min(b,n));
const mix=(a:number,b:number,p:number)=>a+(b-a)*p;
const hash=(n:number)=>{const v=Math.sin(n*12.9898)*43758.5453;return v-Math.floor(v)};
const colors=['#b8cfa5','#dfc277','#d69c70','#b7c7d9'];
const seasonIndex=(index=1)=>Math.min(3,Math.floor((index-1)/6));
const mainShots=shots.filter(s=>s.section==='main');
const mainStart=mainShots[0].start,mainEnd=mainShots[mainShots.length-1].end;
const beatAccent=(shot:Shot,frame:number)=>(shot.accentFrames??[]).reduce((v,cue)=>{const t=frame-cue;return v+(t>=0&&t<22?Math.sin(t*Math.PI/11)*Math.exp(-t/9):0)},0);

export function cameraPose(camera:Shot['camera'],progress:number,width:number,height:number){
 const p=clamp(progress),q=.22*p*p*(3-2*p)+.78*p,amount=camera.amount??1;
 let x=0,y=0,scale=1.025;
 switch(camera.type){
  case 'push':scale=mix(1.025,1.14,q);break;
  case 'pull-back':scale=mix(1.18,1.025,q);break;
  case 'track-left':scale=1.16;x=mix(.05,-.05,q)*width*amount;break;
  case 'track-right':scale=1.16;x=mix(-.05,.05,q)*width*amount;break;
  case 'tilt-up':scale=1.14;y=mix(.05,-.05,q)*height*amount;break;
  case 'tilt-down':scale=1.14;y=mix(-.05,.05,q)*height*amount;break;
  case 'reveal-hold':scale=1.11;x=mix(.04,0,1-Math.pow(1-clamp(p/.42),3))*width*amount;break;
  case 'diagonal':scale=1.13;x=mix(.028,-.028,q)*width*amount;y=mix(-.025,.025,q)*height*amount;break;
 }
 return {x:clamp(x,-width*(scale-1)/2+2,width*(scale-1)/2-2),y:clamp(y,-height*(scale-1)/2+2,height*(scale-1)/2-2),scale};
}
function entrance(shot:Shot,frame:number):{style:React.CSSProperties;blur:number}{
 const n=shot.transition.frames;if(!n||frame>=n)return {style:{},blur:0};
 const p=clamp(frame/n),q=1-Math.pow(1-p,3);
 switch(shot.transition.type){
  case 'dissolve':return {style:{opacity:p},blur:0};
  case 'wipe-left':return {style:{clipPath:'inset(0 '+((1-q)*100)+'% 0 0)'},blur:0};
  case 'wipe-right':return {style:{clipPath:'inset(0 0 0 '+((1-q)*100)+'%)'},blur:0};
  case 'rise':return {style:{opacity:q,transform:'translateY('+((1-q)*40)+'px)'},blur:0};
  case 'focus':return {style:{opacity:q},blur:(1-q)*7};
  case 'match-in':return {style:{opacity:q,transform:'scale('+(1+(1-q)*.045)+')'},blur:0};
  default:return {style:{},blur:0};
 }
}
function Timeline({frame,index}:{frame:number;index:number}){
 const {width}=useVideoConfig();const active=colors[seasonIndex(index)];
 return <div style={{position:'absolute',left:'6%',right:'6%',bottom:36,fontFamily:project.fonts.sans,color:'#efe8d9'}}>
  <div style={{position:'relative',height:28,fontSize:20,marginBottom:13,letterSpacing:3}}>{project.chapters.map((chapter,i)=><span key={chapter.label} style={{position:'absolute',left:((chapter.start-mainStart)/(mainEnd-mainStart)*100)+'%',opacity:i<=seasonIndex(index)?1:.45,color:colors[i]}}>{chapter.label}</span>)}</div>
  <div style={{height:1,background:'#bbb09a55',position:'relative'}}>
   <div style={{height:2,width:(clamp((frame-mainStart)/(mainEnd-mainStart))*100)+'%',background:active}}/>
   {[...mainShots.map(s=>s.start),mainEnd].map((start,i)=><div key={i} style={{position:'absolute',left:((start-mainStart)/(mainEnd-mainStart)*100)+'%',height:i%6===0?13:7,top:i%6===0?-6:-3,width:1,background:i<index?active:'#c0b79c55'}}/>)}
   <div style={{position:'absolute',left:(clamp((frame-mainStart)/(mainEnd-mainStart))*100)+'%',top:-4,width:9,height:9,background:active,borderRadius:9,boxShadow:'0 0 16px '+active}}/>
  </div>
  <div style={{position:'absolute',right:0,bottom:20,fontSize:18,letterSpacing:2}}>{String(index).padStart(2,'0')} / 24</div>
  <div style={{position:'absolute',right:0,bottom:50,fontSize:15,letterSpacing:1,opacity:.60}}>AI视觉演绎 · 物候因地而异</div>
  <div style={{position:'absolute',left:0,bottom:50,width:width*.2,height:1,background:'transparent'}}/>
 </div>;
}
function Dial({angle,progress,large=false}:{angle:number;progress:number;large?:boolean}){
 const r=large?187:128,c=large?245:185,a=(angle-90)*Math.PI/180,opacity=clamp(progress);
 return <svg width={c*2} height={c*2} style={{opacity,overflow:'visible'}}>
  <circle cx={c} cy={c} r={r} fill="#0b1019a8" stroke="#e4d4ad55" strokeWidth={1}/>
  <circle cx={c} cy={c} r={r-22} fill="none" stroke="#e4d4ad22"/>
  {Array.from({length:24},(_,i)=>{const t=(i*15-90)*Math.PI/180;return <line key={i} x1={c+(r-10)*Math.cos(t)} y1={c+(r-10)*Math.sin(t)} x2={c+r*Math.cos(t)} y2={c+r*Math.sin(t)} stroke={colors[Math.floor(i/6)]} strokeWidth={i%6?1:3}/>})}
  {[['春分',0],['夏至',90],['秋分',180],['冬至',270]].map(([label,n])=>{const t=(Number(n)-90)*Math.PI/180;return <text key={String(label)} x={c+(r+29)*Math.cos(t)} y={c+(r+29)*Math.sin(t)+7} textAnchor="middle" fill={n===angle?'#f0d69b':'#e6ddc7aa'} fontSize={large?24:20} fontFamily={project.fonts.serif}>{label}</text>})}
  <line x1={c} y1={c} x2={c+r*Math.cos(a)} y2={c+r*Math.sin(a)} stroke="#edc47c66"/>
  <circle cx={c+r*Math.cos(a)} cy={c+r*Math.sin(a)} r={large?11:8} fill="#f4d28f" style={{filter:'drop-shadow(0 0 10px #edbd6c)'}}/>
  <text x={c} y={c-9} textAnchor="middle" fill="#f1e5ca" fontSize={large?44:34} fontFamily={project.fonts.serif}>{large?'每15°':angle+'°'}</text>
  <text x={c} y={c+33} textAnchor="middle" fill="#d7c9a8aa" fontSize={large?24:19} fontFamily={project.fonts.sans}>{large?'一个节气':'太阳黄经位置'}</text>
 </svg>;
}
function Weather({shot,frame}:{shot:Shot;frame:number}){
 const {width,height}=useVideoConfig();
 if(shot.weather==='rain')return <svg width={width} height={height} style={{position:'absolute',inset:0,opacity:shot.index===12?.34:.24,pointerEvents:'none'}}>{Array.from({length:shot.index===12?100:50},(_,i)=>{const x=(hash(i+311)*width+frame*1.65)%(width+24)-12,y=(hash(i+511)*height+frame*6.2)%(height+24)-12;return <line key={i} x1={x} y1={y} x2={x-5} y2={y+17} stroke="#e5edf1" strokeOpacity={.3+hash(i+611)*.3} strokeWidth={1+hash(i+711)*.6}/>})}</svg>;
 if(shot.weather==='snow')return <svg width={width} height={height} style={{position:'absolute',inset:0,pointerEvents:'none'}}>{Array.from({length:shot.index===21?85:38},(_,i)=>{const speed=.65+hash(i+44)*1.6;return <circle key={i} cx={(hash(i+411)*width+Math.sin(frame*.025+i)*19+frame*.23)%width} cy={(hash(i+511)*height+frame*speed)%(height+20)-10} r={1+hash(i+33)*2.8} fill="#eef5fa" opacity={.18+hash(i+9)*.42}/>})}</svg>;
 if(shot.weather==='mist')return <div style={{position:'absolute',left:-width*.2+Math.sin(frame*.006)*width*.05,top:height*.50,width:width*1.4,height:height*.3,background:'radial-gradient(ellipse,#dee9ed17,transparent 68%)',filter:'blur(20px)',pointerEvents:'none'}}/>;
 return null;
}
function ImageLayers({shot,frame,p}:{shot:Shot;frame:number;p:number}){
 const {width,height}=useVideoConfig(),cam=cameraPose(shot.camera,p,width,height);
 return <>{shot.layers.map((layer,i)=>{
  const a=assets.get(layer.assetId);if(!a)return null;const bg=layer.role==='background',depth=layer.parallax??1,m=layer.motion??{};
  const x=(layer.x+mix(m.x0??0,m.x1??0,p))*width+cam.x*depth,y=(layer.y+mix(m.y0??0,m.y1??0,p))*height+cam.y*depth;
  const accent=beatAccent(shot,frame)*(shot.accentStrength??0);
  const settling=bg?1:1-.018*(1-clamp(frame/11));
  const scale=(bg?cam.scale:1+(cam.scale-1)*.4)*mix(m.scale0??1,m.scale1??1,p)*settling*(1+(bg?Math.max(0,accent)*.20:accent)),rotate=bg?0:Math.sin(frame*.023+i)*(m.sway??0);
  return <React.Fragment key={layer.assetId}>
   {shot.index===9&&i===1?<div style={{position:'absolute',left:'49%',top:'10%',width:'44%',height:'82%',background:'linear-gradient(130deg,#eee1bded,#c8b88be8)',border:'1px solid #f4e8ca88',boxShadow:'0 18px 50px #00000040'}}/>:null}
   {layer.assetId.endsWith('-boat')?<div style={{position:'absolute',left:x+layer.w*width*.20,top:y+layer.h*height*.88,width:layer.w*width*.62,height:9,borderRadius:'50%',background:'#152c3999',filter:'blur(3px)',boxShadow:'0 4px 4px #b5d3ce66',transform:'scale('+scale+')'}}/>:null}
   <Img src={staticFile(a.file)} style={{position:'absolute',left:x,top:y,width:layer.w*width,height:layer.h*height,objectFit:layer.fit??(bg?'cover':'contain'),transform:'scale('+scale+') rotate('+rotate+'deg)',transformOrigin:bg?'50% 50%':'70% 85%',opacity:layer.opacity??1,maskImage:layer.assetId.endsWith('-boat')?'linear-gradient(180deg,#000 0%,#000 81%,transparent 92%)':undefined,filter:a.alpha?'drop-shadow(0 9px 14px #00000022)':undefined}}/>
  </React.Fragment>;
 })}</>;
}
function Opening({shot}:{shot:Shot}){
 const frame=useCurrentFrame(),{width}=useVideoConfig(),p=clamp(frame/149),a=assets.get(shot.layers[0]?.assetId),q=1-Math.pow(1-p,2);
 const cues=project.openingCueFrames;
 const textVisible=frame<shot.end-shot.start?1:0;
 const first=clamp((frame+1-cues.first)/5),second=clamp((frame-cues.second)/5),question=(1-clamp((frame-cues.questionOut)/7))*textVisible,title=clamp((frame-cues.title)/7)*textVisible;
 return <AbsoluteFill style={{overflow:'hidden',background:'#0b1017'}}>
  {a?<Img src={staticFile(a.file)} style={{width:'100%',height:'100%',objectFit:'cover',transform:'scale('+(1.04+q*.055)+') translateX('+(-q*10)+'px)',opacity:1-title*.30}}/>:null}
  <AbsoluteFill style={{background:'linear-gradient(90deg,#050b15e8,transparent 90%)'}}/>
  <div style={{position:'absolute',left:'7%',top:'27%',fontFamily:project.fonts.serif,color:'#f3ead9',fontSize:width*.054,lineHeight:1.4,letterSpacing:3,opacity:question}}>
   <div style={{opacity:first,transform:'translateY('+((1-first)*15)+'px)'}}>冰还没化，</div>
   <div style={{opacity:second,transform:'translateY('+((1-second)*15)+'px)'}}>怎么就<span style={{color:'#efc989'}}>立春</span>了？</div>
  </div>
  <div style={{position:'absolute',left:'7%',top:'34%',opacity:title,color:'#f2e7ce',fontFamily:project.fonts.serif,transform:'translateY('+((1-title)*14)+'px)'}}>
   <div style={{fontSize:width*.067,letterSpacing:10}}>二十四节气</div>
   <div style={{fontFamily:project.fonts.sans,fontSize:30,letterSpacing:7,marginTop:32,opacity:clamp((frame-cues.tagline)/6)}}>顺着太阳，读懂一年</div>
  </div>
  <div style={{position:'absolute',right:'9%',top:'24%',opacity:title,transform:'scale('+(1.05-title*.05)+')'}}><Dial angle={315} progress={title} large/></div>
  <div style={{position:'absolute',left:'7%',bottom:58,fontFamily:project.fonts.sans,color:'#dcd1ba88',fontSize:18,letterSpacing:4,opacity:textVisible}}>二十四节气 · 春生夏长 秋收冬藏</div>
 </AbsoluteFill>;
}
function Ending({shot}:{shot:Shot}){
 const frame=useCurrentFrame(),{height}=useVideoConfig(),duration=shot.end-shot.start,p=clamp(frame/(duration-1));
 return <AbsoluteFill style={{overflow:'hidden',background:'#0a1015',opacity:1-clamp((frame-duration+21)/20)}}>
  {shot.layers.map((l,i)=>{const a=assets.get(l.assetId);return a?<div key={l.assetId} style={{position:'absolute',left:(i*25)+'%',width:'25%',height:'100%',overflow:'hidden',borderRight:'1px solid #f0debe33'}}><Img src={staticFile(a.file)} style={{width:'100%',height:'100%',objectFit:'cover',transform:'scale('+(1.12-p*.09)+')'}}/><div style={{position:'absolute',left:36,top:55,color:colors[i],fontFamily:project.fonts.serif,fontSize:36}}>{['春生','夏长','秋收','冬藏'][i]}</div></div>:null})}
  <AbsoluteFill style={{background:'linear-gradient(180deg,#05090d55,#05090dbb)',opacity:.7+p*.2}}/>
  <div style={{position:'absolute',top:height*.36,width:'100%',textAlign:'center',color:'#f1e5ca',fontFamily:project.fonts.serif,opacity:clamp(frame/14)}}>
   <div style={{fontSize:104,letterSpacing:14}}>二十四节气</div>
   <div style={{fontSize:32,letterSpacing:4,marginTop:43,lineHeight:1.8,opacity:clamp((frame-45)/9),transform:'translateY('+((1-clamp((frame-45)/9))*10)+'px)'}}>记下的不只是时间<br/>也是人与大地相处的方式</div>
  </div>
  <div style={{position:'absolute',bottom:55,width:'100%',textAlign:'center',fontFamily:project.fonts.sans,fontSize:18,color:'#d7cdb888',letterSpacing:3}}>AI视觉演绎 · {project.musicCredit}</div>
 </AbsoluteFill>;
}
function PoetryOverlay({poem,frame,bottom}:{poem:Poem;frame:number;bottom:boolean}){
 const {width,height}=useVideoConfig(),single=poem.lines.length===1;
 const sourceOpacity=clamp((frame-poem.attributionCueFrame)/7);
 return <div style={{position:'absolute',left:width*.06,top:height*(poem.top??(bottom?.16:.565)),width:width*.405,color:'#eed5a4',fontFamily:project.fonts.serif,pointerEvents:'none'}}>
  {bottom?<div style={{position:'absolute',left:-50,top:-50,width:'120%',height:single?240:330,background:'radial-gradient(ellipse at 25% 50%,#05101b94,transparent 72%)',opacity:clamp((frame-poem.cueFrame)/8)}}/>:null}
  <div style={{position:'relative',borderLeft:'2px solid #e1bc7755',paddingLeft:25}}>
   {poem.lines.map((line,i)=>{const show=clamp((frame-poem.cueFrame-i*poem.lineStaggerFrames)/8),q=1-Math.pow(1-show,3);return <div key={line} style={{fontSize:single?76:62,lineHeight:1.42,letterSpacing:5,whiteSpace:'nowrap',opacity:show,transform:'translateY('+((1-q)*12)+'px)',textShadow:'0 2px 8px #000000aa'}}>{line}</div>})}
   <div style={{fontFamily:project.fonts.sans,fontSize:22,lineHeight:1.7,letterSpacing:1.2,marginTop:20,color:'#e4dcc9b8',opacity:sourceOpacity,textShadow:'0 2px 6px #000000aa'}}>{poem.author} ·《{poem.work}》</div>
  </div>
 </div>;
}
function SceneView({shot}:{shot:Shot}){
 const frame=useCurrentFrame(),{width,height}=useVideoConfig(),duration=shot.end-shot.start,p=clamp(frame/Math.max(1,duration-1)),incoming=entrance(shot,frame);
 const labels=frame<duration,index=shot.index??1,accent=colors[seasonIndex(index)],bottom=shot.layout==='bottom';
 const labelEntry=shot.transition.type==='cut'?1:clamp((frame+1)/5),subtitleEntry=clamp((frame-(shot.labelCueFrames?.subtitle??7))/6);
 if(shot.visual==='calendar-opening')return <Opening shot={shot}/>;
 if(shot.visual==='calendar-ending')return <AbsoluteFill style={incoming.style}><Ending shot={shot}/></AbsoluteFill>;
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <AbsoluteFill style={incoming.style}>
   <AbsoluteFill style={{filter:incoming.blur?'blur('+incoming.blur+'px)':undefined}}>
    <ImageLayers shot={shot} frame={frame} p={p}/><Weather shot={shot} frame={frame}/>
   </AbsoluteFill>
   <AbsoluteFill style={{background:bottom?'linear-gradient(0deg,#030810e8,transparent 80%)':'linear-gradient(90deg,#05090ee8,transparent 66%)'}}/>
   <AbsoluteFill style={{boxShadow:'inset 0 0 140px #00000022'}}/>
  </AbsoluteFill>
  {labels?<>
   <div style={{position:'absolute',left:width*.06,top:height*(bottom?.49:.15),width:width*.43,color:'#f0e6d0',fontFamily:project.fonts.serif,opacity:labelEntry,transform:'translateY('+((1-labelEntry)*10)+'px)'}}>
    <div style={{fontSize:width*.032,marginBottom:height*.065,whiteSpace:'nowrap',color:accent}}>{shot.kicker}</div>
    <div style={{fontSize:width*.054,lineHeight:1.15,letterSpacing:4}}>{shot.title}</div>
    <div style={{fontSize:30,lineHeight:1.8,marginTop:26,letterSpacing:1.3,maxWidth:width*.40,opacity:subtitleEntry}}>{shot.subtitle}</div>
    {index===1?<div style={{fontFamily:project.fonts.sans,fontSize:22,marginTop:28,color:'#cdd8dea6'}}>节气入春，天气因地而异</div>:null}
   </div>
   {index===9?<><div style={{position:'absolute',right:'15%',bottom:'16%',fontFamily:project.fonts.sans,fontSize:22,color:'#493720',letterSpacing:3}}>北方麦收</div><div style={{position:'absolute',left:'7%',bottom:'20%',fontFamily:project.fonts.sans,fontSize:22,color:'#d1e4bb',letterSpacing:3}}>南方夏种</div></>:null}
   {shot.poem?<PoetryOverlay poem={shot.poem} frame={frame} bottom={bottom}/>:null}
   {[4,10,16,22].includes(index)?<div style={{position:'absolute',right:'10%',bottom:'14%',transform:'scale(.90)'}}><Dial angle={Number(shot.kicker.match(/(\d+)°/)?.[1]??0)} progress={clamp((frame-12)/14)}/></div>:null}
   <Timeline frame={shot.start+frame} index={index}/>
  </>:null}
 </AbsoluteFill>;
}
export const ThemeFilm:React.FC=()=> <AbsoluteFill style={{background:'#0b1017'}}><Audio src={staticFile(project.audio.file)}/>{shots.map((shot,i)=><Sequence key={shot.id} name={shot.title} from={shot.start} durationInFrames={shot.end-shot.start+(shots[i+1]?.transition.frames??0)}><SceneView shot={shot}/></Sequence>)}</AbsoluteFill>;

