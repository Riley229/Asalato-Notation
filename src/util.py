import pathlib

from neoscore.common import *

notation_data = {
  'flip': {
    'left_file_path': 'resources/flip-LH.svg',
    'right_file_path': 'resources/flip-RH.svg',
  },
  'flop': {
    'left_file_path': 'resources/flop-LH.svg',
    'right_file_path': 'resources/flop-RH.svg',
  },
  'flip_grab': {
    'left_file_path': 'resources/flip-LH-G.svg',
    'right_file_path': 'resources/flip-RH-G.svg',
  },
  'flop_grab': {
    'left_file_path': 'resources/flop-LH-G.svg',
    'right_file_path': 'resources/flop-LH-G.svg',
  },
  'click_flip': {
    'left_file_path': 'resources/click-FI.svg',
    'right_file_path': 'resources/click-FI.svg',
  },
  'click_flop': {
    'left_file_path': 'resources/click-FO.svg',
    'right_file_path': 'resources/click-FO.svg',
  },
  'click_flip_grab': {
    'left_file_path': 'resources/click-FI-G.svg',
    'right_file_path': 'resources/click-FI-G.svg',
  },
  'click_flop_grab': {
    'left_file_path': 'resources/click-FO-G.svg',
    'right_file_path': 'resources/click-FO-G.svg',
  },
  'den_down': {
    'left_file_path': 'resources/den-down-LH.svg',
    'right_file_path': 'resources/den-down-RH.svg',
  },
  'den_up': {
    'left_file_path': 'resources/den-up-LH.svg',
    'right_file_path': 'resources/den-up-RH.svg',
  },
  'den_down_grab': {
    'left_file_path': 'resources/den-down-LH-G.svg',
    'right_file_path': 'resources/den-down-RH-G.svg',
  },
  'den_up_grab': {
    'left_file_path': 'resources/den-up-LH-G.svg',
    'right_file_path': 'resources/den-up-RH-G.svg',
  },
  'airturn': {
    'left_file_path': 'resources/airturn-LH.svg',
    'right_file_path': 'resources/airturn-RH.svg',
  },
  'airturn_fake': {
    'left_file_path': 'resources/airturn-fake-LH.svg',
    'right_file_path': 'resources/airturn-fake-RH.svg',
  },
  'flip_throw': {
    'left_file_path': 'resources/flip-throw.svg',
    'right_file_path': 'resources/flip-throw.svg',
  },
  'flop_throw': {
    'left_file_path': 'resources/flop-throw.svg',
    'right_file_path': 'resources/flop-throw.svg',
  },
  'airturn_throw': {
    'left_file_path': 'resources/airturn-throw.svg',
    'right_file_path': 'resources/airturn-throw.svg',
  },
  'rest': {
    'left_file_path': 'resources/rest.svg',
    'right_file_path': 'resources/rest.svg',
  },
  'shake': {
    'left_file_path': 'resources/shake.svg',
    'right_file_path': 'resources/shake.svg',
  },
  'catch': {
    'left_file_path': 'resources/catch.svg',
    'right_file_path': 'resources/catch.svg',
  },
}

def get_img_path(notation, right):
  if right:
    return pathlib.Path('..') / notation_data[notation]['right_file_path']
  else:
     return pathlib.Path('..') / notation_data[notation]['left_file_path']
   
# TODO: implement
def get_img_x_offset(notation, right):
  return ZERO