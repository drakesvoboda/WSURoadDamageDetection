import six.moves.urllib as urllib
import os

try:
  import urllib.request
except ImportError:
  raise ImportError('You should use Python 3.x')

if not os.path.exists('../data/road_damage_dataset.tar.gz'):
  url_base = 'https://s3-ap-northeast-1.amazonaws.com/mycityreport/RoadDamageDataset.tar.gz'
  urllib.request.urlretrieve(url_base, '../data/road_damage_dataset.tar.gz')
  print("Download road_damage_dataset.tar.gz Done")
    
else:
  print("You have road_damage_dataset.tar.gz")


