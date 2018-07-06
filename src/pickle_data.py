import os
import pickle
import numpy as np
from xml.etree import ElementTree
from xml.dom import minidom
from PIL import Image

image_size = [300, 300]
image_ratio = [image_size[0] / 600, image_size[1] / 600]

base_path = '../data/'
govs =  ["Adachi", "Chiba", "Ichihara", "Muroran", "Nagakute", "Numazu", "Sumida"]

def load_gov_data(govfolder):
  file_list = os.listdir(govfolder + '/Annotations/')
  images = np.ndarray(shape=(len(file_list), image_size[0], image_size[1], 3), dtype=np.int32)
  labels = np.ndarray(shape=(len(file_list), 1), dtype=object)
  num_images = 0
  for xml_file in file_list:
    name = xml_file.split('.')[0]
    image_file = os.path.join(govfolder + "/JPEGImages/", name + '.jpg')

    try:
      with Image.open(image_file).resize(image_size, Image.ANTIALIAS) as pic:
        image_data = np.array(pic.getdata()).reshape((image_size[0], image_size[1], 3))
        if image_data.shape != (image_size[0], image_size[1], 3):
          raise Exception('Unexpected image shape: %s' % str(image_data.shape))
        images[num_images, :, :, :] = image_data

      with open(govfolder + '/Annotations/' + name + '.xml') as infile_xml:
        labels[num_images, :] = infile_xml.read()

      num_images += 1
      if num_images % 100 == 0:
        update_progress(num_images * 100 / len(file_list))

    except (IOError, ValueError) as e:
      print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')

  return zip(images, labels)

def load_all_data():
  file_list = []
  for gov in govs:
    file_list.extend([[base_path + gov,  file] for file in os.listdir(base_path + gov + '/Annotations/')])

  file_list = file_list

  images = np.ndarray(shape=(len(file_list), image_size[0], image_size[1], 3), dtype=np.uint8)
  labels = np.ndarray(len(file_list), dtype=object)
  num_images = 0

  for file in file_list:
    govfolder = file[0]
    name = file[1].split('.')[0]
    image_file = os.path.join(govfolder + "/JPEGImages/", name + '.jpg')

    try:
      with Image.open(image_file).resize(image_size, Image.ANTIALIAS) as pic:
        image_data = np.array(pic.getdata()).reshape((image_size[0], image_size[1], 3))
        if image_data.shape != (image_size[0], image_size[1], 3):
          raise Exception('Unexpected image shape: %s' % str(image_data.shape))
        images[num_images, :, :, :] = image_data

      with open(govfolder + '/Annotations/' + name + '.xml') as infile_xml:
        label = ""
        tree = ElementTree.parse(infile_xml)
        root = tree.getroot()
        for obj in root.iter('object'): 
          cls_name = obj.find('name').text
          xmlbox = obj.find('bndbox')
          xmin = int(int(xmlbox.find('xmin').text) * image_ratio[0])
          ymin = int(int(xmlbox.find('ymin').text) * image_ratio[1])
          xmax = int(int(xmlbox.find('xmax').text) * image_ratio[0])
          ymax = int(int(xmlbox.find('ymax').text) * image_ratio[1])
          label += "{0} {1} {2} {3} {4} ".format(cls_name, xmin, ymin, xmax, ymax)
        
        labels[num_images:num_images+1] = label[:-1]

      num_images += 1
      if num_images % 100 == 0:
        update_progress(num_images * 100 / len(file_list))

    except (IOError, ValueError) as e:
      print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')
  
  update_progress(100)
  return list(zip(images, labels))


def pickle_data(data_folders):
  pickles = []
  for folder in data_folders:
    filename = base_path + folder + '.pickle'
    dataset = load_gov_data(base_path + folder)

    try:
      with open(filename, 'wb') as f:
        pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)
      print('Pickled %s.' % filename)
    except Exception as e:
      print('Unable to save data to', set_filename, ':', e)

  pickles.append(filename)

  return pickles


def pickle_all_data():
  dataset = load_all_data() 
  filename = base_path + 'full_dataset.pickle'
  try:
    print('Saving %s.' % filename)
    with open(filename, 'wb') as f:
      pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)
    print('Pickled %s.' % filename)
  except Exception as e:
    print('Unable to save data to', set_filename, ':', e)

def get_pickle_file():
  filename = base_path + 'full_dataset.pickle'
  return filename

def update_progress(progress):
  print('[{0}{1}] {2}%'.format('#'*int(progress/10), ' '*(10-int(progress/10)), int(progress)), end='\r')

def main():
  pickle_all_data()
  return

if __name__ == '__main__':
    main()

