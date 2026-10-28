import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
summary='120秒，1920×1080，30fps，无旁白。采用Jannik《浮光 (The History)》原曲85–205秒连续片段，前17秒自然铺垫，第17秒在“惊蛰”进入高潮。'
(root/'brief.md').write_text('# V3修订\n\n用户反馈：开头太快进入高潮，显得突兀。\n\n'+summary+'\n\n保留原曲的轻段、逐步推进和高潮前停顿；不通过拼接不同乐段制造起伏。立春、雨水的镜头放慢，取消这两镜的重拍回弹，后续保持节气、画面和音乐对齐。V1、V2保留。\n',encoding='utf-8')
(root/'outline.md').write_text('# 整片方案 V3\n\n'+summary+'\n\n0–5秒为开头；5–11秒立春，11–17秒雨水；17秒主落点进入惊蛰。春季36秒，夏秋冬各24秒，章节从5/41/65/89秒开始。正文113秒结束，结尾7秒。\n\n春季各镜6秒，后续3或4.5秒交替。9个单图层、11个双图层、4个三图层正文镜头，正常推进不复用素材，结尾明确回顾。\n',encoding='utf-8')
table='# 逐镜节奏与用图 · V3自然铺垫版\n\n'+summary+'\n\n|节气|成片时间(秒)|原曲时间(秒)|图层数|相机|切换|文案|\n|---|---:|---:|---:|---|---|---|\n'
for s in shots:
 if s['section']!='main':continue
 a=s['start']/30;b=s['end']/30
 table+=f"|{s['title']}|{a:.3f}–{b:.3f}|{a+85:.3f}–{b+85:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{s['subtitle']}|\n"
(root/'storyboard.md').write_text(table,encoding='utf-8')
(root/'README-使用说明.md').write_text('''# 二十四节气 · 浮光自然铺垫版 V3

120秒，1920×1080，30fps，无旁白，完整介绍立春至大寒24节气。

根据用户反馈，音乐由原曲85秒处较轻的段落开始，保留17秒推进；第17秒对应原曲102秒主要高潮落点，切入“惊蛰：蛰伏的生命醒来”。前两个节气取消重拍回弹，镜头各6秒。春季各镜6秒，夏秋冬按3或4.5秒交替。章节从5、41、65、89秒开始，正文113秒结束，结尾7秒。

音乐取原曲85–205秒的连续片段，不变速、不循环、不跨段拼接。淡入1.25秒，淡出2秒，整体增益0.78。源音轨、成片用AAC和测量记录随工程提供。V1、V2交付文件保留。

## 运行与导出

需要Node.js 24或兼容版本、Python、FFmpeg/ffprobe。检查图需numpy和Pillow；首次安装依赖和浏览器运行文件需要网络。

双击“启动预览.cmd”可带音乐编辑预览；双击“重新导出.cmd”可输出成片。终端可运行：

    npm ci --cache work/npm-cache
    npm run dev
    npm run lint
    npm run render
    npm run finish

输出为 outputs/master-silent.mp4 和 outputs/final.mp4。修改JSON或源码后重新render、finish。

## 编辑与核验

- src/Film.tsx：独立图层、相机、局部重音、天气、标题、太阳刻度盘与结尾。
- public/project.json：总时长、音乐和章节；public/shots.json：每镜起止帧、相机、图层与局部重音。
- public/assets.json：44张图像的实际提示词、alpha和镜头归属。source_file仅记录生成时缓存；渲染只读工程内相对文件。
- public/assets/fuguang-jannik-full.mp3：完整歌曲；fuguang-progressive-120s.m4a：实际使用的120秒音轨。
- music-plan.md、work/music-sync.json：实际截取位置、音乐结构与镜头落点。
- storyboard.md、script.md：实际分镜时间与画面文字。
- work/qc/、work/audio-offset-check.json：本版结构、解码、音轨与抽帧核验。自动测量和抽帧不等于全片人工听审。
- work/generated-records/、work/generated-batches/：图像实际生成记录。

图像是AI视觉演绎，表现典型物候；各地天气、农事并非同日同步发生。知识来源见article.md。标题用Windows系统KaiTi，正文用Microsoft YaHei，未分发系统字体文件。

音乐来源：https://music.163.com/song?id=1394601255 。音乐非本项目原创，版权归权利人；用户指定用于本次本地编辑，公开发布/商业授权未核验。
''',encoding='utf-8')
h=(root/'hook-review.md').read_text(encoding='utf-8');a=h.index('## 实施版本');b=h.index('事实依据：',a)
h=h[:a]+'''## 实施版本 · 浮光 V3

0秒第一句，1秒第二句，2.5秒主题，3.5秒副标题。画面5秒柔和叠化进入立春。音乐继续铺垫至17秒，惊蛰时进入主要高潮；开头不再承担高潮爆发。

独立冰面资产、无旁白；初段1.25秒淡入。前17秒的情绪推进来自原曲85–102秒连续编排；切入高潮对应原曲102秒。

'''+h[b:];(root/'hook-review.md').write_text(h,encoding='utf-8')
plan_path=root/'work/scene-plan.json';plan=json.loads(plan_path.read_text(encoding='utf-8'));lookup={s.get('index'):s for s in shots if s['section']=='main'}
for row in plan:row[4]=(lookup[row[0]]['end']-lookup[row[0]]['start'])/30
plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('V3 docs and actual storyboard updated.')
