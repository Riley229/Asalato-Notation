import pathlib

from neoscore.common import *

notation_data = {
  'flip': {
    'left': {
      'file_path': 'resources/flip-LH.svg',
      # x_offset defines the whitespace added to the left of a note for alignment
      #          notes are currently centered around the 35 pixel mark (stems go from 34-36)
      'x_offset': 4,
    },
    'right': {
      'file_path': 'resources/flip-RH.svg',
      'x_offset': 24,
    },
  },
  'flop': {
    'left': {
      'file_path': 'resources/flop-LH.svg',
      'x_offset': 4,
    },
    'right': {
      'file_path': 'resources/flop-RH.svg',
      'x_offset': 24,
    },
  },
  'flip_grab': {
    'left': {
      'file_path': 'resources/flip-LH-G.svg',
      'x_offset': 4,
    },
    'right': {
      'file_path':  'resources/flip-RH-G.svg',
      'x_offset': 24,
    },
  },
  'flop_grab': {
    'left': {
      'file_path': 'resources/flop-LH-G.svg',
      'x_offset': 4,
    },
    'right': {
      'file_path':  'resources/flop-RH-G.svg',
      'x_offset': 24,
    },
  },
  'click_flip': {
    'left': {
      'file_path': 'resources/click-FI.svg',
      'x_offset': 25.5,
    },
    'right': {
      'file_path': 'resources/click-FI.svg',
      'x_offset': 25.5,
    },
  },
  'click_flop': {
    'left': {
      'file_path': 'resources/click-FO.svg',
      'x_offset': 25.5,
    },
    'right': {
      'file_path': 'resources/click-FO.svg',
      'x_offset': 25.5,
    },
  },
  'click_flip_grab': {
    'left': {
      'file_path': 'resources/click-FI-G.svg',
      'x_offset': 25.5,
    },
    'right': {
      'file_path': 'resources/click-FI-G.svg',
      'x_offset': 25.5,
    },
  },
  'click_flop_grab': {
    'left': {
      'file_path': 'resources/click-FO-G.svg',
      'x_offset': 25.5,
    },
    'right': {
      'file_path': 'resources/click-FO-G.svg',
      'x_offset': 25.5,
    },
  },
  'den_down': {
    'left': {
      'file_path': 'resources/den-down-LH.svg',
      'x_offset': 0,
    },
    'right': {
      'file_path': 'resources/den-down-RH.svg',
      'x_offset': 24,
    },
  },
  'den_up': {
    'left': {
      'file_path': 'resources/den-up-LH.svg',
      'x_offset': 0,
    },
    'right': {
      'file_path': 'resources/den-up-RH.svg',
      'x_offset': 24,
    },
  },
  'den_down_grab': {
    'left': {
      'file_path': 'resources/den-down-LH-G.svg',
      'x_offset': 0,
    },
    'right': {
      'file_path': 'resources/den-down-RH-G.svg',
      'x_offset': 24,
    },
  },
  'den_up_grab': {
    'left': {
      'file_path': 'resources/den-up-LH-G.svg',
      'x_offset': 0,
    },
    'right': {
      'file_path': 'resources/den-up-RH-G.svg',
      'x_offset': 24,
    },
  },
  'airturn': {
    'left': {
      'file_path': 'resources/airturn-LH.svg',
      'x_offset': 4,
    },
    'right': {
      'file_path': 'resources/airturn-RH.svg',
      'x_offset': 14,
    },
  },
  'airturn_fake': {
    'left': {
      'file_path': 'resources/airturn-fake-LH.svg',
      'x_offset': 4,
    },
    'right': {
      'file_path': 'resources/airturn-fake-RH.svg',
      'x_offset': 14,
    },
  },
  'flip_throw': {
    'left': {
      'file_path': 'resources/flip-throw.svg',
      'x_offset': 9.5,
    },
    'right': {
      'file_path': 'resources/flip-throw.svg',
      'x_offset': 9.5,
    },
  },
  'flop_throw': {
    'left': {
      'file_path': 'resources/flop-throw.svg',
      'x_offset': 14,
    },
    'right': {
      'file_path': 'resources/flop-throw.svg',
      'x_offset': 14,
    },
  },
  'airturn_throw': {
    'left': {
      'file_path': 'resources/airturn-throw.svg',
      'x_offset': 4,
    },
    'right': {
      'file_path': 'resources/airturn-throw.svg',
      'x_offset': 4,
    },
  },
  'rest': {
    'left': {
      'file_path': 'resources/rest.svg',
      'x_offset': 31.5,
    },
    'right': {
      'file_path': 'resources/rest.svg',
      'x_offset': 31.5,
    },
  },
  'shake': {
    'left': {
      'file_path': 'resources/shake.svg',
      'x_offset': 34,
    },
    'right': {
      'file_path': 'resources/shake.svg',
      'x_offset': 34,
    },
  },
  'catch': {
    'left': {
      'file_path': 'resources/catch.svg',
      'x_offset': 24,
    },
    'right': {
      'file_path': 'resources/catch.svg',
      'x_offset': 24,
    },
  },
}

# all images should have a width no greater than 70 pixels (less is okay)
default_note_width = 70
# note_scale is used to scale up/down images for the final document/pdf
note_scale = 0.37

def get_img_path(notation, right):
  if right:
    return pathlib.Path('..') / notation_data[notation]['right']['file_path']
  else:
     return pathlib.Path('..') / notation_data[notation]['left']['file_path']
   
def get_img_x_offset(notation, right):
  if right:
    return Unit(notation_data[notation]['right']['x_offset'] * note_scale)
  else:
    return Unit(notation_data[notation]['left']['x_offset'] * note_scale)
  
def get_img_y_offset(notation, right):
  if right:
    return Unit(notation_data[notation]['right']['y_offset'] * note_scale)
  else:
    return Unit(notation_data[notation]['left']['y_offset'] * note_scale)