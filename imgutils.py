#!/usr/bin/env python

'''
imgutils.py:
    Helper functions for Opencv
'''
from skimage.measure import compare_ssim
import imutils
import cv2

import utils


def im_diff(imageA, imageB):
    '''return the diff index [-1, 1] between 2 imgs'''
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    # utils.log('INFO', "SSIM: {}".format(score))
    return score
