import pathlib

from neoscore.common import *

notation_data = {
  'flip': {
    'left': {
      'file_path': 'resources/flip-LH.svg',
      # x_offset: defines whitespace added to left of note for alignment
      #           note stems should be horizontally centered around the 35th pixel with a width of 2 pixels (pixels 34-36)
      'x_offset': 4,
      # y_offset: defines whitespace added to top of note for alignment
      #           note stems should be vertically centered around the 52nd pixel with a height of 42 pixels (pixels 31-73)
      'y_offset': 21,
    },
    'right': {
      'file_path': 'resources/flip-RH.svg',
      'x_offset': 24,
      'y_offset': 21,
    },
  },
  'flop': {
    'left': {
      'file_path': 'resources/flop-LH.svg',
      'x_offset': 4,
      'y_offset': 31,
    },
    'right': {
      'file_path': 'resources/flop-RH.svg',
      'x_offset': 24,
      'y_offset': 31,
    },
  },
  'flip_grab': {
    'left': {
      'file_path': 'resources/flip-LH-G.svg',
      'x_offset': 4,
      'y_offset': 17,
    },
    'right': {
      'file_path':  'resources/flip-RH-G.svg',
      'x_offset': 24,
      'y_offset': 17,
    },
  },
  'flop_grab': {
    'left': {
      'file_path': 'resources/flop-LH-G.svg',
      'x_offset': 4,
      'y_offset': 31,
    },
    'right': {
      'file_path':  'resources/flop-RH-G.svg',
      'x_offset': 24,
      'y_offset': 31,
    },
  },
  'click_flip': {
    'left': {
      'file_path': 'resources/click-FI.svg',
      'x_offset': 25.5,
      'y_offset': 31,
    },
    'right': {
      'file_path': 'resources/click-FI.svg',
      'x_offset': 25.5,
      'y_offset': 31,
    },
  },
  'click_flop': {
    'left': {
      'file_path': 'resources/click-FO.svg',
      'x_offset': 25.5,
      'y_offset': 31,
    },
    'right': {
      'file_path': 'resources/click-FO.svg',
      'x_offset': 25.5,
      'y_offset': 31,
    },
  },
  'click_flip_grab': {
    'left': {
      'file_path': 'resources/click-FI-G.svg',
      'x_offset': 25.5,
      'y_offset': 31,
    },
    'right': {
      'file_path': 'resources/click-FI-G.svg',
      'x_offset': 25.5,
      'y_offset': 31,
    },
  },
  'click_flop_grab': {
    'left': {
      'file_path': 'resources/click-FO-G.svg',
      'x_offset': 25.5,
      'y_offset': 31,
    },
    'right': {
      'file_path': 'resources/click-FO-G.svg',
      'x_offset': 25.5,
      'y_offset': 31,
    },
  },
  'den_down': {
    'left': {
      'file_path': 'resources/den-down-LH.svg',
      'x_offset': 0,
      'y_offset': 31,
    },
    'right': {
      'file_path': 'resources/den-down-RH.svg',
      'x_offset': 24,
      'y_offset': 31,
    },
  },
  'den_up': {
    'left': {
      'file_path': 'resources/den-up-LH.svg',
      'x_offset': 0,
      'y_offset': 21,
    },
    'right': {
      'file_path': 'resources/den-up-RH.svg',
      'x_offset': 24,
      'y_offset': 21,
    },
  },
  'den_down_grab': {
    'left': {
      'file_path': 'resources/den-down-LH-G.svg',
      'x_offset': 0,
      'y_offset': 31,
    },
    'right': {
      'file_path': 'resources/den-down-RH-G.svg',
      'x_offset': 24,
      'y_offset': 31,
    },
  },
  'den_up_grab': {
    'left': {
      'file_path': 'resources/den-up-LH-G.svg',
      'x_offset': 0,
      'y_offset': 17,
    },
    'right': {
      'file_path': 'resources/den-up-RH-G.svg',
      'x_offset': 24,
      'y_offset': 17,
    },
  },
  'airturn': {
    'left': {
      'file_path': 'resources/airturn-LH.svg',
      'x_offset': 4,
      'y_offset': 21,
    },
    'right': {
      'file_path': 'resources/airturn-RH.svg',
      'x_offset': 14,
      'y_offset': 21,
    },
  },
  'airturn_fake': {
    'left': {
      'file_path': 'resources/airturn-fake-LH.svg',
      'x_offset': 4,
      'y_offset': 21,
    },
    'right': {
      'file_path': 'resources/airturn-fake-RH.svg',
      'x_offset': 14,
      'y_offset': 21,
    },
  },
  'flip_throw': {
    'left': {
      'file_path': 'resources/flip-throw.svg',
      'x_offset': 9.5,
      'y_offset': 0,
    },
    'right': {
      'file_path': 'resources/flip-throw.svg',
      'x_offset': 9.5,
      'y_offset': 0,
    },
  },
  'flop_throw': {
    'left': {
      'file_path': 'resources/flop-throw.svg',
      'x_offset': 14,
      'y_offset': 31,
    },
    'right': {
      'file_path': 'resources/flop-throw.svg',
      'x_offset': 14,
      'y_offset': 31,
    },
  },
  'airturn_throw': {
    'left': {
      'file_path': 'resources/airturn-throw.svg',
      'x_offset': 4,
      'y_offset': 2,
    },
    'right': {
      'file_path': 'resources/airturn-throw.svg',
      'x_offset': 4,
      'y_offset': 2,
    },
  },
  'rest': {
    'left': {
      'file_path': 'resources/rest.svg',
      'x_offset': 31.5,
      'y_offset': 48.5,
    },
    'right': {
      'file_path': 'resources/rest.svg',
      'x_offset': 31.5,
      'y_offset': 48.5,
    },
  },
  'shake': {
    'left': {
      'file_path': 'resources/shake.svg',
      'x_offset': 34,
      'y_offset': 45.5,
    },
    'right': {
      'file_path': 'resources/shake.svg',
      'x_offset': 34,
      'y_offset': 45.5,
    },
  },
  'catch': {
    'left': {
      'file_path': 'resources/catch.svg',
      'x_offset': 24,
      'y_offset': 21,
    },
    'right': {
      'file_path': 'resources/catch.svg',
      'x_offset': 24,
      'y_offset': 21,
    },
  },
}

# all images should have a width no greater than 70 pixels (less is okay)
default_note_width = 70
# all images should have a height no greater than 104 pixels (less is okay)
default_note_height = 104
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