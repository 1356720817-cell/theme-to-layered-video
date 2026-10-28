import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
summary='V5诗词版：24个节气分别加入一处古诗词节选、作者及篇名，作为独立可编辑文字层。128秒、1920×1080、30fps；完全保留V4已确认的音乐音量、77秒原曲起点、25秒高潮和逐镜时长。'
(root/'brief.md').write_text('# 本次修订\n\n用户反馈画面有些空，希望每个节气增加一句对应诗词。\n\n'+summary+'\n\n长镜头用一联，3秒短镜头只用一句。诗句独立分行淡入，不跟随图像擦切、模糊或前景运动。\n',encoding='utf-8')
(root/'outline.md').write_text('# 整片方案 V5\n\n'+summary+'\n\n5秒开头；24节气按原时间轴推进，正文121秒结束，7秒结尾。主画面保留9个单图层、11个双图层、4个三图层镜头。正常推进素材不复用，结尾明确回顾。\n\n诗句在左侧空白处用暖金色楷体：常规镜头置于说明下方，原底部排版的镜头置于左上方；芒种诗句略上移，避让南方夏种标签。每句0.4秒后进入，分行错开6帧，作者篇名随后淡入。\n',encoding='utf-8')
table='# V5分镜与诗词\n\n|节气|时间(秒)|图层数|相机|切换|诗句|作者与篇名|\n|---|---:|---:|---|---|---|---|\n'
for s in shots:
 if s['section']!='main':continue
 p=s['poem'];a=s['start']/30;b=s['end']/30
 table+=f"|{s['title']}|{a:.3f}–{b:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{'，'.join(p['lines'])}。|{p['author']}《{p['work']}》|\n"
(root/'storyboard.md').write_text(table,encoding='utf-8')
(root/'README-使用说明.md').write_text('''# 二十四节气 · 诗词版 V5

128秒，1920×1080，30fps，无旁白。24节气各加入一处独立诗词文字层及作者篇名；较长镜头用一联，3秒短镜头只用一句。暖金楷体分行淡入，左侧说明下方与左上方两种位置按画面选择，补充留白并保留主体可见。

音乐与V4完全相同：Jannik《浮光》原曲77–205秒连续片段，第25秒进入高潮，增益0.39（比V3低约6dB）。所有镜头时长和切换时点保留。

## 预览与导出

需要Node.js 24或兼容版本、Python、FFmpeg/ffprobe。检查图需numpy和Pillow。首次安装依赖及浏览器运行文件需要网络。

双击“启动预览.cmd”带音乐预览，双击“重新导出.cmd”重新生成MP4。终端可运行：

    npm ci --cache work/npm-cache
    npm run dev
    npm run lint
    npm run render
    npm run finish

输出为outputs/master-silent.mp4和outputs/final.mp4。修改数据或源码后重新render、finish。

## 编辑文件

- src/Film.tsx：PoetryOverlay控制诗句排版和分行进入；SceneView把诗句放在独立标签层，切换尾部不残留诗句。
- public/shots.json：每镜poem字段可改诗句、作者、篇名、进入帧、位置及单独top。
- public/poems.json、poetry-sources.md：24条实际节选、原文出处与核对链接，包含使用范围说明。
- public/project.json：音乐、时长和章节；public/assets.json：44张图像的实际提示词、alpha、来源和归属。
- public/assets/fuguang-25s-drop-128s.m4a：实际使用音轨；fuguang-jannik-full.mp3：完整来源曲目。
- work/qc/：本版最终编码视频的解码、音轨包哈希、节气顺序、去重和抽帧检查。抽帧与机器检查不等于完整人工听审。
- work/generated-records/和work/generated-batches/：实际生成记录；source_file为生成时缓存信息，渲染只读工程内相对文件。

图像为AI视觉演绎，表现典型物候；不同地区天气、农事并不同日同步发生。诗句是古代诗词原文节选，部分作品描写相应季节，并非专为对应节气而作；未使用现代译文和赏析。知识来源见article.md，诗句来源见poetry-sources.md。

字体为Windows系统KaiTi、Microsoft YaHei，未分发字体文件。音乐版权归权利人，用户指定用于本次本地编辑，公开发布/商业授权未核验。
''',encoding='utf-8')
print('V5 docs updated.')
