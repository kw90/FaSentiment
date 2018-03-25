from __future__ import print_function

__author__ = 'kai'

import time
import requests
import cv2
import operator
import sys
import ConfigParser



def main(arfv):
    config = ConfigParser.RawConfigParser()
    config.read('credentials.cfg')
    #print (os.sys.path)
    cap = cv2.VideoCapture(0)
    test = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
    ratio = cap.get(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO)
    frame_rate = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    brightness = cap.get(cv2.cv.CV_CAP_PROP_BRIGHTNESS)
    contrast = cap.get(cv2.cv.CV_CAP_PROP_CONTRAST)
    saturation = cap.get(cv2.cv.CV_CAP_PROP_SATURATION)
    hue = cap.get(cv2.cv.CV_CAP_PROP_HUE)
    gain = cap.get(cv2.cv.CV_CAP_PROP_GAIN)
    exposure = cap.get(cv2.cv.CV_CAP_PROP_EXPOSURE)
    print("Test: ", test)
    print("Ratio: ", ratio)
    print("Frame Rate: ", frame_rate)
    print("Height: ", height)
    print("Width: ", width)
    print("Brightness: ", brightness)
    print("Contrast: ", contrast)
    print("Saturation: ", saturation)
    print("Hue: ", hue)
    print("Gain: ", gain)
    print("Exposure: ", exposure)

    while(1):
        ret, img = cap.read()
        cv2.imshow("Cam feed", img)
        k = cv2.waitKey(33)
        # Esc
        if k==27:
            break
        # Enter
        elif k==13:
            handleImage(img)
        else:
            print (k)

    cv2.destroyAllWindows()
    cv2.VideoCapture(0).release()


def handleImage(img):
    cv2.imwrite("data.jpg", img)
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None
    params = None

    with open(r'data.jpg', 'rb') as f:
        data = f.read()

    result = processRequest(json, data, headers, params)
    annotateResult(img, result)


def annotateResult(img, result):
    renderResultOnImage(result, img)
    cv2.imshow("Sentiment analysis", img)


def processRequest(json, data, headers, params):
    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json = json, data = data, headers = headers, params = params)

        if response.status_code == 429:

            print ("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print ('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print ("Error code: %d" % response.status_code)
            print ("Message: %s" % (response.json()['error']['message']))

        break

    return result


def renderResultOnImage(result, img):
    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        cv2.rectangle(
            img,
            (faceRectangle['left'], faceRectangle['top']),
            (faceRectangle['left']+faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
            color = (0, 0, 255), thickness = 5)


    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        i = 0
        for emotion in currFace['scores'].items():
            emotionPercentage = "{:.1%}".format(emotion[1])
            textToWrite = emotion[0] + " :  " + str(emotionPercentage)
            cv2.putText(
                img,
                textToWrite,
                (int(faceRectangle['left']+faceRectangle['width']+20), int(faceRectangle['top']+(i*16))),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                1,
                cv2.CV_AA)
            i += 1
        guessedSentiment = 'Your sentiment is ' + max(currFace['scores'].items(), key=operator.itemgetter(1))[0]
        guessedSentimentPercentage = max(currFace['scores'].items(), key=operator.itemgetter(1))[1]
        cv2.putText(
                img,
                "%s" % guessedSentiment + str(" with " + "{:.1%}".format(guessedSentimentPercentage)),
                (faceRectangle['left']+20, int(faceRectangle['top']+faceRectangle['height']+40)),
                cv2.FONT_HERSHEY_DUPLEX,
                0.9,
                (0, 255, 255),
                1,
                cv2.CV_AA)


def __init__(self, name):
    self.name = name

if __name__ == '__main__':
    main(sys.argv)