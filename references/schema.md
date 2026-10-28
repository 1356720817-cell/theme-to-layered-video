# 工程数据约定

starter-remotion读取public里的三个JSON文件。

## project.json

```json
{
  "topic": "本次新主题",
  "status": "draft",
  "width": 1920,
  "height": 1080,
  "fps": 30,
  "durationFrames": 3900,
  "language": "zh-CN",
  "palette": {"dark":"#080a0d","paper":"#e4d8b9","accent":"#e4b264","text":"#f0e5cd","ink":"#25251f"},
  "fonts": {"serif":"KaiTi, SimSun, serif","sans":"Microsoft YaHei, sans-serif"},
  "audio": {"file":"","source":"","rights":"","offsetSeconds":0},
  "chapters": [],
  "beats": []
}
```

时间以真实音轨为准。有配音则用配音与对齐结果确定durationFrames，最后再适当留尾声。默认3900帧只用于无额外约束时的策划目标。改变比例时重新检查布局，不能仅改宽高就宣称竖屏已验收。

## shots.json

数组；start/end均为整数帧，end为不包含的边界，片段连续覆盖0到durationFrames。

```json
{
  "id":"shot-01",
  "start":0,"end":90,
  "section":"opening",
  "chapter":"引入",
  "title":"新主题的标题",
  "subtitle":"本镜头想让观众记住的话",
  "kicker":"可选年代或阶段",
  "theme":"dark",
  "camera":{"type":"still","amount":1},
  "transition":{"type":"cut","frames":0},
  "layers":[{"assetId":"intro-a","role":"background","x":0,"y":0,"w":1,"h":1,"fit":"cover","parallax":1}],
  "words":[{"text":"词组","frame":0,"color":"accent"}]
}
```

section取opening、main、recap、ending。只有recap/ending且显式出现在此前镜头中的素材才允许回顾复用；全新图像也可以出现在结尾。默认每镜正文2–3层信息，不能把大量文字堆在短镜头内。

layers坐标x/y/w/h为相对画面的0–1比例；可用motion={"x0":0,"x1":0.04,"y0":0,"y1":0,"scale0":1,"scale1":1}指定独立位移/尺度。透明图role=foreground时必须是真alpha；相机/前景越界需看帧验证。

生产引擎扩展：motion.sway、layer.shadow/maskBottom、shot.weather/weatherIntensity、accentFrames/accentStrength、layout=bottom、poem、visual=hook-opening/panel-ending。具体字段和适用范围见shot-recipes.md，不再依赖固定index==9或固定24项触发通用效果。黄经盘等主题专用组件保存在案例中。

## assets.json

```json
{"assets":[{
  "id":"intro-a",
  "file":"assets/intro-a.png",
  "ownerShot":"shot-01",
  "entityId":"本次主体",
  "status":"ready",
  "kind":"image",
  "depiction":"generated",
  "source":"image_gen",
  "prompt":"实际调用的完整提示词",
  "rights":"本次生成",
  "alpha":false
}]}
```

同一entityId不代表可复用同一assetId。两次描述同一种物品可以分别用两个不同构图。audit会检查文件内容哈希，不能复制同一文件改名绕过规则。素材文件路径相对public，不能指向技能缓存、工具输出缓存或上次工程。

共同颗粒、统一版式、字幕、时间轴和程序光影是视觉系统，不列入历史主体去重；不要把真实主体图假装标成“纹理”绕过检查。

## production.json

保存stage、topic、completed_shot_ids、pending_shot_ids、audio、checks、next_action。默认音轨offsetSeconds为0；有偏移时实际合成与QC都要使用同一偏移，不把有意偏移误判为比特流不匹配。

确认索引在work/review-ledger.json，逐镜确认在work/shot-approvals.json，实际音乐方案在music-plan.json。文件哈希过期须重核相应范围。交付状态用delivered_pending_acceptance，与用户明确的accepted分开。具体政策见approvals.md。
