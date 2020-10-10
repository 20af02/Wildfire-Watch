import os, io, cv2, requests
from google.cloud import vision
from absl import app, flags
from absl.flags import FLAGS
import numpy as np

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"

client = vision.ImageAnnotatorClient()

flags.DEFINE_string('video', './video/WF.mp4', 'path to input video, set to 0 for webcam')
flags.DEFINE_integer('capRate', 100, 'every amount of frames to send an API call')
flags.DEFINE_boolean('info', True, 'print info on detections')
flags.DEFINE_boolean('output', True, 'write image detections')
flags.DEFINE_boolean('Display', True, 'Display individual frames')


def main(_argv):
    cap = cv2.VideoCapture(FLAGS.video)

    frameNum = 0
    #Main capture loop
    while True:
        #Get frame
        ret, frame = cap.read()

        if not ret:
            print('Video has ended or failed')
            break

        cv2.namedWindow("Current Frame", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("Current Frame", frame)

        #every 150 frames
        if frameNum % FLAGS.capRate == 0:

            #Get geolocation
            ipRequest = requests.get('https://get.geojs.io/v1/ip.json')
            geoRequest = requests.get('https://get.geojs.io/v1/ip/geo/' + ipRequest.json()['ip'] + '.json')
            geoData = geoRequest.json()

            #store capture
            cv2.imwrite('./tmp.png', frame)

            #Use Vision API to get predictions
            with io.open('./tmp.png', 'rb') as imageFile:
                content = imageFile.read()
            image = vision.Image(content=content)
            
            #Perform label detection
            response = client.label_detection(image=image)
            lables  = response.label_annotations

           # Find wildfires
            for label in lables:
                #If a wildfire is detected
                if label.description == "Wildfire":
                    if label.score > 0.60:
  #                      geoData['latitude'] = 28.117929
  #                      geoData['longitude'] = -80.672204
                        if FLAGS.info:
                            print("Fire Detected on frame# " + str(frameNum) + "\nScore: " + str(label.score) + "\n@ " + str(geoData['latitude']) +', '+ str(geoData['longitude']) + "\n")
                        if FLAGS.output:
                            cv2.imwrite('./detections/frame_' + str(frameNum) +'_'+str(geoData['latitude']) +'_'+ str(geoData['longitude']) + ".png", frame)
        
            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                        response.error.message))
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        frameNum  += 1

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass