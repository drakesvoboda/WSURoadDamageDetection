import pickle
import pickle_data
import numpy as np

def make_datasets(pickle_file, train_ratio, valid_ratio, test_ratio):
  try:
    with open(pickle_file, 'rb') as f:
      data = pickle.load(f)
      np.random.shuffle(data)
      start_train = 0
      start_valid = int(len(data) * train_ratio)
      start_test = int(len(data) * valid_ratio) + start_valid
      train = data[start_train:start_valid]
      valid = data[start_valid:start_test]
      test = data[start_test:]
      print('Total data: ', len(data))
      print('Train data: ', len(train))
      print('Valid data: ', len(valid))
      print(' Test data: ', len(test))
      return train, valid, test
  except Exception as e:
    print('Unable to process data from ', pickle_file, ' : ', e)
    raise


def load_data():
  # Percentage of data for each subset
  train_ratio = .9
  valid_ratio = .05
  test_ratio = .05

  if train_ratio + valid_ratio + test_ratio > 1:
    raise ValueError('Data ratios shoud add to 1')

  pickle_file = pickle_data.get_pickle_file()

  return make_datasets(pickle_file, train_ratio, valid_ratio, test_ratio)
