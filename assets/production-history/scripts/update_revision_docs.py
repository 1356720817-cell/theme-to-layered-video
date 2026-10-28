import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=json.loads((root/'public/project.json').read_text(encoding='utf-8'))
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
(root/'README-使用说明.md').write_text('''# 二十四节气 · 浮光高潮版 V2

108秒，1920×1080，30fps，无旁白。按立春至大寒完整介绍24节气。

本版按用户选定的 Jannik《浮光 (The History)》重新剪辑：取原曲97–205秒连续片段，正文集中在102–198秒的96秒高能段；开头5秒接入主落点，四季各24秒，结尾7秒。没有循环高潮，没有改变歌曲速度。

9个单图层、11个双图层、4个三图层正文镜头。背景和独立前景分开运动，选定重音加入轻微主体回弹；静镜、横移、拉远、上下揭示与短切换交替。时间轴按新镜头时长重算，正常推进不重复使用素材，结尾明确回顾四季。

## 运行

需要 Node.js 24或兼容版本、Python、FFmpeg/ffprobe。Python检查脚本使用 python -I；检查图需要numpy和Pillow。首次安装依赖和浏览器运行文件需要网络。

双击“启动预览.cmd”打开带本版音乐的预览。双击“重新导出.cmd”输出MP4。

    npm ci --cache work/npm-cache
    npm run dev
    npm run lint
    npm run render
    npm run finish

输出：outputs/master-silent.mp4 与 outputs/final.mp4。每次修改后重新执行 render、finish。

## 编辑文件

- src/Film.tsx：独立图层、相机、天气、开头、太阳黄经盘和结尾回顾。
- public/project.json：108秒总时长、音乐、开头词组卡点和章节。
- public/shots.json：每镜起止帧、图层、相机、切换、局部重音帧。
- public/assets.json：44张独立生成图的实际提示词、alpha、来源和镜头归属。source_file仅记录生成时缓存，渲染读取工程内相对路径。
- public/assets/fuguang-jannik-full.mp3：所选歌曲完整来源文件。
- public/assets/fuguang-highlight-108s.m4a：实际合成进本片的108秒AAC音轨。
- music-plan.md、work/music-sync.json：原曲截取位置、实测音乐网格、各镜头的音乐时码、片头和结尾事件。
- script.md、storyboard.md：最终文字和本版实际时间轴。
- hook-review.md：已采用的开头诊断、备选及本版时码。
- work/qc/：本版实际成片的检查与抽帧记录；自动分析不等于完整人工听审。
- work/generated-records/ 与 work/generated-batches/：实际生成记录。

## 素材与音乐身份

图像为AI视觉演绎，表现典型物候；不同地区实际天气、农事并非同日同步发生。主题事实依据见 article.md。

音乐是用户指定的 Jannik《浮光 (The History)》，来源 https://music.163.com/song?id=1394601255 ，并非本项目原创。原曲音频未变速，只做0.78倍增益、35毫秒淡入与2秒淡出；版权归权利人，公开发布或商业授权未核验。

字体使用 Windows 系统 KaiTi、Microsoft YaHei；未分发字体文件。其他系统须有相应合法字体，替换后应重新看布局。
''',encoding='utf-8')
(root/'brief.md').write_text('# 本次修订\n\n用户确认使用Jannik《浮光 (The History)》，优先高潮并重做音乐、画面卡点。\n\nV2：108秒，中文，1920×1080，30fps，无旁白。保留24节气完整顺序和已确认图像，调整镜头时长、标题落点、局部前景动作、四季时间轴与结尾。原V1交付文件保留。\n',encoding='utf-8')
(root/'outline.md').write_text('# 整片方案 V2\n\n108秒，1920×1080，30fps，无旁白。开场5秒；正文96秒，春夏秋冬各24秒；结尾7秒。\n\n主画面保留9个单图层、11个双图层、4个三图层；每镜3或4.5秒，按实测音乐重音组编排。全部正常推进素材保持唯一归属，结尾才允许回用。\n\n音乐原曲97–205秒连续截取，正文对应高潮102–198秒。首个主要落点在视频5秒进入立春，四季交接在5、29、53、77秒。原曲不变速、不循环。\n',encoding='utf-8')
header='# 逐镜节奏与用图 · 浮光 V2\n\n音乐使用Jannik《浮光》，连续截取原曲97–205秒。下表原曲时间包含97秒偏移。\n\n|节气|成片时间(秒)|原曲时间(秒)|主画面层数|相机|切换|文案|\n|---|---:|---:|---:|---|---|---|\n'
for s in shots:
 if s['section']=='main':
  a=s['start']/30;b=s['end']/30
  header+=f"|{s['title']}|{a:.3f}–{b:.3f}|{a+97:.3f}–{b+97:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{s['subtitle']}|\n"
header+='\n开场0–5秒，结尾101–108秒；字幕/标题不跟随画面擦切与模糊。背景连续运镜，局部前景在选定重音独立回弹。\n'
(root/'storyboard.md').write_text(header,encoding='utf-8')
h=(root/'hook-review.md').read_text(encoding='utf-8')
start=h.index('## 实施版本');tail=h.index('事实依据：',start)
h=h[:start]+'''## 实施版本 · 浮光 V2

0–1.00秒：第一句“冰还没化，”。
1.00–2.50秒：第二句“怎么就立春了？”。
2.50–3.50秒：在高潮前短暂停顿中带出“二十四节气”和日历盘。
3.50–5.00秒：旋律拾起时带出“顺着太阳，读懂一年”。
5.00秒：原曲102秒主要低频重音进入立春正片。

画面为独立生成冰面，不复用立春主体。无口播。本版依据实际曲目网格重写时码，不沿用V1的96BPM合成音乐时码。

'''+h[tail:]
(root/'hook-review.md').write_text(h,encoding='utf-8')
print('Updated revision docs and actual storyboard.')
