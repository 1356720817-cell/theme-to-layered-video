import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
summary='128�룬1920��1080��30fps�����԰ס�Jannik������ (The History)����ԭ��1��17�뿪ʼ��������ȡ��3��25�룬��25���Ӧԭ��1��42����Ҫ�߳���㣻������V3����Լ6.02dB��'
(root/'brief.md').write_text('# V4�޶�\n\n�û�����Ҫ���������ͣ��߳�Լ��25�룬ԭ��Լ1��15�봦��ʼ����ǰ��3��߳����������ѱ����θ���ȡ����\n\n'+summary+'\n\n����77����㣬ʹ102����Ҫ�߳�׼ȷ���ڳ�Ƭ25�롣ǰ�����·��侵ͷʱ�������ֵĴ��ȫ���ڸ߳������롣V1��V3������\n',encoding='utf-8')
(root/'outline.md').write_text('# ��Ƭ���� V4\n\n'+summary+'\n\n����0�C5�룬����5�C11�룬��ˮ11�C17�룬����17�C25�롣25�봺��ȫ������߳�������44�룬���ﶬ��24�룬�½ڿ�ʼ5/49/73/97�룻����121���������β7�롣\n\n9����ͼ�㡢11��˫ͼ�㡢4����ͼ�����ģ������ƽ��������زģ���β��ȷ�عˡ����ֲ����١���ѭ���������ƴ�ӡ�\n',encoding='utf-8')
table='# V4ʵ�ʷ־����������\n\n'+summary+'\n\n|����|��Ƭʱ��(��)|ԭ��ʱ��(��)|ͼ��|���|�л�|�İ�|\n|---|---:|---:|---:|---|---|---|\n'
for s in shots:
 if s['section']!='main':continue
 a=s['start']/30;b=s['end']/30
 table+=f"|{s['title']}|{a:.3f}�C{b:.3f}|{a+77:.3f}�C{b+77:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{s['subtitle']}|\n"
(root/'storyboard.md').write_text(table,encoding='utf-8')
(root/'music-plan.md').write_text('''# ���� V4 �� ����������25��߳�

�û�����ָ�����ǰ��3��߳�Ҫ�󣺽����������߳���25�����ң�ԭ��Լ1��15����

- ԭ��������Դ��https://music.163.com/song?id=1394601255 ��258������MP3�湤�̱��档
- ��77.000�루1��17�룬�ӽ��û���˵1��15�룩��ʼ��������205.000�룬�ܼ�128�롣
- �����102.000���77.000����㣬���ڳ�Ƭ25.000�룬��750֡������ȫ����������ֱ�����롣
- �����V3��0.78��Ϊ0.39����-6.0206dB�����ٶ������������������1.25�뵭���2�뵭����
- ǰ25�뱣��ԭ���н�����ƽ����߳�ǰ22.2�C23.4�븽���ı�������Ϊԭ���ṹ��
- ��һ����ͷ6/6/8/7.5/9/7.5�룬�������ڸ�24�룬��0.5��ʵ�����嶨ʱ��ֻ��ѡ��������ǰ���ص���
- ��121������β������205�봦��Ӧ��Ƭ128�룻�����١���ѭ���������ƴ�ӡ�

Ƶ���벨�β�������ȷ����ѡ�������շ�װ�˶���Ƶ����ϣ��PCMƫ�ơ�δ�������˹�����

���ְ�Ȩ��Ȩ���ˣ��û�ָ�����ڱ��α��ر༭����������/��ҵ��Ȩδ���顣
''',encoding='utf-8')
(root/'README-ʹ��˵��.md').write_text('''# ��ʮ�Ľ��� �� ���� V4

128�룬1920��1080��30fps�����԰ף�24���������ƽ������ִ�Jannik�����⡷ԭ��1��17�봦��ʼ����25�����߳������������V3����Լ6.02dB��ԭ��������ȡ�������١���ѭ����

0�C5�뿪��������5�C11�룬��ˮ11�C17�룬����17�C25�룻��25�봺��ȫ���Ӹ߳����ļ��½ڴ�5��49��73��97�뿪ʼ��121������β������ǰ������ͬ�˾���44��ר��ͼƬ�����������ƽ�û����ͬ�زĸ��á�

## Ԥ���뵼��

��ҪNode.js 24����ݰ汾��Python��FFmpeg/ffprobe�����ͼ��Ҫnumpy��Pillow���״�������װ������������ļ���Ҫ���硣

˫��������Ԥ��.cmd���ɴ����ֱ༭��˫�������µ���.cmd������������MP4���ն����

    npm ci --cache work/npm-cache
    npm run dev
    npm run lint
    npm run render
    npm run finish

���Ϊoutputs/master-silent.mp4��outputs/final.mp4���޸�JSON��Դ�������render��finish��

## �ļ�

- src/Film.tsx���ֲ㡢������ֲ��������������������ֺͽ�β��
- public/project.json�����ֺ���ʱ����public/shots.json��ʵ��ʱ�����ͼ�㣻public/assets.json������ʵ����ʾ�ʡ�alpha����ͷ��������Դ��
- public/assets/fuguang-jannik-full.mp3��������Ŀ��fuguang-25s-drop-128s.m4a��ʵ�ʺϳɵ�128�����졣
- music-plan.md��work/music-sync.json��ԭ�������25������㡢����ͷʵ������
- work/audio-level-check.json����V3��ͬ��������������������
- work/qc/��work/audio-offset-check.json�����ս��롢���졢˳��ȥ�����֡��顣δ�������˹�����
- work/generated-records/��work/generated-batches/��ͼ��ʵ�����ɼ�¼��source_file��Ϊ����ʱ�����¼����Ⱦ��ȡ����������ļ���

ͼ����AI�Ӿ�������ֵ�����򣻸���������ũ�²���ͬ��ͬ��������֪ʶ��Դ��article.md������ΪWindowsϵͳKaiTi��Microsoft YaHei��δ�ַ�ϵͳ�����ļ���

������Դ��https://music.163.com/song?id=1394601255 �����ַǱ���Ŀԭ������Ȩ��Ȩ���ˣ��û�ָ�����ڱ��α��ر༭����������/��ҵ��Ȩδ���顣
''',encoding='utf-8')
h=(root/'hook-review.md').read_text(encoding='utf-8');a=h.index('## ʵʩ�汾');b=h.index('��ʵ���ݣ�',a)
h=h[:a]+'''## ʵʩ�汾 �� ���� V4

Ƭͷ����0��1��2.5��3.5�����ν��룬5����͵��������������ִ�ԭ��77�뿪ʼ��25�루��750֡����Ӧԭ��102��߳����䴺��ȫ����㡣��ͷ�����ظ߳���

������������0.39����V3����Լ6.02dB��1.25�뵭�룬2�뵭��������ֻ��ʾ��������ͷ������β��ֻ����ͼƬ�����������Ӱ��

'''+h[b:];(root/'hook-review.md').write_text(h,encoding='utf-8')
plan_path=root/'work/scene-plan.json';plan=json.loads(plan_path.read_text(encoding='utf-8'));lookup={s.get('index'):s for s in shots if s['section']=='main'}
for row in plan:row[4]=(lookup[row[0]]['end']-lookup[row[0]]['start'])/30
plan_path.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print('V4 docs updated.')
