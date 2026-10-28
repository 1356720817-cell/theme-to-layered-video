---
name: theme-to-layered-video
description: 将主题或参考短片制作成高质感分层叙事视频，包含资料与文案、配乐试听确认、专属图像、多样运镜、音乐卡点、验收证据和可编辑交付；支持继续修订与按要求制作封面。不用于仅提取文案。
metadata:
  workflow_version: "2.0"
---

# 主题分层叙事视频

使用已验证的制作方法完成本次新主题，保留用户已作决定和明确授权。默认中文、16:9、1920×1080/30fps、策划约130秒、音乐驱动无新增口播；用户要求覆盖默认值。时长在真实音轨确定后锁定，不能机械沿用旧时间轴。

## 开始与恢复
- 首次使用或需复现这次质量时，先完整查看 [参考分析](references/reference-analysis.md) 所列的完整原片和128秒成片视觉标尺，并读 [详细执行规程](references/detailed-production.md)。标尺缺失时运行 scripts/prepare_benchmark.py 下载并校验；下载不可用则记录缺口，不声称已观看。逐镜实际参数和完整提示词在assets/benchmarks/shot-cards.json和assets/solar-terms-case，不得只看本入口后直接套旧简化模板。
- 生图前读 [视觉规格](references/visual-bible.md)，动画前读 [镜头配方](references/shot-recipes.md)。新默认starter来自本次生产引擎：支持轻摆、选择性重音、雨雪雾、独立引文层、可配置hook和分屏结尾。题材专属图表仍须按本次内容实现，不承诺模板自动画出任何结构。
- 先读 [制作流程](references/production.md)。新建用 init_project.py；已有工程先读 production.json、review-ledger 和实际交付记录，恢复当前阶段，避免重复生图或重新询问已确认选项。
- 用 [确认与修订](references/approvals.md) 建立本任务确认政策。默认音乐试听、代表动效样片需用户确认，其他阶段自主审阅推进；用户要求逐镜/脚本/风格确认时照做，明确委托时沿用委托。不要照搬案例的全部审批次数。
- 主题、研究、脚本、实体、素材、配乐、绝对时码和封面每次独立决定；可以复用工程与检查工具，不继承旧主题内容。
- 所有主体/字体/音频进入当前工程，不能只引用旧聊天、缓存或临时URL。缺工具/文件如实处理，不生成假结果。

## 制作与确认
1. 内容：建立 brief、article/script、outline、sources，核验陌生实体、物候、年代、结构和引文。实拍、原迹、摹本和生成演绎明确区分。按要求提交文案；没有要求时自主完成。
2. 分镜：按 [数据约定](references/schema.md) 逐镜规划信息、资产归属、1/2/3层配置和运动目的。正常推进不复用相同主体图；同一实体再次出现也换新构图。只有显式recap/ending可回顾复用，改名/镜像/裁切不算新图。
3. 视觉锚点：先做难主体细节、真分层遮挡和复杂连续切换样片。实际输出尺寸看细节、真实alpha、光照/尺度和边缘；通过后扩展全片。用户要求每镜确认时，整批整理可审核材料并绑定逐镜版本。
4. 音乐：读 [音乐制作](references/music.md)。先明确具体曲目/版本，再生成带实际选段、音量与淡变的试听和有声预览；预览必须覆盖高潮前后的上下文。用户确认具体版本后记录原话及哈希，才锁定全片音乐节奏。临时轨不当正式配乐，不自动将程序基础节奏升级为成片音乐。用户指定不代表公开/商用授权已核验。
5. 图像：用可用内置image_gen，一种独立资产一次调用；保留原图、实际提示词、来源、alpha和ownerShot。古籍/原迹/科学结构优先可核验素材，粗糙主体不能用缩放和粒子掩盖。
6. 动画：读 [运镜与卡点](references/motion.md)。前景与背景独立运动，单/双/三层和静镜依内容混用；不要全片同向推近。持续性主体不能意外中断。文字与图像切换分离，尾部关旧标签，无年代重影、文字被擦切或黑闪。
7. 卡点：在实际最终音轨上确定cue帧。自动谱峰仅作候选，结合波形/实际预览核验。高潮不必从第0秒开始。换音乐、选段、速度或时长后重算；音量更改比较同一音乐区间。
8. 预览：提交/审阅开头5秒、高潮前后、复杂分层/章节转换和结尾；按确认政策继续。已确认音轨下只改画面/诗词时保持声音并核验一致，避免重开音乐选择。
9. 最终制作：运行 audit、lint/TypeScript 与render gate，再正式渲染合成。按 [验收矩阵](references/acceptance.md) 和 [媒体QC](references/quality.md) 绑定当前输入与最终MP4，进行全解码、每镜/边界抽帧、音轨比对和真实视觉复核。机器通过不是美术/听审通过。
10. 封面（需要时）：确认标题/人物/具体参考；已有决定直接沿用。每个要求的比例独立构图、检查字与缩略图可读性。用户否定风格后从其喜欢的真实画面修订，不再反复询问已知选项。
11. 交付：MP4、有声预览、可编辑ZIP、素材/提示词/来源、音轨方案与确认记录、逐镜运镜、QC范围和重导出入口；保留旧版。状态先写delivered_pending_acceptance，用户明确认可对应版本后才写accepted。没有完整听审或重导出验证就明确未做，不补造证据。

## 工具入口
```text
python -I <技能目录>/scripts/init_project.py --topic "新主题" --output <新工程目录>
python -I scripts/production_gate.py record . --gate music --actor user --statement "<真实确认原话>" --source-ref "<消息定位>" --file music-plan.json --file work/music-preview.mp4
python -I scripts/production_gate.py check . --stage render
npm run render
npm run finish
python -I scripts/verify_media.py . --video outputs/final.mp4
python -I scripts/verify_audio.py . --video outputs/final.mp4
python -I scripts/production_gate.py check . --stage deliver --video outputs/final.mp4
```

先读确认规则，不把上方命令当作可填写假原话的模板。gate负责证据是否存在/过期，不认证身份、不代替主观判断。Node使用锁定依赖；FFmpeg/ffprobe用于音频处理和媒体检查。工具通过不保证零问题，必须说明实际验证范围。

需要理解本流程的真实失败和音乐修改链时，读 [二十四节气案例](references/solar-terms-case.md)；需要回归验证时运行 scripts/test_workflow.py，测试只生成隔离的合成夹具，不使用商业音轨或付费生图。

需要追溯这次具体实现而非一般规则时，读assets/production-history/CONTEXT.md，再按问题查看历史脚本/实际生成记录。它们保留案例硬编码且仅供参考，不是新主题的执行入口。完整操作规程、素材规格和真实引擎不能被一份摘要替代。
