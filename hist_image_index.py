#!/usr/bin/python

import argparse
import cv2
import sys
import os
import re
import cPickle as pickle

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
ap.add_argument('-imgdir', '--imgdir', required = True, help = 'image directory')
ap.add_argument('-hist', '--hist', required = True, help = 'histogram index file')
ap.add_argument('-bin', '--bin', required=True, help='histogram bin size')
ap.add_argument('-clr', '--clr', required=True, help='color space')
args = vars(ap.parse_args())

HIST_INDEX = {}

def hist_index_img(imgp, color_space, bin_size=8):
  global HIST_INDEX

  


  cv2.calcHist(cv2.open(imgp), channels, mask, histSize, ranges)


  pass

def hist_index_img_dir(imgdir, color_space, bin_size):
  for path, dirlist, filelist in os.walk(roordir):
    for file_name in fnmatch.filter(filelist, r'.+/.(jpg|png|JPG)'):
     yield hist_index_img(os.path.join(path, file_name),color_space, bin_size)
  pass

if __name__ == '__main__':
  hist_index_img_dir(args['imgdir'], args['clr'], int(args['bin']))
  with open(args['hist'], 'wb') as histpick:
    pickle.dump(HIST_INDEX, histpick)
  print('indexing finished')


