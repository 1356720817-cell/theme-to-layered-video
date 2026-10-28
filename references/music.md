# 音乐实际制作

使用当前项目已可用、用户提供或经核验的音乐。没有选曲时先研究/提出少量适合的候选；网络查询按可用检索能力进行，不假称热度或流行度。没有音乐时可以继续研究/视觉样片，用临时音轨必须标临时，未经确认不做昂贵全片最终渲染。不要自动把程序生成的基础节奏当作最终配乐。

## 连续选段工具
```text
python -I scripts/prepare_music.py <工程> --source public/assets/full-song.mp3 --start 77 --duration 128 --gain-db -8.18 --fade-in 1.25 --fade-out 2 --climax-source 102 --output public/assets/music-approved-candidate.m4a
```
以上是本案例的参数演示，下一主题重新确定。工具拒绝超出源时长、非有限数字、过长淡变和未授权覆盖，生成M4A和独立recipe JSON。它不会自动改project.json、记为已确认或自动证明音乐授权。先查看实际峰值/响度、检查淡变，再将实际audio.file指向候选，audio.copy=true、offsetSeconds=0，更新music-plan.json。

music-plan.json至少写song/artist/version/source_url/source_file/source_sha256/excerpt_start_seconds/excerpt_end_seconds/gain_db/fade_in_seconds/fade_out_seconds/climax_source_seconds/climax_video_seconds/rights_status/preview_file。拼接/变速使用segments数组，记录speed、source_in/out、video_in/out、join方式；本工具不支持拼接，另行编辑后导出单个混音母带。

实际剪辑和增益已烘焙到母带，导出时不要重复应用metadata中的gain。音量数值需结合目标平台、旁白和用户实际试听确定，不把本案例0.39增益写成通用最佳值。

## 验证
试听前测实际输入响度、真峰值与RMS，测量工具不改音频。参数中的分析目标不是所有视频都必须达到的交付标准：
```text
python -I scripts/measure_audio.py --file public/assets/music-approved-candidate.m4a --output work/music-levels.json
```
同段降幅比较要分别指定对应start/seconds，不比较两版不同内容的整片平均。真峰值过零、削波或过响需要修复并重出具体试听，不能靠匹配哈希掩盖。

```text
python -I scripts/verify_audio.py <工程> --video outputs/final.mp4
```
比较工程中真实母带与最终文件，复制轨用压缩音频包哈希，转码轨用解码后波形相关性和增益比；工具写出范围和阈值。它不证明音乐好听、卡点自然或用户已经试听。先完成所有音频混合再锁定母带，避免用“只比较BGM”去检查含旁白的新混音。
