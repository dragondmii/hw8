#!/usr/bin/python

import argparse
import cv2
import sys
import os
import cPickle as pickle
from matplotlib import pyplot as plt
#import matplotlib.pyplot
from os.path import basename

################################
# module: hist_image_retrieval.py
# author:  Robert Epstein and A01092594
# description: persistent image retriever
# to run:
# $ python hist_image_retrieval.py -ip horfood_test/img01.JPG -hist hsv_hist16.pck -bin 16 -sim bhatta
#
# the output should print the matches for the top 3 images and display the input image
# and the top 3 matches in 4 matplotlib figures.
# images/123472793.JPG --> 0.914982328755
# images/123465243.JPG --> 0.921478476016
# images/123465992.JPG --> 0.923478808005
#################################

ap = argparse.ArgumentParser()
ap.add_argument('-ip', '--imgpath', required = True, help = 'image path')
ap.add_argument('-hist', '--hist', required = True, help = 'hist index file')
ap.add_argument('-bin', '--bin', required = True, help = 'hist bin size')
ap.add_argument('-sim', '--sim', required = True, help = 'hist similarity')
ap.add_argument('-clr', '--clr', required = False, help = 'color space')
args = vars(ap.parse_args())

inimg = cv2.imread(args['imgpath'])
bin_size = int(args['bin'])
# compute the histogram of inimg and save it in inhist
inimg = cv2.cvtColor(inimg, cv2.COLOR_BGR2RGB)
inhist = cv2.calcHist([inimg],[0,1,2], None, [bin_size,bin_size,bin_size],[0,256,0,256,0,256])
# normalize and flatten the inhist into a feature vector
inhist_vec = cv2.normalize(inhist,inhist).flatten()

# get the similarity metric string from the command line parameter.
hist_sim = args['sim']

HIST_INDEX = None

def hist_correl_sim(norm_hist1, norm_hist2):
  # compute correlation similarity b/w normalized and flattened histograms
  return cv2.compareHist(norm_hist1, norm_hist2, cv2.HISTCMP_CORREL)

def hist_chisqr_sim(norm_hist1, norm_hist2):
  # compute chi square similarity b/w normalized and flattened histograms
  return cv2.compareHist(norm_hist1, norm_hist2, cv2.HISTCMP_CHISQR)

def hist_intersect_sim(norm_hist1, norm_hist2):
  # compute intersection similarity b/w normalized and flattened histograms
  return cv2.compareHist(norm_hist1, norm_hist2, cv2.HISTCMP_INTERSECT)

def hist_bhatta_sim(norm_hist1, norm_hist2):
  # compute bhattacharyya similarity b/w normalized and flattened histograms
  return cv2.compareHist(norm_hist1, norm_hist2, cv2.HISTCMP_BHATTACHARYYA)

# compute the topn matches using the value saved in hist_sim above.
def compute_hist_sim(inhist_vec, hist_index, topn=3):

  if (args['clr']=='hsv'):
    inimg = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    inhist = cv2.calcHist([inimg],[0,1,2], None, [bin_size,bin_size,bin_size],[0,180,0,256,0,256])
    inhist_vec = cv2.normalize(inhist,inhist).flatten()

  hist_sim_box = []

  for imgp, norm_hist in hist_index.items():
    if(args['sim']=='correl'):
      hist_sim_box.append([imgp, hist_correl_sim(inhist_vec, norm_hist)])
    if(args['sim']=='chisqr'):
      hist_sim_box.append([imgp,hist_chisqr_sim(inhist_vec, norm_hist)])
    if(args['sim']=='inter'):
      hist_sim_box.append([imgp,hist_intersect_sim(inhist_vec, norm_hist)])
    if(args['sim']=='bhatta'):
      hist_sim_box.append([imgp,hist_bhatta_sim(inhist_vec, norm_hist)])

  if(args['sim']=='correl'):
    return sorted(hist_sim_box, key=lambda x: x[1],reverse=True)[:topn]
  if(args['sim']=='chisqr'):
    return sorted(hist_sim_box, key=lambda x: x[1])[:topn]
  if(args['sim']=='inter'):
    return sorted(hist_sim_box, key=lambda x: x[1],reverse=True)[:topn]
  if(args['sim']=='bhatta'):
    return sorted(hist_sim_box, key=lambda x: x[1])[:topn]

  return_list = []

  for x in xrange(topn):
    return_list.append(hist_sim_box[x])
  return return_list

def show_images(input_image, match_list):
  fig_base = plt.figure(1)
  fig_base.suptitle("Input")
  plt.imshow(input_image)

  holding = 2
  for impath, sim in match_list:
    img = cv2.imread(impath)
    img = cv2..cvtColor(inimg, cv2.COLOR_BGR2RGB)
    fig = plt.figure(holding)
    fig.suptitle('Match: '+str(holding-1)+str(impath)+' : '+str(sim))
    plt.imshow(img)
    holding += 1
  plt.show()
  cv2.waitKey(0) 

  pass
 
if __name__ == '__main__':
  with open(args['hist'], 'rb') as histfile:
    HIST_INDEX = pickle.load(histfile)
  sim_list = compute_hist_sim(inhist_vec, HIST_INDEX)
  for imagepath, sim in sim_list:
    print(imagepath + ' --> ' + str(sim))
  show_images(inimg, sim_list)


