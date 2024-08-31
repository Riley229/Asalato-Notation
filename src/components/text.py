from lark.lexer import Token
from neoscore.common import *
from components.util import parse_escaped_string

class DocumentText:
  def __init__(self, text='', font='Arial', font_size=Unit(10), font_weight=50, italic=False):
    self.text = text
    self.font = font
    self.font_size = font_size
    self.font_weight = font_weight
    self.italic = italic
    
  def from_tree(tree, default_font='Arial', default_font_size=Unit(10), default_font_weight=50, default_italic=False):
    text = DocumentText('', default_font, default_font_size, default_font_weight, default_italic)
    for option in tree.children:
      if type(option) == Token:
        text.text = parse_escaped_string(option.value)
      elif option.data.value == 'text_formatting':
        for format_option in option.children:
          if format_option.data.value == 'font':
            text.font = parse_escaped_string(format_option.children[0].value)
          elif format_option.data.value == 'font_size':
            text.font_size = Unit(float(format_option.children[0].value))
          elif format_option.data.value == 'font_weight':
            text.font_weight = int(format_option.children[0].value)
          elif format_option.data.value == 'font_italic':
            text.italic = True
      
    return text
  
  def draw(self, position, parent, alignment_x=AlignmentX.LEFT):
    return Text(position, parent, self.text, Font(self.font, self.font_size, self.font_weight, self.italic), alignment_x=alignment_x)