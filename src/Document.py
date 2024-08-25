from enum import Enum

class PaperSize(Enum):
  Letter = 0
  A4 = 1


class Metadata:
  def __init__(self):
    self.paper_size = PaperSize.Letter
    self.title = ''
    self.subtitle = ''
    self.composer = ''


class Staff:
  def __init__(self):
    self.name = ''
    self.display_name = True
    self.western_notation = False
  
  
class Voice:
  def __init__(self):
    self.name = ''
    self.left_pattern = []
    self.right_pattern = []
    
    
class TimeSignature:
  def __init__(self):
    self.top_value = 4
    self.bottom_value = 4
  
  
class ScoreSegment:
  def __init__(self):
    self.time_signature = None
    self.dot_value = 4
    self.voices = []
  

class Score:
  def __init__(self):
    self.header = ''
    self.layout = []
    self.segments = []


class Document:
  def __init__(self):
    self.metadata = Metadata()
    self.scores = []