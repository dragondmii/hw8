#!/usr/bin/python

import argparse
import cv2
import sys
import os
import re
import cPickle as pickle
from matplotlib import pyplot as plt

################################
# module: hist_image_index.py
# author:  Robert Epstein and A01092594
# description: persistent image histogram indexer
# to run:
#
# $ python hist_image_index.py -imgdir images/ -clr rgb -hist rgb_hist16.pck -bin 16
# $ python hist_image_index.py -imgdir images/ -clr hsv -hist hsv_hist16.pck -bin 16
#
# the output will look as follows:
# ...
# indexing images/16_07_02_14_50_48_orig.png
# images/16_07_02_14_50_48_orig.png indexed
# images/16_07_02_14_37_38_orig.png
# images/16_07_02_14_37_38_orig.png indexed
# images/123473019.JPG
# images/123473019.JPG indexed
# indexing finished
#
# when indexing is finished, the persisted index object is
# saved in rgb_hist16.pck and hst_hist16.pck
################################

ap = argparse.ArgumentParser()
ap.add_argument('-imgdir', '--imgdir', required = False, help = 'image directory')
ap.add_argument('-hist', '--hist', required = False, help = 'histogram index file')
ap.add_argument('-bin', '--bin', required=False, help='histogram bin size')
ap.add_argument('-clr', '--clr', required=False, help='color space')
args = vars(ap.parse_args())

HIST_INDEX = {}

def hist_index_img(imgp, color_space, bin_size=8):
  global HIST_INDEX

  image = cv2.imread(imgp)
  
  bin_size_list = [bin_size,bin_size,bin_size]

  if color_space == 'rgb':
#    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_hist = cv2.calcHist([image],[0,1,2],None, bin_size_list, [0,256,0,256,0,256])
  
  if color_space == 'hsv':
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    img_hist = cv2.calcHist(hsv,[0,1,2],None, bin_size_list, [0,180,0,256,0,256])
  
  norm_hist = cv2.normalize(img_hist, img_hist).flatten()
#  print norm_hist, '\n'
  HIST_INDEX[imgp]=norm_hist
  print str(imgp)
#  print(HIST_INDEX[imgp]), '\n'
  pass

def hist_index_img_dir(imgdir, color_space, bin_size):
  for imgp in gen_imgp(imgdir):
    hist_index_img(imgp, color_space, bin_size)
  pass


def gen_imgp(imgdir):
  for path, dirlist, filelist in os.walk(imgdir):
    for file_name in filelist:
      yield os.path.join(path, file_name)
  pass

def mass_build():
  imgdir = 'images/'

  clr_val = 'rgb'

  hist_index_img_dir(imgdir, clr_val, 8)
  with open('rgb_hist8.pck', 'wb') as histpick:
    pickle.dump(HIST_INDEX, histpick)
  print('indexing finished-rgb8')

  HIST_INDEX.clear()
  hist_index_img_dir(imgdir, clr_val, 16)
  with open('rgb_hist16.pck', 'wb') as histpick:
    pickle.dump(HIST_INDEX, histpick)
  print('indexing finished-rgb16')

  clr_val = 'hsv'

  HIST_INDEX.clear()
  hist_index_img_dir(imgdir, clr_val, 8)
  with open('hsv_hist8.pck', 'wb') as histpick:
    pickle.dump(HIST_INDEX, histpick)
  print('indexing finished-hsv8')

  HIST_INDEX.clear()  
  hist_index_img_dir(imgdir, clr_val, 16)
  with open('hsv_hist16.pck', 'wb') as histpick:
    pickle.dump(HIST_INDEX, histpick)
  print('indexing finished-hsv16')



if __name__ == '__main__':
#  hist_index_img_dir(args['imgdir'], args['clr'], int(args['bin']))
#  with open(args['hist'], 'wb') as histpick:
#    pickle.dump(HIST_INDEX, histpick)
#  print('indexing finished')

  mass_build()
  print ('shit got done')











#  image = cv2.imread('car_test/img12.png')
#  rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#  cv2.imshow('rgb',rgb)
#  cv2.imshow('bgr',image)

#  fig1 = plt.figure(1)
#  fig1.suptitle('Image')
#  img_hist = cv2.calcHist([rgb],[0,1,2],None, [8,8,8], [0,256,0,256,0,256])
#  plt.xlim([0,256])
#  plt.xlabel('Bins')
#  plt.ylabel('P')
#  plt.subplot(311)
#  plt.plot(img_hist, color='r')
#  cv2.waitKey(0)
