"""Attach verified public-domain verse; preserve the approved V4 timing and audio."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
rows=[
 (1,'立春',['律回岁晚冰霜少','春到人间草木知'],'张栻','立春偶成','https://www.ccdi.gov.cn/yaowenn/202501/t20250126_402828_m.html'),
 (2,'雨水',['好雨知时节','当春乃发生'],'杜甫','春夜喜雨','https://www.moe.gov.cn/srcsite/A06/s3331/201612/W020161213303084709835.pdf'),
 (3,'惊蛰',['微雨众卉新','一雷惊蛰始'],'韦应物','观田家','https://www.beijing.gov.cn/renwen/zt/essjq/zjs/202209/t20220908_2811393.html'),
 (4,'春分',['仲春初四日','春色正中分'],'徐铉','春分日','https://dfzb.suzhou.gov.cn/dfzb/szdq/202203/fccc818c79dd44ecac50d2eb5b1a9aa0.shtml'),
 (5,'清明',['梨花风起正清明','游子寻春半出城'],'吴惟信','苏堤清明即事','https://www.qingcheng.gov.cn/zjqc/mswh/content/post_150917.html'),
 (6,'谷雨',['谷雨春光晓','山川黛色青'],'元稹','咏廿四气诗·谷雨三月中','https://www.bjqtm.com/xcjy/dwxc/宝博微课堂｜诗词话节气-谷雨春光晓，山川黛色青'),
 (7,'立夏',['绿阴幽草胜花时'],'王安石','初夏即事','https://zh.wikisource.org/zh-hans/初夏即事'),
 (8,'小满',['麦穗初齐稚子娇','桑叶正肥蚕食饱'],'欧阳修','归田园四时乐春夏二首·其二','https://www.kfdsw.com/index/detail/id/2670.html'),
 (9,'芒种',['时雨及芒种','四野皆插秧'],'陆游','时雨','https://wn.bjsjw.gov.cn/n702/20250310/i101223.html'),
 (10,'夏至',['昼晷已云极'],'韦应物','夏至避暑北池','https://wjw.shanxi.gov.cn/zfxxgk/fdzdgknr/jkzx/202505/t20250516_9835856.shtml'),
 (11,'小暑',['荷风送香气','竹露滴清响'],'孟浩然','夏日南亭怀辛大','https://www.cma.gov.cn/2011xzt/20150130/20150701/201507/t20150701_286561.html'),
 (12,'大暑',['连雨不知春去','一晴方觉夏深'],'范成大','喜晴','https://m.ahjjjc.gov.cn/p/60817.html'),
 (13,'立秋',['自古逢秋悲寂寥','我言秋日胜春朝'],'刘禹锡','秋词二首·其一','https://yllhj.beijing.gov.cn/ztxx/bjhx/hhzs/202011/t20201104_2128451.shtml'),
 (14,'处暑',['袅袅凉风起'],'白居易','早秋曲江感怀','https://www.bjqtm.com/xcjy/dwxc/宝博微课堂金文话节气-处暑'),
 (15,'白露',['露从今夜白','月是故乡明'],'杜甫','月夜忆舍弟','https://hb.cma.gov.cn/qxkp/qxkp/202202/t20220207_4494148.html'),
 (16,'秋分',['金气秋分','风清露冷秋期半'],'谢逸','点绛唇·金气秋分','https://m.12371.gov.cn/content/2023-09/23/content_449476.html'),
 (17,'寒露',['袅袅凉风动','凄凄寒露零'],'白居易','池上','https://www.shidianguji.com/mingju/7623272193846034483'),
 (18,'霜降',['草木摇落露为霜'],'曹丕','燕歌行二首·其一','https://www.bjxch.gov.cn/file/20191108/1573199211783080701.pdf'),
 (19,'立冬',['秋风吹尽旧庭柯','黄叶丹枫客里过'],'王稚登','立冬','https://www.sqlzw.gov.cn/sitesources/nysjwjw/page_pc/xcjd/wh/article5698d5bb9e8f41ccb35c541a293116f5.html'),
 (20,'小雪',['坐看青竹变琼枝'],'高骈','对雪','https://dxs.moe.gov.cn/zx/a/jj/220210/1747122.shtml'),
 (21,'大雪',['忽如一夜春风来','千树万树梨花开'],'岑参','白雪歌送武判官归京','https://www.nationalreading.gov.cn/ydzg/plgc/202508/t20250815_926664.html'),
 (22,'冬至',['天时人事日相催','冬至阳生春又来'],'杜甫','小至','https://www.beijing.gov.cn/renwen/zt/essjq/hsjq/202209/t20220908_2811456.html'),
 (23,'小寒',['凌寒独自开'],'王安石','梅花','https://yllhj.beijing.gov.cn/ztxx/bjhx/hhzs/201902/t20190222_118661.shtml'),
 (24,'大寒',['大寒雪未消','闭户不能出'],'陆游','大寒','https://paper.people.com.cn/zgnyb/pc/attachement/202501/20/460e9077-87be-47d8-8262-b688d3720d3f.pdf')
]
# Preserve exact observed reference URLs, including the site's actual punctuation in the slug.
rows[5]=(*rows[5][:-1],'https://www.bjqtm.com/xcjy/dwxc/%E5%AE%9D%E5%8D%9A%E5%BE%AE%E8%AF%BE%E5%A0%82%EF%BD%9C%E8%AF%97%E8%AF%8D%E8%AF%9D%E8%8A%82%E6%B0%94-%E8%B0%B7%E9%9B%A8%E6%98%A5%E5%85%89%E6%99%93%EF%BC%8C%E5%B1%B1%E5%B7%9D%E9%BB%9B')
rows[13]=(*rows[13][:-1],'https://www.bjqtm.com/xcjy/dwxc/%E5%AE%9D%E5%8D%9A%E5%BE%AE%E8%AF%BE%E5%A0%82%E9%87%91%E6%96%87%E8%AF%9D%E8%8A%82%E6%B0%94-%E5%A4%84%E6%9A%91')
shots_path=root/'public/shots.json';shots=json.loads(shots_path.read_text(encoding='utf-8'))
records=[]
for index,term,lines,author,work,url in rows:
 s=next(s for s in shots if s.get('index')==index)
 assert s['title']==term
 poem={'lines':lines,'author':author,'work':work,'sourceUrl':url,'verified':True,'copyright':'古代诗词，原文属公有领域；仅节选原文，不采用现代译文或赏析。','cueFrame':12,'lineStaggerFrames':6,'attributionCueFrame':24,'placement':'upper-left' if s.get('layout')=='bottom' else 'lower-left'}
 if index==9:poem['top']=.53
 s['poem']=poem
 if s['end']-s['start']<=90:assert len(lines)==1
 records.append({'index':index,'term':term,'excerpt':'，'.join(lines)+'。','author':author,'work':work,'source_url':url,'text_and_attribution_checked':True,'relationship':'节气或相应时令意象；部分诗作并非专为该节气而作。','clip_seconds':[(s['start']/30),(s['end']/30)],'short_excerpt_for_fast_shot':len(lines)==1})
shots_path.write_text(json.dumps(shots,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'public/poems.json').write_text(json.dumps({'selection_note':'每节气一处古诗词节选；按镜头时长选一联或一句。诗句为文化意象，不用于替代物候科学说明。','poems':records},ensure_ascii=False,indent=2),encoding='utf-8')
md='# 二十四节气诗句与出处 · V5\n\n每节气一处独立诗词文字层。较长镜头用一联，3秒短镜头只用一句。以下为古代诗词原文节选，作者及篇名逐条核对；节气配对包含同季节物候意象，并非每首作品都专为该节气而作。\n\n|节气|画面诗句|作者与作品|核对来源|\n|---|---|---|---|\n'
for r in records:md+=f"|{r['term']}|{r['excerpt']}|{r['author']}《{r['work']}》|[原文/权威选录]({r['source_url']})|\n"
md+='\n校核说明：小满采用可在欧阳修作品中核对的《归田园四时乐春夏二首·其二》，未采用网络上流传且归属容易混淆的《五绝·小满》。秋分选谢逸词，避免人名异写的争议条目。原文保留“晷”“袅”“柯”等字，不用同音字替换。\n'
(root/'poetry-sources.md').write_text(md,encoding='utf-8')
project_path=root/'public/project.json';project=json.loads(project_path.read_text(encoding='utf-8'));project['revision']='V5诗词版';project['poetry']={'count':24,'style':'楷体诗句+独立小字作者篇名','independent_overlay':True,'audio_unchanged_from_v4':True};project_path.write_text(json.dumps(project,ensure_ascii=False,indent=2),encoding='utf-8')
state_path=root/'production.json';state=json.loads(state_path.read_text(encoding='utf-8'));state.update(stage='motion',updated_at=datetime.now(timezone.utc).isoformat(),next_action='Review left and bottom poetry placements; render V5, verify 24 poems and unchanged approved music.',checks={'poetry_selected':24,'poetry_text_and_attribution_checked':True,'visual_review_completed':False,'human_full_listening_review':False});state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'poems':24,'single_line_short_shots':sum(len(r[2])==1 for r in rows),'audio_sha256':hashlib.sha256((root/'public'/project['audio']['file']).read_bytes()).hexdigest(),'music_unchanged':True},indent=2))
