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

# Used to dynamically scale each scores notations
custom_note_scale = 1.0
custom_note_spacing = 1.0


# Image Utilities
def set_custom_note_scale(note_scale, note_spacing):
  global custom_note_scale
  global custom_note_spacing
  custom_note_scale = note_scale
  custom_note_spacing = note_spacing

def get_note_scale(multiplier=1):
  return default_note_scale * multiplier * custom_note_scale

def note_width(multiplier=1):
  return Unit(default_note_width * get_note_scale(multiplier) * custom_note_spacing)

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
   
def get_x_offset(type, notation, right_hand):
  data = get_data_definition(type, notation, right_hand)
  if data.get('center_x'):
    return Unit(((default_note_width / 2) - data['center_x']) * get_note_scale())
  else:
    return note_width(0.5)
  
def get_y_alignment(type, notation, right_hand):
  data = get_data_definition(type, notation, right_hand)
  if data.get('alignment'):
    return data['alignment']
  else:
    return 'top'  
  
def get_y_offset(type, notation, right_hand):
  base_value = -1 if get_y_alignment(type, notation, right_hand) == 'top' else 1
  data = get_data_definition(type, notation, right_hand)
  if data.get('center_y'):
    return (base_value * note_height(0.5)) + Unit(((default_note_height / 2) - data['center_y']) * get_note_scale())
  else:
    return base_value * note_height(0.5)

def get_y_alignment_offset(base_type, base_notation, accessory_type, accessory_notation, right_hand):
  alignment = get_y_alignment(accessory_type, accessory_notation, right_hand)
  if alignment == 'bottom':
    base_data = get_data_definition(base_type, base_notation, right_hand)
    return get_y_offset(base_type, base_notation, right_hand) + Unit(base_data['height'] * get_note_scale())
  else:
    accessory_data = get_data_definition(accessory_type, accessory_notation, right_hand)
    return get_y_offset(base_type, base_notation, right_hand) - Unit(accessory_data['height'] * get_note_scale())
  
# Parsing Utilities
def parse_margin(tree):
  if tree.data.value == 'inch':
    return Inch(float(tree.children[0].value))
  elif tree.data.value == 'millimeter':
    return Mm(float(tree.children[0].value))
  else:
    return None

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