import pathlib
import os

from neoscore.common import *
from neoscore.core import paper
from notation_data import note_data, modifier_data

# all images should have a width no greater than 70 pixels (less is okay)
default_note_width = 70
# all images should have a height no greater than 104 pixels (less is okay)
default_note_height = 104
# used to scale up/down default image sizes for the final document/pdf
default_note_scale = 0.37

# Image Utilities
def get_note_scale(multiplier=1):
  return default_note_scale * multiplier

def note_width(multiplier=1):
  return Unit(default_note_width * get_note_scale(multiplier))

def note_height(multiplier=1):
  return Unit(default_note_height * get_note_scale(multiplier))

def get_data_definition(type, notation, right_hand):
  notation_data = None
  if type == 'modifier':
    notation_data = modifier_data[notation]
  elif type == 'note':
    notation_data = note_data[notation]
    
  if notation_data.get('both'):
    return notation_data['both']
  elif right_hand:
    return notation_data['right']
  else:
    return notation_data['left']

def get_data_type(type, notation):
  data = get_data_definition(type, notation, True)    
  if data.get('glyph'):
    return 'glyph'
  elif data.get('file_path'):
    return 'image'

def get_img_path(type, notation, right_hand):
  base_path = pathlib.Path(os.path.dirname(__file__)) / '..' / '..'
  data = get_data_definition(type, notation, right_hand)
  return base_path / data['file_path']

def get_glyph_id(type, notation, right_hand):
  data = get_data_definition(type, notation, right_hand)
  return data['glyph']
   
def get_img_x_offset(type, notation, right_hand):
  data = get_data_definition(type, notation, right_hand)
  if data.get('x_offset'):
    return Unit(data['x_offset'] * get_note_scale())
  else:
    return ZERO
  
def get_img_y_offset(type, notation, right_hand):
  data = get_data_definition(type, notation, right_hand)
  if data.get('y_offset'):
    return Unit(data['y_offset'] * get_note_scale())
  else:
    return ZERO
  
# Parsing Utilities
def parse_paper_size(str):
  if str == 'letter':
    return paper.LETTER
  else:
    return paper.A4

def parse_time_signature(str):
  time = TimeSignature()
  components = str.split('/')
  time.top_value = int(components[0])
  time.bottom_value = int(components[1])
  return time

def parse_duration(str):
  components = str.split('/')
  return Duration(int(components[0]), int(components[1]))

def parse_escaped_string(str):
  return str[1:-1]