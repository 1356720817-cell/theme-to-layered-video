# 完整参考片如何变成制作规格

## 必看材料
开始新主题前，不只看封面或几张截图。至少完整查看：
- assets/benchmarks/original-reference-full-130s.mp4：130秒完整原片，原始视频与单独保存的音轨已合成。
- assets/benchmarks/solar-terms-finished-visual-full-128s.mp4：本次128秒完整视觉标尺；首次使用若文件缺失，运行 python -I <技能目录>/scripts/prepare_benchmark.py 从公开仓库下载三段，逐段校验并重组，再校验完整文件SHA-256。该标尺静音。
- assets/benchmarks/reference-index.json：原片与成片标尺的哈希、来源、下载位置及用途；新主题配乐重新选择。
- assets/benchmarks/final-review-*.jpg 与 boundaries-*.jpg：正文与切换取样。
- assets/solar-terms-case：本次完整可编辑视觉案例，44张图、原始提示词、实际26镜头、实际生产渲染器。自带明确标注的静音母带，不把《浮光》当默认音乐分发。

本机原音参考不存在时，不能假称已听完；可先分析完整视觉，再取得本任务允许使用的音乐。视觉标尺不能代替本次配乐确认。

## 三次观看，每次有明确产物
### 第一遍：整体情绪与叙事
完整看起承转合，记录hook、段落、节奏转折、高潮、情绪留白、结尾。写reference-summary.md：哪些是制作机制可迁移，哪些是原主题专属事实。不要把24节气、59历史镜头、火焰或25秒高潮变成新主题的固定参数。

### 第二遍：逐镜结构
运行 inspect_reference.py 作候选取样，再人工核对切镜点。每镜记录：
reference_in/out、段落目的、景别、视觉主体、画面留白、相机方向、图层推断及置信度、独立运动、文字位置/字号/进入时间、过渡类型/帧数、持续对象、光影、音乐cue依据。
图层数量只能根据遮挡/相对运动推断，参考视频不能直接证明原作者源工程结构。标“推断2–3层”，不能写成已知源层数。

### 第三遍：重点运动与声画
开头0–5秒、明显重音前后、长镜、最复杂分层、所有转场风格、结尾必须连续看。截图看不出实际运动，播放不具备条件时保留缺口，不填写“已播放”。有音频时实际试听来源文件；拍点、波形和情绪变化分别记录。
持续火焰的例子：检查画面上火源始终存在、大小/亮度按具体重音变化、转场中未意外消失。新主题可迁移“持续生命体/水流/光”机制，但不能无理由搬火焰。

## 最终产物：reference-map.json
每个新镜头写参考机制和差异：
- source_reference、reference_time_range、mechanism；
- new_shot_id、new_subject、new_layer_plan、camera、transition；
- typography、music_cue、continuity_obligation；
- verification：actual_viewed/frames_only/inferred/not_reviewed。
没有参考支持且有意原创的镜头写original_design，不强造对应关系。

## 看标尺时重点区分
本案例植物、天气、地貌用自然摄影细节；文明器物更重材料/结构、原迹和展陈。两者共同有准确主体、真alpha、逐镜方向、独立排版、实际音轨，但不是相同画风。不得用“国风”“电影感”两个形容词代替上述明确规格。


