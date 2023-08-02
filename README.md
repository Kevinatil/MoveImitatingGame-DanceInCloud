
# Move Imitating Game with Openpose from  *Dance In Cloud*  Team

A game for moves imitating and scoring using scoring process designed by *Dance In Cloud* Team.


## Introduction
This repo provides a game to do move imitating scoring and evaluating to test videos based on standard move videos. You can choose any move video with single person as the standard video.

This version supports *video* scoring. You can choose a ready-made video or record a video in advance as standard video. After choosing the standard video, you can record the test video and do the moves in the standard video as well as you can. the framework will do pose estimation, score regression. The score includes dancing move score and rhythm score. The dancing move score includes total score and detail scores for each joint.

## Environment

The scoring process is based on [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose). Please configure the OpenPose environment before running this framework.

```bash
# After configuring OpenPose, run command to install packages
pip install -r requirements.txt
```

## Demo

The interface and scoring process are shown below. The scoring process is obfuscated by `pyarmor` because of the commercial usage.

![img](https://github.com/Kevinatil/MoveImitatingGame-DanceInCloud/blob/main/media/show.gif)

## Usage

(1) Use ready-made video as standard video

1. Put the target(standard) video into `origin_videos` folder;

2. Open *origin.py*, set `camera` as *False*, and change `namelist` in `main` into the name of the target video(without .mp4);

3. Run *origin.py*, and the rendered video and extracted json files will be generated;

4. (optional) put a thumbnail of the standard video into `origin_pics` folder;

5. Run *imitate.py* after changing the work directory based on your environment;

6. Click *start recording* to record test video, and click *show score* to get the scores of test video;

7. The scoring process can be restarted by clicking input box.

(2) Record the standard video

1. Open *origin.py*, change `namelist` into the name of the video to be recording, or set `namelist` as empty to use default name;

2. Set the `camera` as *True* in *origin.py*;

3. Run *origin.py* to do video recording, and the rendered video and extracted json files will be generated;

4. (optional) put a thumbnail of the standard video into `origin_pics` folder;

5. Run *imitate.py* after changing the work directory based on your environment;

6. Click *start recording* to record test video, and click *show score* to get the scores of test video;

7. The scoring process can be restarted by clicking input box.

## Quick start

You can watch a scoring demo by setting the `pose` under `if camera` branch as *False* in the `photo_score` function in `imitate.py` . The scoring function will use cached json files to do scoring.

```python
def photo_score(ns,camera=True,pose=False,del_all=True,duration=3):
    pose_obj=OpenPoseVideo()
    origin_video_path=rootpath+'origin_videos/'
    origin_json_path=rootpath+'origin_jsons/'+ns+'/'
    imitate_video_path=rootpath+'imitate_videos/'+ns+'/'
    imitate_json_path=rootpath+'imitate_jsons/'+ns+'/'
    if camera:
        if del_all:
            del_file(imitate_video_path[:-1])
            del_file(imitate_json_path[:-1])
        video_capture(origin_name=ns,duration=int(duration+0.5))
        pose=True # set as False to use cached json files to do scoring
    if pose:
        pose_obj.openposedemo_json(input_video = imitate_video_path, 
                                   output_json = imitate_json_path)
    return calculate_score.score_print(ns, 
                                       origin_json_path, 
                                       imitate_json_path)
```
