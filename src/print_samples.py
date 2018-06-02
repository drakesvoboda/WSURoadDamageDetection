from xml.etree import ElementTree
from xml.dom import minidom
import os
import random
import cv2
import matplotlib.pyplot as plt
import matplotlib as matplot

base_path = '../data/'
damageTypes = ["D00", "D01", "D10", "D11", "D20", "D40", "D43", "D44"]
govs =  ["Adachi", "Chiba", "Ichihara", "Muroran", "Nagakute", "Numazu", "Sumida"]

def draw_images(image_file):
  gov = image_file.split('_')[1]
  img = cv2.imread(base_path + gov + '/JPEGImages/' + image_file + '.jpg')
  
  infile_xml = open(base_path + gov + '/Annotations/' + image_file + '.xml')
  tree = ElementTree.parse(infile_xml)
  root = tree.getroot()
  
  for obj in root.iter('object'):
    cls_name = obj.find('name').text
    xmlbox = obj.find('bndbox')
    xmin = int(xmlbox.find('xmin').text)
    xmax = int(xmlbox.find('xmax').text)
    ymin = int(xmlbox.find('ymin').text)
    ymax = int(xmlbox.find('ymax').text)

    font = cv2.FONT_HERSHEY_SIMPLEX

    # put text
    cv2.putText(img,cls_name,(xmin,ymin-10),font,1,(0,255,0),2,cv2.LINE_AA)

    # draw bounding box
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0,255,0),3)
  return img

for i, gov in enumerate(govs):
  file_list = os.listdir(base_path + gov + '/Annotations/')
  for file in file_list[0:1]:
    img = draw_images(file.split('.')[0])
    plt.axis('off')
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


