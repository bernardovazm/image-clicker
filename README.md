# Image clicker

## About

Image clicker is a script that clicks on the center of any images it finds on the screen.

![Image Clicker](.github/preview.gif)

## How to use

In this repository, go to [releases](https://github.com/bernardovazm/image-clicker/releases), download and execute image-clicker.exe file. By default, put a screenshot of anything you want to click inside image folder. Hold esc to stop execution.

You can create a config.json file in the same folder of image-clicker.exe and set some custom values. The default ones are:

```json
{
  "images_path": "images",
  "key_quit": "esc",
  "file_extensions": [".png", ".jpg"],
  "should_return_position": false,
  "grayscale": true,
  "duration": 0.1
}
```

Note: PyAutoGUI is used to locate images, and this might take some time for each image depending on main monitor resolution and computer. Taken from [documentation](https://pyautogui.readthedocs.io/en/latest/screenshot.html#the-screenshot-function):

> On a 1920 x 1080 screen, the locate function calls take about 1 or 2 seconds. This may be too slow for action video games, but works for most purposes and applications.

## Modules used

The following modules were used:

- PyAutoGUI
- OS
- Keyboard
- Datetime
- JSON

Build generated with PyInstaller.

## To do

- [x] Config file
- [x] Custom vars
- [ ] Set % of confidence
- [ ] CLI
- [ ] GUI
