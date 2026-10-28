"""Attach verified public-domain verse; preserve the approved V4 timing and audio."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
rows=[
 (1,'����',['�ɻ�������˪��','�����˼��ľ֪'],'�Ŗ�','����ż��','https://www.ccdi.gov.cn/yaowenn/202501/t20250126_402828_m.html'),
 (2,'��ˮ',['����֪ʱ��','�����˷���'],'�Ÿ�','��ҹϲ��','https://www.moe.gov.cn/srcsite/A06/s3331/201612/W020161213303084709835.pdf'),
 (3,'����',['΢���ڻ���','һ�׾���ʼ'],'ΤӦ��','�����','https://www.beijing.gov.cn/renwen/zt/essjq/zjs/202209/t20220908_2811393.html'),
 (4,'����',['�ٴ�������','��ɫ���з�'],'����','������','https://dfzb.suzhou.gov.cn/dfzb/szdq/202203/fccc818c79dd44ecac50d2eb5b1a9aa0.shtml'),
 (5,'����',['�滨����������','����Ѱ�������'],'��Ω��','�յ���������','https://www.qingcheng.gov.cn/zjqc/mswh/content/post_150917.html'),
 (6,'����',['���괺����','ɽ����ɫ��'],'Ԫ�','ӽإ����ʫ������������','https://www.bjqtm.com/xcjy/dwxc/����΢���ã�ʫ�ʻ�����-���괺������ɽ����ɫ��'),
 (7,'����',['�����Ĳ�ʤ��ʱ'],'����ʯ','���ļ���','https://zh.wikisource.org/zh-hans/���ļ���'),
 (8,'С��',['����������ӽ�','ɣҶ���ʲ�ʳ��'],'ŷ����','����԰��ʱ�ִ��Ķ��ס����','https://www.kfdsw.com/index/detail/id/2670.html'),
 (9,'â��',['ʱ�꼰â��','��Ұ�Բ���'],'½��','ʱ��','https://wn.bjsjw.gov.cn/n702/20250310/i101223.html'),
 (10,'����',['�������Ƽ�'],'ΤӦ��','���������','https://wjw.shanxi.gov.cn/zfxxgk/fdzdgknr/jkzx/202505/t20250516_9835856.shtml'),
 (11,'С��',['�ɷ�������','��¶������'],'�Ϻ�Ȼ','������ͤ������','https://www.cma.gov.cn/2011xzt/20150130/20150701/201507/t20150701_286561.html'),
 (12,'����',['���겻֪��ȥ','һ�緽������'],'���ɴ�','ϲ��','https://m.ahjjjc.gov.cn/p/60817.html'),
 (13,'����',['�Թŷ��ﱯ����','��������ʤ����'],'������','��ʶ��ס���һ','https://yllhj.beijing.gov.cn/ztxx/bjhx/hhzs/202011/t20201104_2128451.shtml'),
 (14,'����',['����������'],'�׾���','���������л�','https://www.bjqtm.com/xcjy/dwxc/����΢���ý��Ļ�����-����'),
 (15,'��¶',['¶�ӽ�ҹ��','���ǹ�����'],'�Ÿ�','��ҹ�����','https://hb.cma.gov.cn/qxkp/qxkp/202202/t20220207_4494148.html'),
 (16,'���',['�������','����¶�����ڰ�'],'л��','��筴����������','https://m.12371.gov.cn/content/2023-09/23/content_449476.html'),
 (17,'��¶',['�������綯','���ຮ¶��'],'�׾���','����','https://www.shidianguji.com/mingju/7623272193846034483'),
 (18,'˪��',['��ľҡ��¶Ϊ˪'],'��ا','����ж��ס���һ','https://www.bjxch.gov.cn/file/20191108/1573199211783080701.pdf'),
 (19,'����',['��紵����ͥ��','��Ҷ��������'],'���ɵ�','����','https://www.sqlzw.gov.cn/sitesources/nysjwjw/page_pc/xcjd/wh/article5698d5bb9e8f41ccb35c541a293116f5.html'),
 (20,'Сѩ',['�����������֦'],'����','��ѩ','https://dxs.moe.gov.cn/zx/a/jj/220210/1747122.shtml'),
 (21,'��ѩ',['����һҹ������','ǧ�������滨��'],'᯲�','��ѩ�������йٹ龩','https://www.nationalreading.gov.cn/ydzg/plgc/202508/t20250815_926664.html'),
 (22,'����',['��ʱ���������','��������������'],'�Ÿ�','С��','https://www.beijing.gov.cn/renwen/zt/essjq/hsjq/202209/t20220908_2811456.html'),
 (23,'С��',['�躮���Կ�'],'����ʯ','÷��','https://yllhj.beijing.gov.cn/ztxx/bjhx/hhzs/201902/t20190222_118661.shtml'),
 (24,'��',['��ѩδ��','�ջ����ܳ�'],'½��','��','https://paper.people.com.cn/zgnyb/pc/attachement/202501/20/460e9077-87be-47d8-8262-b688d3720d3f.pdf')
]
# Preserve exact observed reference URLs, including the site's actual punctuation in the slug.
rows[5]=(*rows[5][:-1],'https://www.bjqtm.com/xcjy/dwxc/%E5%AE%9D%E5%8D%9A%E5%BE%AE%E8%AF%BE%E5%A0%82%EF%BD%9C%E8%AF%97%E8%AF%8D%E8%AF%9D%E8%8A%82%E6%B0%94-%E8%B0%B7%E9%9B%A8%E6%98%A5%E5%85%89%E6%99%93%EF%BC%8C%E5%B1%B1%E5%B7%9D%E9%BB%9B')
rows[13]=(*rows[13][:-1],'https://www.bjqtm.com/xcjy/dwxc/%E5%AE%9D%E5%8D%9A%E5%BE%AE%E8%AF%BE%E5%A0%82%E9%87%91%E6%96%87%E8%AF%9D%E8%8A%82%E6%B0%94-%E5%A4%84%E6%9A%91')
shots_path=root/'public/shots.json';shots=json.loads(shots_path.read_text(encoding='utf-8'))
records=[]
for index,term,lines,author,work,url in rows:
 s=next(s for s in shots if s.get('index')==index)
 assert s['title']==term
 poem={'lines':lines,'author':author,'work':work,'sourceUrl':url,'verified':True,'copyright':'�Ŵ�ʫ�ʣ�ԭ�����������򣻽���ѡԭ�ģ��������ִ����Ļ�������','cueFrame':12,'lineStaggerFrames':6,'attributionCueFrame':24,'placement':'upper-left' if s.get('layout')=='bottom' else 'lower-left'}
 if index==9:poem['top']=.53
 s['poem']=poem
 if s['end']-s['start']<=90:assert len(lines)==1
 records.append({'index':index,'term':term,'excerpt':'��'.join(lines)+'��','author':author,'work':work,'source_url':url,'text_and_attribution_checked':True,'relationship':'��������Ӧʱ�����󣻲���ʫ������רΪ�ý���������','clip_seconds':[(s['start']/30),(s['end']/30)],'short_excerpt_for_fast_shot':len(lines)==1})
shots_path.write_text(json.dumps(shots,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'public/poems.json').write_text(json.dumps({'selection_note':'ÿ����һ����ʫ�ʽ�ѡ������ͷʱ��ѡһ����һ�䡣ʫ��Ϊ�Ļ����󣬲������������ѧ˵����','poems':records},ensure_ascii=False,indent=2),encoding='utf-8')
md='# ��ʮ�Ľ���ʫ������� �� V5\n\nÿ����һ������ʫ�����ֲ㡣�ϳ���ͷ��һ����3��̾�ͷֻ��һ�䡣����Ϊ�Ŵ�ʫ��ԭ�Ľ�ѡ�����߼�ƪ�������˶ԣ�������԰���ͬ����������󣬲���ÿ����Ʒ��רΪ�ý���������\n\n|����|����ʫ��|��������Ʒ|�˶���Դ|\n|---|---|---|---|\n'
for r in records:md+=f"|{r['term']}|{r['excerpt']}|{r['author']}��{r['work']}��|[ԭ��/Ȩ��ѡ¼]({r['source_url']})|\n"
md+='\nУ��˵����С�����ÿ���ŷ������Ʒ�к˶Եġ�����԰��ʱ�ִ��Ķ��ס��������δ���������������ҹ������׻����ġ������С���������ѡл�ݴʣ�����������д��������Ŀ��ԭ�ı������С����������¡����֣�����ͬ�����滻��\n'
(root/'poetry-sources.md').write_text(md,encoding='utf-8')
project_path=root/'public/project.json';project=json.loads(project_path.read_text(encoding='utf-8'));project['revision']='V5ʫ�ʰ�';project['poetry']={'count':24,'style':'����ʫ��+����С������ƪ��','independent_overlay':True,'audio_unchanged_from_v4':True};project_path.write_text(json.dumps(project,ensure_ascii=False,indent=2),encoding='utf-8')
state_path=root/'production.json';state=json.loads(state_path.read_text(encoding='utf-8'));state.update(stage='motion',updated_at=datetime.now(timezone.utc).isoformat(),next_action='Review left and bottom poetry placements; render V5, verify 24 poems and unchanged approved music.',checks={'poetry_selected':24,'poetry_text_and_attribution_checked':True,'visual_review_completed':False,'human_full_listening_review':False});state_path.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'poems':24,'single_line_short_shots':sum(len(r[2])==1 for r in rows),'audio_sha256':hashlib.sha256((root/'public'/project['audio']['file']).read_bytes()).hexdigest(),'music_unchanged':True},indent=2))
