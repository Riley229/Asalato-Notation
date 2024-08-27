from enum import Enum
from lark.lexer import Token

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
class PaperSize(Enum):
  Letter = 0
  A4 = 1
  
  
class Voice:
  def __init__(self, name='', left_pattern=[], right_pattern=[]):
    self.name = name
    self.left_pattern = left_pattern
    self.right_pattern = right_pattern
    
  def from_tree(tree):
    voice = Voice()
    for child in tree.children:
      if type(child) == Token:
        voice.name = parse_escaped_string(child.value)
      else:
        for option in child.children:
          if option.data.value == 'right_voice_component':
            for notation in option.children:
              voice.right_pattern.append(notation.children[0].data.value)
          elif option.data.value == 'left_voice_component':
            for notation in option.children:
              voice.left_pattern.append(notation.children[0].data.value)
    
    return voice
    
    
class TimeSignature:
  def __init__(self, top_value=4, bottom_value=4):
    self.top_value = top_value
    self.bottom_value = bottom_value
    
  def beats_per_measure(self):
    return self.top_value * (4 / self.bottom_value)
  
  
class ScoreSegment:
  def __init__(self, time_signature=None, dot_value=None, voices=[]):
    self.time_signature = time_signature
    self.dot_value = dot_value
    self.voices = voices
    
  def notes_per_measure(self):
    return (self.time_signature.beats_per_measure() / 4) * (self.dot_value.bottom_value / self.dot_value.top_value)
  
  def from_tree(tree):
    segment = ScoreSegment()
    for child in tree.children:
      for option in child.children:
        if option.data.value == 'segment_time':
          segment.time_signature = parse_time_signature(option.children[0].value)
        elif option.data.value == 'segment_dot_value':
          segment.dot_value = parse_time_signature(option.children[0].value)
        elif option.data.value == 'segment_voice':
          segment.voices.append(Voice.from_tree(option))
    
    return segment
  
  
class Staff:
  def __init__(self, name='', display_name=True, western_notation=False):
    self.name = name
    self.display_name = display_name
    self.western_notation = western_notation
    
  def from_tree(tree):
    staff = Staff()
    for child in tree.children:
      if type(child) == Token:
        staff.name = parse_escaped_string(child.value)
      else:
        for option in child.children:
          if option.data.value == 'staff_display_name':
            staff.display_name = parse_boolean(option.children[0].value)
          elif option.data.value == 'staff_western_notation':
            staff.western_notation == parse_boolean(option.children[0].value)
    
    return staff


class Score:
  def __init__(self, header='', layout=[], segments=[]):
    self.header = header
    self.layout = layout
    self.segments = segments
    
  def from_tree(tree):
    score = Score()
    for child in tree.children:
      for option in child.children:
        if option.data.value == 'score_header':
          score.header = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'score_layout':
          for staff_tree in option.children:
            score.layout.append(Staff.from_tree(staff_tree))
        elif option.data.value == 'score_segment':
          segment = ScoreSegment.from_tree(option)
          if len(score.segments) == 0:
            if segment.time_signature == None:
              segment.time_signature = TimeSignature(4, 4)
            if segment.dot_value == None:
              segment.dot_value = TimeSignature(1, 4)
          score.segments.append(segment)
    
    return score


class Metadata:
  def __init__(self, paper_size=PaperSize.Letter, title='', subtitle='', composer=''):
    self.paper_size = paper_size
    self.title = title
    self.subtitle = subtitle
    self.composer = composer
    
  def from_tree(tree):
    metadata = Metadata()
    for child in tree.children:
      for option in child.children:
        if option.data.value == 'paper_size':
          metadata.papersize = parse_paper_size(option.children[0].value)
        elif option.data.value == 'title':
          metadata.title = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'subtitle':
          metadata.subtitle = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'composer':
          metadata.composer = parse_escaped_string(option.children[0].value)
          
    return metadata


class Document:
  def __init__(self, metadata=Metadata(), scores=[]):
    self.metadata = metadata
    self.scores = scores
    
  def from_tree(tree):
    document = Document()
    for child in tree.children:
      if child.data.value == 'metadata':
        document.metadata = Metadata.from_tree(child)
      elif child.data.value == 'score':
        document.scores.append(Score.from_tree(child))
        
    return document