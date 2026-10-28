import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=json.loads((root/'public/project.json').read_text(encoding='utf-8'))
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
(root/'README-ʹ��˵��.md').write_text('''# ��ʮ�Ľ��� �� ����߳��� V2

108�룬1920��1080��30fps�����԰ס�������������������24������

���水�û�ѡ���� Jannik������ (The History)�����¼�����ȡԭ��97�C205������Ƭ�Σ����ļ�����102�C198���96����ܶΣ���ͷ5���������㣬�ļ���24�룬��β7�롣û��ѭ���߳���û�иı�����ٶȡ�

9����ͼ�㡢11��˫ͼ�㡢4����ͼ�����ľ�ͷ�������Ͷ���ǰ���ֿ��˶���ѡ������������΢����ص������������ơ���Զ�����½�ʾ����л����档ʱ���ᰴ�¾�ͷʱ�����㣬�����ƽ����ظ�ʹ���زģ���β��ȷ�ع��ļ���

## ����

��Ҫ Node.js 24����ݰ汾��Python��FFmpeg/ffprobe��Python���ű�ʹ�� python -I�����ͼ��Ҫnumpy��Pillow���״ΰ�װ����������������ļ���Ҫ���硣

˫��������Ԥ��.cmd���򿪴��������ֵ�Ԥ����˫�������µ���.cmd�����MP4��

    npm ci --cache work/npm-cache
    npm run dev
    npm run lint
    npm run render
    npm run finish

�����outputs/master-silent.mp4 �� outputs/final.mp4��ÿ���޸ĺ�����ִ�� render��finish��

## �༭�ļ�

- src/Film.tsx������ͼ�㡢�������������ͷ��̫���ƾ��̺ͽ�β�عˡ�
- public/project.json��108����ʱ�������֡���ͷ���鿨����½ڡ�
- public/shots.json��ÿ����ֹ֡��ͼ�㡢������л����ֲ�����֡��
- public/assets.json��44�Ŷ�������ͼ��ʵ����ʾ�ʡ�alpha����Դ�;�ͷ������source_file����¼����ʱ���棬��Ⱦ��ȡ���������·����
- public/assets/fuguang-jannik-full.mp3����ѡ����������Դ�ļ���
- public/assets/fuguang-highlight-108s.m4a��ʵ�ʺϳɽ���Ƭ��108��AAC���졣
- music-plan.md��work/music-sync.json��ԭ����ȡλ�á�ʵ���������񡢸���ͷ������ʱ�롢Ƭͷ�ͽ�β�¼���
- script.md��storyboard.md���������ֺͱ���ʵ��ʱ���ᡣ
- hook-review.md���Ѳ��õĿ�ͷ��ϡ���ѡ������ʱ�롣
- work/qc/������ʵ�ʳ�Ƭ�ļ�����֡��¼���Զ����������������˹�����
- work/generated-records/ �� work/generated-batches/��ʵ�����ɼ�¼��

## �ز�����������

ͼ��ΪAI�Ӿ�������ֵ�����򣻲�ͬ����ʵ��������ũ�²���ͬ��ͬ��������������ʵ���ݼ� article.md��

�������û�ָ���� Jannik������ (The History)������Դ https://music.163.com/song?id=1394601255 �����Ǳ���Ŀԭ����ԭ����Ƶδ���٣�ֻ��0.78�����桢35���뵭����2�뵭������Ȩ��Ȩ���ˣ�������������ҵ��Ȩδ���顣

����ʹ�� Windows ϵͳ KaiTi��Microsoft YaHei��δ�ַ������ļ�������ϵͳ������Ӧ�Ϸ����壬�滻��Ӧ���¿����֡�
''',encoding='utf-8')
(root/'brief.md').write_text('# �����޶�\n\n�û�ȷ��ʹ��Jannik������ (The History)�������ȸ߳����������֡����濨�㡣\n\nV2��108�룬���ģ�1920��1080��30fps�����԰ס�����24��������˳�����ȷ��ͼ�񣬵�����ͷʱ����������㡢�ֲ�ǰ���������ļ�ʱ�������β��ԭV1�����ļ�������\n',encoding='utf-8')
(root/'outline.md').write_text('# ��Ƭ���� V2\n\n108�룬1920��1080��30fps�����԰ס�����5�룻����96�룬�����ﶬ��24�룻��β7�롣\n\n�����汣��9����ͼ�㡢11��˫ͼ�㡢4����ͼ�㣻ÿ��3��4.5�룬��ʵ��������������š�ȫ�������ƽ��زı���Ψһ��������β���������á�\n\n����ԭ��97�C205��������ȡ�����Ķ�Ӧ�߳�102�C198�롣�׸���Ҫ�������Ƶ5������������ļ�������5��29��53��77�롣ԭ�������١���ѭ����\n',encoding='utf-8')
header='# �𾵽�������ͼ �� ���� V2\n\n����ʹ��Jannik�����⡷��������ȡԭ��97�C205�롣�±�ԭ��ʱ�����97��ƫ�ơ�\n\n|����|��Ƭʱ��(��)|ԭ��ʱ��(��)|���������|���|�л�|�İ�|\n|---|---:|---:|---:|---|---|---|\n'
for s in shots:
 if s['section']=='main':
  a=s['start']/30;b=s['end']/30
  header+=f"|{s['title']}|{a:.3f}�C{b:.3f}|{a+97:.3f}�C{b+97:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{s['subtitle']}|\n"
header+='\n����0�C5�룬��β101�C108�룻��Ļ/���ⲻ���滭�������ģ�������������˾����ֲ�ǰ����ѡ�����������ص���\n'
(root/'storyboard.md').write_text(header,encoding='utf-8')
h=(root/'hook-review.md').read_text(encoding='utf-8')
start=h.index('## ʵʩ�汾');tail=h.index('��ʵ���ݣ�',start)
h=h[:start]+'''## ʵʩ�汾 �� ���� V2

0�C1.00�룺��һ�䡰����û��������
1.00�C2.50�룺�ڶ��䡰��ô�������ˣ�����
2.50�C3.50�룺�ڸ߳�ǰ����ͣ���д�������ʮ�Ľ������������̡�
3.50�C5.00�룺����ʰ��ʱ������˳��̫��������һ�ꡱ��
5.00�룺ԭ��102����Ҫ��Ƶ��������������Ƭ��

����Ϊ�������ɱ��棬�������������塣�޿ڲ�����������ʵ����Ŀ������дʱ�룬������V1��96BPM�ϳ�����ʱ�롣

'''+h[tail:]
(root/'hook-review.md').write_text(h,encoding='utf-8')
print('Updated revision docs and actual storyboard.')
