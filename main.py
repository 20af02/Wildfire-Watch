import os, io, cv2, requests
from google.cloud import vision
#from google.cloud.vision import types
from absl import app
import numpy as np

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"

client = vision.ImageAnnotatorClient()

def main(_argv):
    cap = cv2.VideoCapture('video/WF.mp4')

    frameNum = 0
    capRate = 100
    #Main capture loop
    while True:
        #Get frame
        ret, frame = cap.read()
        #every 150 frames
        if frameNum % capRate == 0:

            #Get geolocation
            ipRequest = requests.get('https://get.geojs.io/v1/ip.json')
            geoRequest = requests.get('https://get.geojs.io/v1/ip/geo/' + ipRequest.json()['ip'] + '.json')
            geoData = geoRequest.json()

            #store capture
            cv2.imwrite('./tmp.png', frame)

            #Use Vision API
            with io.open('./tmp.png', 'rb') as imageFile:
                content = imageFile.read()
            image = vision.Image(content=content)
            
            #Perform label detection
            response = client.label_detection(image=image)
            lables  = response.label_annotations

           # print('Lables:')
            for label in lables:
                #If a wildfire is detected
                if label.description == "Wildfire":
                    if label.score > 0.60:
                        vertices = ([(vertex.x, vertex.y)
                                    for vertex in label.bounding_poly.vertices])

                        print("Fire Detected on frame# " + str(frameNum) + "\nScore: " + str(label.score) + "\n@ " + str(geoData['latitude']) +', '+ str(geoData['longitude']) + "\n")
                        cv2.imwrite('./detections/frame_' + str(frameNum) +'_'+str(geoData['latitude']) +', '+ str(geoData['longitude']) + ".png", frame)
        
            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                        response.error.message))
      
        frameNum  = frameNum +1

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass