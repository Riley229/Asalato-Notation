import pathlib
import os

from enum import Enum
from neoscore.common import *
from notation_data import notation_data

# all images should have a width no greater than 70 pixels (less is okay)
default_note_width = 70
# all images should have a height no greater than 104 pixels (less is okay)
default_note_height = 104
# used to scale up/down default image sizes for the final document/pdf
default_note_scale = 0.37

def get_note_scale(multiplier=1):
  return default_note_scale * multiplier

def note_width(multiplier=1):
  return Unit(default_note_width * get_note_scale(multiplier))

def note_height(multiplier=1):
  return Unit(default_note_height * get_note_scale(multiplier))

def get_img_path(notation, right_hand):
  base_path = pathlib.Path(os.path.dirname(__file__)) / '..' / '..'
  if right_hand:
    return base_path / notation_data[notation]['right']['file_path']
  else:
    return base_path / notation_data[notation]['left']['file_path']
   
def get_img_x_offset(notation, right_hand):
  if right_hand:
    return Unit(notation_data[notation]['right']['x_offset'] * get_note_scale())
  else:
    return Unit(notation_data[notation]['left']['x_offset'] * get_note_scale())
  
def get_img_y_offset(notation, right_hand):
  if right_hand:
    return Unit(notation_data[notation]['right']['y_offset'] * get_note_scale())
  else:
    return Unit(notation_data[notation]['left']['y_offset'] * get_note_scale())
  
def parse_paper_size(str):
  if str == 'letter':
    return PaperSize.Letter
  else:
    return PaperSize.A4

def parse_time_signature(str):
  time = TimeSignature()
  components = str.split('/')
  time.top_value = int(components[0])
  time.bottom_value = int(components[1])
  return time
  
def parse_boolean(str):
  if str == 'true':
    return True
  else:
    return False
  
def parse_escaped_string(str):
  return str[1:-1]

def parse_duration(str):
  components = str.split('/')
  return Duration(int(components[0]), int(components[1]))

class PaperSize(Enum):
  Letter = 0
  A4 = 1