import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
summary='120�룬1920��1080��30fps�����԰ס�����Jannik������ (The History)��ԭ��85�C205������Ƭ�Σ�ǰ17����Ȼ�̵棬��17���ڡ����ݡ�����߳���'
(root/'brief.md').write_text('# V3�޶�\n\n�û���������ͷ̫�����߳����Ե�ͻأ��\n\n'+summary+'\n\n����ԭ������Ρ����ƽ��͸߳�ǰͣ�٣���ͨ��ƴ�Ӳ�ͬ�ֶ������������������ˮ�ľ�ͷ������ȡ�������������Ļص����������ֽ�������������ֶ��롣V1��V2������\n',encoding='utf-8')
(root/'outline.md').write_text('# ��Ƭ���� V3\n\n'+summary+'\n\n0�C5��Ϊ��ͷ��5�C11��������11�C17����ˮ��17���������뾪�ݡ�����36�룬���ﶬ��24�룬�½ڴ�5/41/65/89�뿪ʼ������113���������β7�롣\n\n��������6�룬����3��4.5�뽻�档9����ͼ�㡢11��˫ͼ�㡢4����ͼ�����ľ�ͷ�������ƽ��������زģ���β��ȷ�عˡ�\n',encoding='utf-8')
table='# �𾵽�������ͼ �� V3��Ȼ�̵��\n\n'+summary+'\n\n|����|��Ƭʱ��(��)|ԭ��ʱ��(��)|ͼ����|���|�л�|�İ�|\n|---|---:|---:|---:|---|---|---|\n'
for s in shots:
 if s['section']!='main':continue
 a=s['start']/30;b=s['end']/30
 table+=f"|{s['title']}|{a:.3f}�C{b:.3f}|{a+85:.3f}�C{b+85:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{s['subtitle']}|\n"
(root/'storyboard.md').write_text(table,encoding='utf-8')
(root/'README-ʹ��˵��.md').write_text('''# ��ʮ�Ľ��� �� ������Ȼ�̵�� V3

120�룬1920��1080��30fps�����԰ף�����������������24������

�����û�������������ԭ��85�봦����Ķ��俪ʼ������17���ƽ�����17���Ӧԭ��102����Ҫ�߳���㣬���롰���ݣ��ݷ���������������ǰ��������ȡ�����Ļص�����ͷ��6�롣��������6�룬���ﶬ��3��4.5�뽻�档�½ڴ�5��41��65��89�뿪ʼ������113���������β7�롣

����ȡԭ��85�C205�������Ƭ�Σ������١���ѭ���������ƴ�ӡ�����1.25�룬����2�룬��������0.78��Դ���졢��Ƭ��AAC�Ͳ�����¼�湤���ṩ��V1��V2�����ļ�������

## �����뵼��

��ҪNode.js 24����ݰ汾��Python��FFmpeg/ffprobe�����ͼ��numpy��Pillow���״ΰ�װ����������������ļ���Ҫ���硣

˫��������Ԥ��.cmd���ɴ����ֱ༭Ԥ����˫�������µ���.cmd���������Ƭ���ն˿����У�

    npm ci --cache work/npm-cache
    npm run dev
    npm run lint
    npm run render
    npm run finish

���Ϊ outputs/master-silent.mp4 �� outputs/final.mp4���޸�JSON��Դ�������render��finish��

## �༭�����

- src/Film.tsx������ͼ�㡢������ֲ����������������⡢̫���̶������β��
- public/project.json����ʱ�������ֺ��½ڣ�public/shots.json��ÿ����ֹ֡�������ͼ����ֲ�������
- public/assets.json��44��ͼ���ʵ����ʾ�ʡ�alpha�;�ͷ������source_file����¼����ʱ���棻��Ⱦֻ������������ļ���
- public/assets/fuguang-jannik-full.mp3������������fuguang-progressive-120s.m4a��ʵ��ʹ�õ�120�����졣
- music-plan.md��work/music-sync.json��ʵ�ʽ�ȡλ�á����ֽṹ�뾵ͷ��㡣
- storyboard.md��script.md��ʵ�ʷ־�ʱ���뻭�����֡�
- work/qc/��work/audio-offset-check.json������ṹ�����롢�������֡���顣�Զ������ͳ�֡������ȫƬ�˹�����
- work/generated-records/��work/generated-batches/��ͼ��ʵ�����ɼ�¼��

ͼ����AI�Ӿ�������ֵ�����򣻸���������ũ�²���ͬ��ͬ��������֪ʶ��Դ��article.md��������WindowsϵͳKaiTi��������Microsoft YaHei��δ�ַ�ϵͳ�����ļ���

������Դ��https://music.163.com/song?id=1394601255 �����ַǱ���Ŀԭ������Ȩ��Ȩ���ˣ��û�ָ�����ڱ��α��ر༭����������/��ҵ��Ȩδ���顣
''',encoding='utf-8')
h=(root/'hook-review.md').read_text(encoding='utf-8');a=h.index('## ʵʩ�汾');b=h.index('��ʵ���ݣ�',a)
h=h[:a]+'''## ʵʩ�汾 �� ���� V3

0���һ�䣬1��ڶ��䣬2.5�����⣬3.5�븱���⡣����5����͵����������������ּ����̵���17�룬����ʱ������Ҫ�߳�����ͷ���ٳе��߳�������

���������ʲ������԰ף�����1.25�뵭�롣ǰ17��������ƽ�����ԭ��85�C102���������ţ�����߳���Ӧԭ��102�롣

'''+h[b:];(root/'hook-review.md').write_text(h,encoding='utf-8')
plan_path=root/'work/scene-plan.json';plan=json.loads(plan_path.read_text(encoding='utf-8'));lookup={s.get('index'):s for s in shots if s['section']=='main'}
for row in plan:row[4]=(lookup[row[0]]['end']-lookup[row[0]]['start'])/30
plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('V3 docs and actual storyboard updated.')
