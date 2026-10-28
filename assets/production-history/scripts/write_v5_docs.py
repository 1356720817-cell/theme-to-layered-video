import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
shots=json.loads((root/'public/shots.json').read_text(encoding='utf-8'))
summary='V5ʫ�ʰ棺24�������ֱ����һ����ʫ�ʽ�ѡ�����߼�ƪ������Ϊ�����ɱ༭���ֲ㡣128�롢1920��1080��30fps����ȫ����V4��ȷ�ϵ�����������77��ԭ����㡢25��߳�����ʱ����'
(root/'brief.md').write_text('# �����޶�\n\n�û�����������Щ�գ�ϣ��ÿ����������һ���Ӧʫ�ʡ�\n\n'+summary+'\n\n����ͷ��һ����3��̾�ͷֻ��һ�䡣ʫ��������е��룬������ͼ����С�ģ����ǰ���˶���\n',encoding='utf-8')
(root/'outline.md').write_text('# ��Ƭ���� V5\n\n'+summary+'\n\n5�뿪ͷ��24������ԭʱ�����ƽ�������121�������7���β�������汣��9����ͼ�㡢11��˫ͼ�㡢4����ͼ�㾵ͷ�������ƽ��زĲ����ã���β��ȷ�عˡ�\n\nʫ�������հ״���ů��ɫ���壺���澵ͷ����˵���·���ԭ�ײ��Ű�ľ�ͷ�������Ϸ���â��ʫ�������ƣ������Ϸ����ֱ�ǩ��ÿ��0.4�����룬���д���6֡������ƪ������롣\n',encoding='utf-8')
table='# V5�־���ʫ��\n\n|����|ʱ��(��)|ͼ����|���|�л�|ʫ��|������ƪ��|\n|---|---:|---:|---|---|---|---|\n'
for s in shots:
 if s['section']!='main':continue
 p=s['poem'];a=s['start']/30;b=s['end']/30
 table+=f"|{s['title']}|{a:.3f}�C{b:.3f}|{len(s['layers'])}|{s['camera']['type']}|{s['transition']['type']}|{'��'.join(p['lines'])}��|{p['author']}��{p['work']}��|\n"
(root/'storyboard.md').write_text(table,encoding='utf-8')
(root/'README-ʹ��˵��.md').write_text('''# ��ʮ�Ľ��� �� ʫ�ʰ� V5

128�룬1920��1080��30fps�����԰ס�24����������һ������ʫ�����ֲ㼰����ƪ�����ϳ���ͷ��һ����3��̾�ͷֻ��һ�䡣ů������е��룬���˵���·������Ϸ�����λ�ð�����ѡ�񣬲������ײ���������ɼ���

������V4��ȫ��ͬ��Jannik�����⡷ԭ��77�C205������Ƭ�Σ���25�����߳�������0.39����V3��Լ6dB�������о�ͷʱ�����л�ʱ�㱣����

## Ԥ���뵼��

��ҪNode.js 24����ݰ汾��Python��FFmpeg/ffprobe�����ͼ��numpy��Pillow���״ΰ�װ����������������ļ���Ҫ���硣

˫��������Ԥ��.cmd��������Ԥ����˫�������µ���.cmd����������MP4���ն˿����У�

    npm ci --cache work/npm-cache
    npm run dev
    npm run lint
    npm run render
    npm run finish

���Ϊoutputs/master-silent.mp4��outputs/final.mp4���޸����ݻ�Դ�������render��finish��

## �༭�ļ�

- src/Film.tsx��PoetryOverlay����ʫ���Ű�ͷ��н��룻SceneView��ʫ����ڶ�����ǩ�㣬�л�β��������ʫ�䡣
- public/shots.json��ÿ��poem�ֶοɸ�ʫ�䡢���ߡ�ƪ��������֡��λ�ü�����top��
- public/poems.json��poetry-sources.md��24��ʵ�ʽ�ѡ��ԭ�ĳ�����˶����ӣ�����ʹ�÷�Χ˵����
- public/project.json�����֡�ʱ�����½ڣ�public/assets.json��44��ͼ���ʵ����ʾ�ʡ�alpha����Դ�͹�����
- public/assets/fuguang-25s-drop-128s.m4a��ʵ��ʹ�����죻fuguang-jannik-full.mp3��������Դ��Ŀ��
- work/qc/���������ձ�����Ƶ�Ľ��롢�������ϣ������˳��ȥ�غͳ�֡��顣��֡�������鲻���������˹�����
- work/generated-records/��work/generated-batches/��ʵ�����ɼ�¼��source_fileΪ����ʱ������Ϣ����Ⱦֻ������������ļ���

ͼ��ΪAI�Ӿ�������ֵ�����򣻲�ͬ����������ũ�²���ͬ��ͬ��������ʫ���ǹŴ�ʫ��ԭ�Ľ�ѡ��������Ʒ��д��Ӧ���ڣ�����רΪ��Ӧ����������δʹ���ִ����ĺ�������֪ʶ��Դ��article.md��ʫ����Դ��poetry-sources.md��

����ΪWindowsϵͳKaiTi��Microsoft YaHei��δ�ַ������ļ������ְ�Ȩ��Ȩ���ˣ��û�ָ�����ڱ��α��ر༭����������/��ҵ��Ȩδ���顣
''',encoding='utf-8')
print('V5 docs updated.')
