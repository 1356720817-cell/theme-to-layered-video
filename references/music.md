# ����ʵ������

ʹ�õ�ǰ��Ŀ�ѿ��á��û��ṩ�򾭺�������֡�û��ѡ��ʱ���о�/��������ʺϵĺ�ѡ�������ѯ�����ü����������У����ٳ��ȶȻ����жȡ�û������ʱ���Լ����о�/�Ӿ���Ƭ������ʱ����������ʱ��δ��ȷ�ϲ�������ȫƬ������Ⱦ����Ҫ�Զ��ѳ������ɵĻ������൱���������֡�

## ����ѡ�ι���
```text
python -I scripts/prepare_music.py <����> --source public/assets/full-song.mp3 --start 77 --duration 128 --gain-db -8.18 --fade-in 1.25 --fade-out 2 --climax-source 102 --output public/assets/music-approved-candidate.m4a
```
�����Ǳ������Ĳ�����ʾ����һ��������ȷ�������߾ܾ�����Դʱ�������������֡����������δ��Ȩ���ǣ�����M4A�Ͷ���recipe JSON���������Զ���project.json����Ϊ��ȷ�ϻ��Զ�֤��������Ȩ���Ȳ鿴ʵ�ʷ�ֵ/��ȡ���鵭�䣬�ٽ�ʵ��audio.fileָ���ѡ��audio.copy=true��offsetSeconds=0������music-plan.json��

music-plan.json����дsong/artist/version/source_url/source_file/source_sha256/excerpt_start_seconds/excerpt_end_seconds/gain_db/fade_in_seconds/fade_out_seconds/climax_source_seconds/climax_video_seconds/rights_status/preview_file��ƴ��/����ʹ��segments���飬��¼speed��source_in/out��video_in/out��join��ʽ�������߲�֧��ƴ�ӣ����б༭�󵼳���������ĸ����

ʵ�ʼ����������Ѻ決��ĸ��������ʱ��Ҫ�ظ�Ӧ��metadata�е�gain��������ֵ����Ŀ��ƽ̨���԰׺��û�ʵ������ȷ�������ѱ�����0.39����д��ͨ�����ֵ��

## ��֤
����ǰ��ʵ��������ȡ����ֵ��RMS���������߲�����Ƶ�������еķ���Ŀ�겻��������Ƶ������ﵽ�Ľ�����׼��
```text
python -I scripts/measure_audio.py --file public/assets/music-approved-candidate.m4a --output work/music-levels.json
```
ͬ�ν����Ƚ�Ҫ�ֱ�ָ����Ӧstart/seconds�����Ƚ����治ͬ���ݵ���Ƭƽ�������ֵ���㡢�����������Ҫ�޸����س��������������ܿ�ƥ���ϣ�ڸǡ�

```text
python -I scripts/verify_audio.py <����> --video outputs/final.mp4
```
�ȽϹ�������ʵĸ���������ļ������ƹ���ѹ����Ƶ����ϣ��ת����ý����������Ժ�����ȣ�����д����Χ����ֵ������֤�����ֺ�����������Ȼ���û��Ѿ������������������Ƶ���������ĸ���������á�ֻ�Ƚ�BGM��ȥ��麬�԰׵��»�����
