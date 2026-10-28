import React from 'react';
import {AbsoluteFill,Audio,Img,Sequence,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import projectJson from '../public/project.json';
import shotsJson from '../public/shots.json';
import assetsJson from '../public/assets.json';

type Motion={x0?:number;x1?:number;y0?:number;y1?:number;scale0?:number;scale1?:number;sway?:number};
type Layer={assetId:string;role:string;x:number;y:number;w:number;h:number;fit?:'cover'|'contain';parallax?:number;opacity?:number;label?:string;shadow?:boolean;maskBottom?:boolean;motion?:Motion};
type Poem={lines:string[];author:string;work:string;sourceUrl:string;cueFrame:number;lineStaggerFrames:number;attributionCueFrame:number;top?:number;fontSize?:number};
type Shot={id:string;start:number;end:number;section:string;chapter:string;title:string;subtitle:string;kicker?:string;layout?:string;visual?:string;weather?:string;weatherIntensity?:number;accentColor?:string;camera:{type:string;amount?:number};transition:{type:string;frames:number};layers:Layer[];accentFrames?:number[];accentStrength?:number;labelCueFrames?:{kicker:number;title:number;subtitle:number};poem?:Poem;words?:{text:string;frame:number;color?:string}[]};
type Project={topic:string;status:string;width:number;height:number;fps:number;durationFrames:number;fonts:{serif:string;sans:string};palette:Record<string,string>;chapters:{label:string;start:number;color?:string}[];audio:{file:string;offsetSeconds?:number};disclosure?:string;musicCredit?:string;opening?:{lines:{text:string;frame:number}[];questionOut:number;titleFrame:number;taglineFrame:number;tagline:string;footer?:string};ending?:{panelLabels?:string[];lines?:string[];subtitleFrame?:number;footer?:string}};
type Asset={id:string;file:string;alpha?:boolean};
export const project=projectJson as unknown as Project;
export const shots=shotsJson as unknown as Shot[];
const assets=new Map((assetsJson.assets as Asset[]).map(a=>[a.id,a]));
const clamp=(n:number,a=0,b=1)=>Math.max(a,Math.min(b,n));
const mix=(a:number,b:number,p:number)=>a+(b-a)*p;
const hash=(n:number)=>{const v=Math.sin(n*12.9898)*43758.5453;return v-Math.floor(v);};
const main=shots.filter(s=>s.section==='main');
const firstMain=main[0]?.start??0,lastMain=main[main.length-1]?.end??project.durationFrames;
const beat=(shot:Shot,frame:number)=>(shot.accentFrames??[]).reduce((v,c)=>{const t=frame-c;return v+(t>=0&&t<22?Math.sin(t*Math.PI/11)*Math.exp(-t/9):0);},0);
const chapterColor=(frame:number)=>[...(project.chapters??[])].reverse().find(c=>frame>=c.start)?.color??project.palette.accent;
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
function Timeline({frame,shot}:{frame:number;shot:Shot}){
 const {width,height}=useVideoConfig(),active=chapterColor(frame),n=main.findIndex(s=>s.id===shot.id)+1,span=Math.max(1,lastMain-firstMain),pct=clamp((frame-firstMain)/span)*100;
 return <div style={{position:'absolute',left:'6%',right:'6%',bottom:height*.035,fontFamily:project.fonts.sans,color:project.palette.text}}>
  <div style={{position:'relative',height:height*.026,fontSize:width*.0104,marginBottom:height*.012,letterSpacing:3}}>{project.chapters.map(c=><span key={c.start} style={{position:'absolute',left:clamp((c.start-firstMain)/span)*100+'%',opacity:frame>=c.start?1:.45,color:c.color??active}}>{c.label}</span>)}</div>
  <div style={{height:1,background:'#bbb09a55',position:'relative'}}><div style={{height:2,width:pct+'%',background:active}}/>{[...main.map(s=>s.start),lastMain].map((f,i)=><div key={i} style={{position:'absolute',left:((f-firstMain)/span*100)+'%',height:7,top:-3,width:1,background:f<=frame?active:'#c0b79c55'}}/>)}<div style={{position:'absolute',left:pct+'%',top:-4,width:8,height:8,background:active,borderRadius:8}}/></div>
  {n>0?<div style={{position:'absolute',right:0,bottom:20,fontSize:width*.0094,letterSpacing:2}}>{String(n).padStart(2,'0')} / {main.length}</div>:null}
  {project.disclosure?<div style={{position:'absolute',right:0,bottom:48,fontSize:width*.0078,opacity:.6}}>{project.disclosure}</div>:null}
 </div>;
}
function Weather({shot,frame}:{shot:Shot;frame:number}){
 const {width,height}=useVideoConfig(),intensity=shot.weatherIntensity??1;
 if(shot.weather==='rain')return <svg width={width} height={height} style={{position:'absolute',inset:0,opacity:.24,pointerEvents:'none'}}>{Array.from({length:Math.round(50*intensity)},(_,i)=>{const x=(hash(i+311)*width+frame*1.65)%(width+24)-12,y=(hash(i+511)*height+frame*6.2)%(height+24)-12;return <line key={i} x1={x} y1={y} x2={x-5} y2={y+17} stroke="#e5edf1" strokeOpacity={.3+hash(i+611)*.3} strokeWidth={1+hash(i+711)*.6}/>;})}</svg>;
 if(shot.weather==='snow')return <svg width={width} height={height} style={{position:'absolute',inset:0,pointerEvents:'none'}}>{Array.from({length:Math.round(38*intensity)},(_,i)=><circle key={i} cx={(hash(i+411)*width+Math.sin(frame*.025+i)*19+frame*.23)%width} cy={(hash(i+511)*height+frame*(.65+hash(i+44)*1.6))%(height+20)-10} r={1+hash(i+33)*2.8} fill="#eef5fa" opacity={.18+hash(i+9)*.42}/>)}</svg>;
 if(shot.weather==='mist')return <div style={{position:'absolute',left:-width*.2+Math.sin(frame*.006)*width*.05,top:height*.5,width:width*1.4,height:height*.3,background:'radial-gradient(ellipse,#dee9ed17,transparent 68%)',filter:'blur(20px)',pointerEvents:'none'}}/>;
 return null;
}
function ImageLayers({shot,frame,p}:{shot:Shot;frame:number;p:number}){
 const {width,height}=useVideoConfig(),cam=cameraPose(shot.camera,p,width,height);
 return <>{shot.layers.map((l,i)=>{
  const a=assets.get(l.assetId);if(!a)return null;const bg=l.role==='background',depth=l.parallax??(bg?1:1.4),m=l.motion??{};
  const x=(l.x+mix(m.x0??0,m.x1??0,p))*width+cam.x*depth,y=(l.y+mix(m.y0??0,m.y1??0,p))*height+cam.y*depth;
  const pulse=beat(shot,frame)*(shot.accentStrength??0),settle=bg?1:1-.018*(1-clamp(frame/11));
  const scale=(bg?cam.scale:1+(cam.scale-1)*.4)*mix(m.scale0??1,m.scale1??1,p)*settle*(1+(bg?Math.max(0,pulse)*.2:pulse)),rotate=bg?0:Math.sin(frame*.023+i)*(m.sway??0);
  return <React.Fragment key={l.assetId}>
   {l.shadow?<div style={{position:'absolute',left:x+l.w*width*.2,top:y+l.h*height*.88,width:l.w*width*.62,height:9,borderRadius:'50%',background:'#152c3999',filter:'blur(3px)',transform:'scale('+scale+')'}}/>:null}
   <Img src={staticFile(a.file)} style={{position:'absolute',left:x,top:y,width:l.w*width,height:l.h*height,objectFit:l.fit??(bg?'cover':'contain'),transform:'scale('+scale+') rotate('+rotate+'deg)',transformOrigin:bg?'50% 50%':'70% 85%',opacity:l.opacity??1,maskImage:l.maskBottom?'linear-gradient(180deg,#000 0%,#000 81%,transparent 92%)':undefined,filter:a.alpha?'drop-shadow(0 9px 14px #00000022)':undefined}}/>
  </React.Fragment>;
 })}</>;
}
function Poetry({poem,frame,bottom}:{poem:Poem;frame:number;bottom:boolean}){
 const {width,height}=useVideoConfig(),single=poem.lines.length===1,size=poem.fontSize??width*(single?.0396:.0323);
 return <div style={{position:'absolute',left:'6%',top:height*(poem.top??(bottom?.16:.565)),width:'41%',color:'#eed5a4',fontFamily:project.fonts.serif,pointerEvents:'none'}}>
  {bottom?<div style={{position:'absolute',left:-50,top:-50,width:'120%',height:single?240:330,background:'radial-gradient(ellipse at 25% 50%,#05101b94,transparent 72%)',opacity:clamp((frame-poem.cueFrame)/8)}}/>:null}
  <div style={{position:'relative',borderLeft:'2px solid #e1bc7755',paddingLeft:width*.013}}>
   {poem.lines.map((line,i)=>{const show=clamp((frame-poem.cueFrame-i*poem.lineStaggerFrames)/8),q=1-Math.pow(1-show,3);return <div key={line} style={{fontSize:size,lineHeight:1.42,letterSpacing:5,whiteSpace:'nowrap',opacity:show,transform:'translateY('+((1-q)*12)+'px)',textShadow:'0 2px 8px #000000aa'}}>{line}</div>;})}
   <div style={{fontFamily:project.fonts.sans,fontSize:width*.0115,lineHeight:1.7,letterSpacing:1.2,marginTop:20,color:'#e4dcc9b8',opacity:clamp((frame-poem.attributionCueFrame)/7),textShadow:'0 2px 6px #000000aa'}}>{poem.author} ·《{poem.work}》</div>
  </div>
 </div>;
}
function Opening({shot}:{shot:Shot}){
 const frame=useCurrentFrame(),{width,height}=useVideoConfig(),duration=shot.end-shot.start,config=project.opening;
 const a=assets.get(shot.layers[0]?.assetId),p=clamp(frame/Math.max(1,duration-1)),visible=frame<duration?1:0,title=clamp((frame-(config?.titleFrame??0))/7)*visible;
 return <AbsoluteFill style={{overflow:'hidden',background:'#0b1017'}}>
  {a?<Img src={staticFile(a.file)} style={{width:'100%',height:'100%',objectFit:'cover',transform:'scale('+(1.04+(1-Math.pow(1-p,2))*.055)+')',opacity:1-title*.3}}/>:null}
  <AbsoluteFill style={{background:'linear-gradient(90deg,#050b15e8,transparent 90%)'}}/>
  {config?<div style={{position:'absolute',left:'7%',top:'27%',fontFamily:project.fonts.serif,color:project.palette.text,fontSize:width*.054,lineHeight:1.4,opacity:(1-clamp((frame-config.questionOut)/7))*visible}}>{config.lines.map(l=>{const show=clamp((frame-l.frame+1)/5);return <div key={l.frame} style={{opacity:show,transform:'translateY('+((1-show)*15)+'px)'}}>{l.text}</div>;})}</div>:null}
  <div style={{position:'absolute',left:'7%',top:'34%',opacity:title,color:project.palette.text,fontFamily:project.fonts.serif,transform:'translateY('+((1-title)*14)+'px)'}}>
   <div style={{fontSize:width*.067,letterSpacing:10}}>{shot.title||project.topic}</div>
   <div style={{fontFamily:project.fonts.sans,fontSize:width*.0156,letterSpacing:7,marginTop:32,opacity:clamp((frame-(config?.taglineFrame??12))/6)}}>{config?.tagline??shot.subtitle}</div>
  </div>
  {config?.footer?<div style={{position:'absolute',left:'7%',bottom:height*.054,fontFamily:project.fonts.sans,color:'#dcd1ba88',fontSize:width*.0094,letterSpacing:4,opacity:visible}}>{config.footer}</div>:null}
 </AbsoluteFill>;
}
function Ending({shot}:{shot:Shot}){
 const frame=useCurrentFrame(),{width,height}=useVideoConfig(),duration=shot.end-shot.start,p=clamp(frame/Math.max(1,duration-1)),count=Math.max(1,shot.layers.length),config=project.ending,show=clamp((frame-(config?.subtitleFrame??45))/9);
 return <AbsoluteFill style={{overflow:'hidden',background:'#0a1015',opacity:1-clamp((frame-duration+21)/20)}}>
  {shot.layers.map((l,i)=>{const a=assets.get(l.assetId);return a?<div key={l.assetId} style={{position:'absolute',left:(i*100/count)+'%',width:(100/count)+'%',height:'100%',overflow:'hidden',borderRight:'1px solid #f0debe33'}}><Img src={staticFile(a.file)} style={{width:'100%',height:'100%',objectFit:'cover',transform:'scale('+(1.12-p*.09)+')'}}/>{l.label||config?.panelLabels?.[i]?<div style={{position:'absolute',left:width*.019,top:height*.051,color:'#efe8d9aa',fontFamily:project.fonts.serif,fontSize:width*.019}}>{l.label??config?.panelLabels?.[i]}</div>:null}</div>:null;})}
  <AbsoluteFill style={{background:'linear-gradient(180deg,#05090d55,#05090dbb)',opacity:.7+p*.2}}/>
  <div style={{position:'absolute',top:'36%',width:'100%',textAlign:'center',color:project.palette.text,fontFamily:project.fonts.serif,opacity:clamp(frame/14)}}>
   <div style={{fontSize:width*.0542,letterSpacing:14}}>{shot.title||project.topic}</div>
   <div style={{fontSize:width*.0167,letterSpacing:4,marginTop:43,lineHeight:1.8,opacity:show,transform:'translateY('+((1-show)*10)+'px)'}}>{(config?.lines??[shot.subtitle]).map((line,i)=><div key={i}>{line}</div>)}</div>
  </div>
  {config?.footer||project.musicCredit?<div style={{position:'absolute',bottom:height*.051,width:'100%',textAlign:'center',fontFamily:project.fonts.sans,fontSize:width*.0094,color:'#d7cdb888',letterSpacing:3}}>{config?.footer??project.musicCredit}</div>:null}
 </AbsoluteFill>;
}
function SceneView({shot}:{shot:Shot}){
 const frame=useCurrentFrame(),{width,height}=useVideoConfig(),duration=shot.end-shot.start,p=clamp(frame/Math.max(1,duration-1)),incoming=entrance(shot,frame),labels=frame<duration,bottom=shot.layout==='bottom',accent=shot.accentColor??chapterColor(shot.start);
 if(shot.visual==='hook-opening'||shot.visual==='calendar-opening')return <Opening shot={shot}/>;
 if(shot.visual==='panel-ending'||shot.visual==='calendar-ending')return <AbsoluteFill style={incoming.style}><Ending shot={shot}/></AbsoluteFill>;
 const entry=shot.transition.type==='cut'?1:clamp((frame+1)/5),subtitle=clamp((frame-(shot.labelCueFrames?.subtitle??7))/6),vertical=height>width;
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <AbsoluteFill style={incoming.style}>
   <AbsoluteFill style={{background:project.palette.dark,filter:incoming.blur?'blur('+incoming.blur+'px)':undefined}}><ImageLayers shot={shot} frame={frame} p={p}/><Weather shot={shot} frame={frame}/></AbsoluteFill>
   <AbsoluteFill style={{background:bottom?'linear-gradient(0deg,#030810e8,transparent 80%)':'linear-gradient(90deg,#05090ee8,transparent 66%)'}}/>
   <AbsoluteFill style={{boxShadow:'inset 0 0 140px #00000022'}}/>
  </AbsoluteFill>
  {labels?<>
   {shot.words?.length?<div style={{position:'absolute',left:'7%',right:'7%',top:'36%',fontFamily:project.fonts.serif,fontSize:width*.06,color:project.palette.text,textAlign:'center'}}>{shot.words.filter(w=>frame>=w.frame).map(w=><span key={w.frame} style={{marginRight:20,opacity:clamp((frame-w.frame+1)/3),color:w.color==='accent'?accent:undefined}}>{w.text}</span>)}</div>:<div style={{position:'absolute',left:'6%',top:height*(bottom?.49:.15),width:width*(vertical?.86:.43),color:project.palette.text,fontFamily:project.fonts.serif,opacity:entry,transform:'translateY('+((1-entry)*10)+'px)'}}>
    {shot.kicker?<div style={{fontSize:width*.032,marginBottom:height*.065,color:accent}}>{shot.kicker}</div>:null}
    <div style={{fontSize:width*(vertical?.08:.054),lineHeight:1.15,letterSpacing:4}}>{shot.title}</div>
    <div style={{fontSize:width*(vertical?.03:.0156),lineHeight:1.8,marginTop:26,letterSpacing:1.3,opacity:subtitle}}>{shot.subtitle}</div>
   </div>}
   {shot.poem?<Poetry poem={shot.poem} frame={frame} bottom={bottom}/>:null}
   <Timeline frame={shot.start+frame} shot={shot}/>
   {project.status!=='ready'?<div style={{position:'absolute',right:'6%',top:'5%',fontFamily:project.fonts.sans,color:accent,fontSize:width*.012}}>制作预览</div>:null}
  </>:null}
 </AbsoluteFill>;
}
export const ThemeFilm:React.FC=()=> <AbsoluteFill style={{background:project.palette.dark}}>
 {project.audio.file?<Audio src={staticFile(project.audio.file)} startFrom={Math.round((project.audio.offsetSeconds??0)*project.fps)}/>:null}
 {shots.map((shot,i)=><Sequence key={shot.id} name={shot.title} from={shot.start} durationInFrames={shot.end-shot.start+(shots[i+1]?.transition.frames??0)}><SceneView shot={shot}/></Sequence>)}
</AbsoluteFill>;
