# Wildfire-Watch
A scalable forest fire prevention framework written in python.

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

## Getting Started
### Conda (Recommended)
```bash
cond env create -f requirements.yml
conda activate WFW
```

### Pip
```bash
pip install -r reqirements.txt
```

### Flags
Wildfire-Watch has five flags a user can define listed as follows
```bash
video - A path to an OpenCV video input, which is set to 0 for a local webcam
capRate - Sets a capture rate. For every specified number of frames, a Google Vision API call will be made
info - determines if detection information will be logged to the console
output - determines if forest fire detections will be saved as individual images
Display - determines if each analyzed frame is displayed, for debugging purposes
```

### Output
You can find the output detection(s) of forest fires showing detections in the detections folder.
Each detection is formatted as follows: FRAMENUMBER_LATITUDE_LONGITUDE.png, where FRAMENUMBER is the current frame number. LATITUDE and LONGITUDE denote the latitude and longitude generated from an IP adress.

## Results

## Developer Notes
All object identification used Google's VISION API.
