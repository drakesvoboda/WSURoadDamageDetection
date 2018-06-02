from xml.etree import ElementTree
from xml.dom import minidom
import collections
import os
import matplotlib.pyplot as plt
import matplotlib as matplot
import seaborn as sns

base_path = '../data/'

damageTypes = ["D00", "D01", "D10", "D11", "D20", "D40", "D43", "D44"]
govs =  ["Adachi", "Chiba", "Ichihara", "Muroran", "Nagakute", "Numazu", "Sumida"]

# the number of total images and total labels.
cls_names = []
total_images = 0
for gov in govs:
  file_list = os.listdir(base_path + gov + '/Annotations/')
  for file in file_list:
    total_images = total_images + 1
    if file =='.DS_Store':
      pass
    else:
      infile_xml = open(base_path + gov + '/Annotations/' + file)
      tree = ElementTree.parse(infile_xml)
      root = tree.getroot()
      for obj in root.iter('object'):
        cls_name = obj.find('name').text
        cls_names.append(cls_name)

print("total")
print("# of images: " + str(total_images))
print("# of labels: " + str(len(cls_names)))

import collections
count_dict = collections.Counter(cls_names)
cls_count = []
for damageType in damageTypes:
  print(str(damageType) + ' : ' + str(count_dict[damageType]))
  cls_count.append(count_dict[damageType])

sns.set_palette("winter", 8)
sns.barplot(damageTypes, cls_count)

# the number of each class labels for each municipality
for gov in govs:
  cls_names = []
  total_images = 0
  file_list = os.listdir(base_path + gov + '/Annotations/')

  for file in file_list:
    total_images = total_images + 1
    if file =='.DS_Store':
      pass
    else:
      infile_xml = open(base_path + gov + '/Annotations/' + file)
      tree = ElementTree.parse(infile_xml)
      root = tree.getroot()
      for obj in root.iter('object'):
        cls_name = obj.find('name').text
        cls_names.append(cls_name)

  print('**************************************************')
  print(gov)
  print("# of images:" + str(total_images))
  print("# of labels:" + str(len(cls_names)))

  count_dict = collections.Counter(cls_names)
  cls_count = []
  for damageType in damageTypes:
    print(str(damageType) + ' : ' + str(count_dict[damageType]))
    cls_count.append(count_dict[damageType])

print('**************************************************')

