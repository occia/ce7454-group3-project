# Import required modules
import cv2 as cv
import time
import argparse
from src.preprocess.face_detection.face_utils import getFaces

parser = argparse.ArgumentParser(description='Use this script to run age and gender recognition using OpenCV.')
parser.add_argument('--input', help='Path to input image or video file. Skip this argument to capture frames from a camera.')

args = parser.parse_args()

faces = getFaces(args.input)
if faces == 0:
    print('no face detected')

cv.imwrite('testimg.jpg', faces[0])