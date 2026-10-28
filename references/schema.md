# ��������Լ��

starter-remotion��ȡpublic�������JSON�ļ���

## project.json

```json
{
  "topic": "����������",
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

ʱ������ʵ����Ϊ׼�����������������������ȷ��durationFrames��������ʵ���β����Ĭ��3900ֻ֡�����޶���Լ��ʱ�Ĳ߻�Ŀ�ꡣ�ı����ʱ���¼�鲼�֣����ܽ��Ŀ��߾��������������ա�

## shots.json

���飻start/end��Ϊ����֡��endΪ�������ı߽磬Ƭ����������0��durationFrames��

```json
{
  "id":"shot-01",
  "start":0,"end":90,
  "section":"opening",
  "chapter":"����",
  "title":"������ı���",
  "subtitle":"����ͷ���ù��ڼ�ס�Ļ�",
  "kicker":"��ѡ�����׶�",
  "theme":"dark",
  "camera":{"type":"still","amount":1},
  "transition":{"type":"cut","frames":0},
  "layers":[{"assetId":"intro-a","role":"background","x":0,"y":0,"w":1,"h":1,"fit":"cover","parallax":1}],
  "words":[{"text":"����","frame":0,"color":"accent"}]
}
```

sectionȡopening��main��recap��ending��ֻ��recap/ending����ʽ�����ڴ�ǰ��ͷ�е��زĲ������ع˸��ã�ȫ��ͼ��Ҳ���Գ����ڽ�β��Ĭ��ÿ������2�C3����Ϣ�����ܰѴ������ֶ��ڶ̾�ͷ�ڡ�

layers����x/y/w/hΪ��Ի����0�C1����������motion={"x0":0,"x1":0.04,"y0":0,"y1":0,"scale0":1,"scale1":1}ָ������λ��/�߶ȡ�͸��ͼrole=foregroundʱ��������alpha�����/ǰ��Խ���迴֡��֤��

����������չ��motion.sway��layer.shadow/maskBottom��shot.weather/weatherIntensity��accentFrames/accentStrength��layout=bottom��poem��visual=hook-opening/panel-ending�������ֶκ����÷�Χ��shot-recipes.md�����������̶�index==9��̶�24���ͨ��Ч�����ƾ��̵�����ר����������ڰ����С�

## assets.json

```json
{"assets":[{
  "id":"intro-a",
  "file":"assets/intro-a.png",
  "ownerShot":"shot-01",
  "entityId":"��������",
  "status":"ready",
  "kind":"image",
  "depiction":"generated",
  "source":"image_gen",
  "prompt":"ʵ�ʵ��õ�������ʾ��",
  "rights":"��������",
  "alpha":false
}]}
```

ͬһentityId�������ɸ���ͬһassetId����������ͬһ����Ʒ���Էֱ���������ͬ��ͼ��audit�����ļ����ݹ�ϣ�����ܸ���ͬһ�ļ������ƹ������ز��ļ�·�����public������ָ���ܻ��桢�������������ϴι��̡�

��ͬ������ͳһ��ʽ����Ļ��ʱ����ͳ����Ӱ���Ӿ�ϵͳ����������ʷ����ȥ�أ���Ҫ����ʵ����ͼ��װ��ɡ��������ƹ���顣

## production.json

����stage��topic��completed_shot_ids��pending_shot_ids��audio��checks��next_action��Ĭ������offsetSecondsΪ0����ƫ��ʱʵ�ʺϳ���QC��Ҫʹ��ͬһƫ�ƣ���������ƫ������Ϊ��������ƥ�䡣

ȷ��������work/review-ledger.json����ȷ����work/shot-approvals.json��ʵ�����ַ�����music-plan.json���ļ���ϣ�������غ���Ӧ��Χ������״̬��delivered_pending_acceptance�����û���ȷ��accepted�ֿ����������߼�approvals.md��
