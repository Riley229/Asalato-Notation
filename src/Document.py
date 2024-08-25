from enum import Enum

class PaperSize(Enum):
  Letter = 0
  A4 = 1


class Metadata:
  paper_size = PaperSize.Letter
  title = ''
  subtitle = ''
  composer = ''


class Staff:
  name = ''
  display_name = True
  western_notation = False
  
  
class Voice:
  name = ''
  left_pattern = []
  right_pattern = []
    
    
class TimeSignature:
  top_value = 4
  bottom_value = 4
  
  
class ScoreSegment:
  time_signature = TimeSignature()
  dot_value = 4
  voices = []
  

class Score:
  header = ''
  layout = []
  segments = []


class Document:
  metadata = Metadata()
  scores = []