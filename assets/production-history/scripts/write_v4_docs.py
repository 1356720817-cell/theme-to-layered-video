import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
summary='128秒，1920×1080，30fps，无旁白。Jannik《浮光 (The History)》从原曲1分17秒开始，连续截取至3分25秒，第25秒对应原曲1分42秒主要高潮落点；音量较V3降低约6.02dB。'
(root/'brief.md').write_text('# V4修订\n\n用户最终要求：声音降低，高潮约在25秒，原曲约1分15秒处开始。此前“3秒高潮”的请求已被本次更正取代。\n\n'+summary+'\n\n采用77秒起点，使102秒主要高潮准确落在成片25秒。前段重新分配镜头时长，春分的大地全景在高潮落点进入。V1至V3保留。\n',encoding='utf-8')
(root/'outline.md').write_text('# 整片方案 V4\n\n'+summary+'\n\n开场0–5秒，立春5–11秒，雨水11–17秒，惊蛰17–25秒。25秒春分全景接入高潮。春季44秒，夏秋冬各24秒，章节开始5/49/73/97秒；正文121秒结束，结尾7秒。\n\n9个单图层、11个双图层、4个三图层正文；正常推进不复用素材，结尾明确回顾。音乐不变速、不循环、不跨段拼接。\n',encoding='utf-8')
table='# V4实际分镜与音乐落点\n\n'+summary+'\n\n|节气|成片时间(秒)|原曲时间(秒)|图层|相机|切换|文案|\n|---|---:|---:|---:|---|---|---|\n'
for s in shots:
 if s['section']!='main':continue
 a=s['start']/30;b=s['end']/30
 table+=f"|{s['title']}|{a:.3f}–{b:.3f}|{a+77:.3f}–{b+77:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{s['subtitle']}|\n"
(root/'storyboard.md').write_text(table,encoding='utf-8')
(root/'music-plan.md').write_text('''# 浮光 V4 · 降低音量，25秒高潮

用户最终指令覆盖先前的3秒高潮要求：降低声音，高潮在25秒左右，原曲约1分15秒起。

- 原曲公开来源：https://music.163.com/song?id=1394601255 ，258秒完整MP3随工程保存。
- 从77.000秒（1分17秒，接近用户所说1分15秒）开始，连续到205.000秒，总计128秒。
- 主落点102.000秒减77.000秒起点，等于成片25.000秒，第750帧。春分全景在这个落点直接切入。
- 增益从V3的0.78降为0.39，即-6.0206dB；不再额外做响度提升。保留1.25秒淡入和2秒淡出。
- 前25秒保留原曲有节奏的推进，高潮前22.2–23.4秒附近的编曲留白为原曲结构。
- 第一季镜头6/6/8/7.5/9/7.5秒，后续季节各24秒，按0.5秒实测脉冲定时。只在选定重音让前景回弹。
- 第121秒进入结尾，音乐205秒处对应成片128秒；不变速、不循环、不跨段拼接。

频谱与波形测量用于确定候选网格，最终封装核对音频包哈希和PCM偏移。未做完整人工听审。

音乐版权归权利人；用户指定用于本次本地编辑，公开发布/商业授权未核验。
''',encoding='utf-8')
(root/'README-使用说明.md').write_text('''# 二十四节气 · 浮光 V4

128秒，1920×1080，30fps，无旁白，24节气完整推进。音乐从Jannik《浮光》原曲1分17秒处开始，第25秒进入高潮；整首增益较V3降低约6.02dB。原曲连续截取，不变速、不循环。

0–5秒开场；立春5–11秒，雨水11–17秒，惊蛰17–25秒；第25秒春分全景接高潮。四季章节从5、49、73、97秒开始，121秒进入结尾。独立前景、不同运镜和44张专属图片保留，正常推进没有相同素材复用。

## 预览与导出

需要Node.js 24或兼容版本、Python、FFmpeg/ffprobe。检查图需要numpy、Pillow；首次依赖安装和浏览器运行文件需要网络。

双击“启动预览.cmd”可带音乐编辑，双击“重新导出.cmd”可重新生成MP4。终端命令：

    npm ci --cache work/npm-cache
    npm run dev
    npm run lint
    npm run render
    npm run finish

输出为outputs/master-silent.mp4与outputs/final.mp4。修改JSON或源码后重新render、finish。

## 文件

- src/Film.tsx：分层、相机、局部重音、天气、独立文字和结尾。
- public/project.json：音乐和总时长；public/shots.json：实际时间轴和图层；public/assets.json：完整实际提示词、alpha、镜头归属和来源。
- public/assets/fuguang-jannik-full.mp3：完整曲目；fuguang-25s-drop-128s.m4a：实际合成的128秒音轨。
- music-plan.md、work/music-sync.json：原曲起点与25秒主落点、各镜头实测网格。
- work/audio-level-check.json：与V3相同音乐区间的音量差测量。
- work/qc/、work/audio-offset-check.json：最终解码、音轨、顺序、去重与抽帧检查。未做完整人工听审。
- work/generated-records/与work/generated-batches/：图像实际生成记录；source_file仅为生成时缓存记录，渲染读取工程内相对文件。

图像是AI视觉演绎，表现典型物候；各地天气、农事不在同日同步发生。知识来源见article.md。字体为Windows系统KaiTi和Microsoft YaHei，未分发系统字体文件。

音乐来源：https://music.163.com/song?id=1394601255 。音乐非本项目原创，版权归权利人；用户指定用于本次本地编辑，公开发布/商业授权未核验。
''',encoding='utf-8')
h=(root/'hook-review.md').read_text(encoding='utf-8');a=h.index('## 实施版本');b=h.index('事实依据：',a)
h=h[:a]+'''## 实施版本 · 浮光 V4

片头文字0、1、2.5、3.5秒依次进入，5秒柔和叠化至立春。音乐从原曲77秒开始，25秒（第750帧）对应原曲102秒高潮，配春分全景落点。开头不承载高潮。

整体音乐增益0.39，较V3降低约6.02dB；1.25秒淡入，2秒淡出。标题只显示在所属镜头，叠化尾部只保留图片，避免标题重影。

'''+h[b:];(root/'hook-review.md').write_text(h,encoding='utf-8')
plan_path=root/'work/scene-plan.json';plan=json.loads(plan_path.read_text(encoding='utf-8'));lookup={s.get('index'):s for s in shots if s['section']=='main'}
for row in plan:row[4]=(lookup[row[0]]['end']-lookup[row[0]]['start'])/30
plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('V4 docs updated.')
