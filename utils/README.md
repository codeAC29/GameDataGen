# Create Boxes Around Areas of Interest

Before being able to extract values such as: Health, Armor, Bullet, etc.
user needs to tell where exactly these informations are located in a sample scene.
These regions are region of interest (ROI) for us.

Steps:
+ Select a `ROI` using mouse
+ A popup will appear after mouse-release where you need to enter keyword for the ROI
+ After clicking `OK`, the selected area will get highlighted by a bounding-box
+ Keep on repeating the above steps until you have covered all ROIs
+ Once you are done, press `c` to exit

`key_info.log` file will be generated as a result of the above steps.
This file will contain `keywords` and their corresponding coordinates.

```
python3 get_key_cors.py -i /video.mp4 -s ./
```
