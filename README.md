# Game Data Generator

This repository can be used as a tool to extract information from frames of any game which can otherwise not be used for research purpose.

Steps:

+ Acquire a video of the game (make sure resolution of this video is the same as that of actual gameplay)
+ Find the coordinates of region of interests (ROIs) using [utils](utils)
+ Use the generated `key_info.log` actual gameplay video as input for `main.py` to extract values written in ROI

These extracted values for example can be used as reward values for training any model.

```
python3 main.py --video_path game.mp4 --key_info ./key_info.log --model Model/model.pyt
```

## TODO

+ Data collector to fine tune neural network for any given game
+ Add information about hacks to control game in order to automate keyboard inputs
