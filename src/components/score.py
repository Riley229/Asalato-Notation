from lark.lexer import Token
from neoscore.western.duration import Duration
from neoscore.common import *
from components.measure import Measure
from components.note import Note, EmptyNote, Tuplet
from components.util import note_height, note_width, parse_escaped_string, parse_duration, parse_boolean

class TimeSignature:
  def __init__(self, top_value=4, bottom_value=4):
    self.top_value = top_value
    self.bottom_value = bottom_value
    
  def beats_per_measure(self):
    return self.top_value * (4 / self.bottom_value)
  
  def from_tree(tree):
    components = tree.children[0].value.split('/')
    return TimeSignature(int(components[0]), int(components[1]))


class ScoreDisplay:
  def __init__(self, voices):
    self.measures = []
    
    voice = voices[0] # temporary, only supports 1 voice
    time_pattern = [x for _, x in sorted(zip(voice.time_pattern_indices, voice.time_pattern))]
    time_pattern_indices = sorted(voice.time_pattern_indices)
    measure = Measure(TimeSignature(), Duration(1, 4), [], [])

    time_pattern_index = 0
    measure_index = 0
    
    if len(voice.right_pattern) != len(voice.left_pattern):
      raise Exception('Hands have mismatching beats. Right hand has %s beats while left hand has %s beats' % (len(voice.right_pattern), len(voice.left_pattern)))
    
    for index in range(0, len(voice.right_pattern)):
      while (len(time_pattern_indices) > time_pattern_index) and (time_pattern_indices[time_pattern_index] == index):
        if measure_index != 0:
          raise Exception('Time definition specified before new measure')
        elif type(time_pattern[time_pattern_index]) == TimeSignature:
          measure.time_signature = time_pattern[time_pattern_index]
        elif type(time_pattern[time_pattern_index]) == Duration:
          measure.note_duration = time_pattern[time_pattern_index]
        time_pattern_index += 1
        
      measure.right_pattern.append(voice.right_pattern[index])
      measure.left_pattern.append(voice.left_pattern[index])
        
      measure_index += 1
      if measure_index == measure.expected_note_count():
        self.measures.append(measure)
        measure = Measure(measure.time_signature, measure.note_duration, [], [])
        measure_index = 0
    
    if measure_index != 0:
      raise Exception('Final measure is missing %s beats' % int(measure.expected_note_count() - measure_index))
      
  def draw(self, y_offset, parent):
    length = ZERO
    for measure in self.measures:
      length += measure.minimum_width()

    flowable = Flowable((ZERO, Unit(y_offset)), parent, length - Unit(1), Unit(110), break_threshold=Unit(300))
    staff_group = StaffGroup()
    
    # create staff objects
    Staff((ZERO, y_offset), flowable, length * 3, staff_group, line_count=0) # additional staff is used to "lead" barlines
    right_staff = Staff((ZERO, y_offset + note_width(0.5)), flowable, length, staff_group, line_count=0)
    InstrumentName((right_staff.unit(-2), right_staff.center_y), right_staff, 'R', 'R', font=Font('Arial', Unit(10), weight=50))
    left_staff = Staff((ZERO, y_offset + note_height(1.5)), flowable, length, staff_group, line_count=0)
    InstrumentName((left_staff.unit(-2), left_staff.center_y), left_staff, 'L', 'L', font=Font('Arial', Unit(10), weight=50))
    Staff((ZERO, y_offset + note_height(2.0)), flowable, length, staff_group, line_count=0) # additional staff is used to "ground" barlines
    
    x_offset = ZERO
    time_signature = None
    note_duration = None
    for measure in self.measures:
      render_time_signature = False
      render_note_duration = False
      if time_signature != measure.time_signature:
        render_time_signature = True
        time_signature = measure.time_signature
      if note_duration != measure.note_duration:
        render_note_duration = True
        note_duration = measure.note_duration
        
      measure.draw(x_offset, right_staff, left_staff, staff_group, render_note_duration, render_time_signature)
      x_offset += measure.minimum_width()
      
    SystemLine(staff_group)   # Automatically adds barlines to the beginning of each line
    return flowable.canvas_pos().y + flowable.height + Unit(50)
  
  
class Voice:
  def __init__(self, name='', left_pattern=[], right_pattern=[], time_pattern=[], time_pattern_indices=[]):
    self.name = name
    self.left_pattern = left_pattern
    self.right_pattern = right_pattern
    self.time_pattern = time_pattern
    self.time_pattern_indices = time_pattern_indices
    
  def parse_hand_from_tree(tree, time_pattern, time_pattern_indices, hand_pattern, right_hand):
    for notation in tree.children:
      if notation.children[0].data.value == 'time_signature':
        time_pattern.append(TimeSignature.from_tree(notation.children[0]))
        time_pattern_indices.append(len(hand_pattern))
      elif notation.children[0].data.value == 'note_duration':
        time_pattern.append(parse_duration(notation.children[0].children[0].value))
        time_pattern_indices.append(len(hand_pattern))
      elif notation.children[0].data.value == 'tuplet':
        tuplet = Tuplet.from_tree(notation.children[0], right_hand)
        hand_pattern.append(tuplet)
        for i in range(0, tuplet.duration - 1):
          hand_pattern.append(EmptyNote())
      elif notation.children[0].data.value == 'note_notation':
        hand_pattern.append(Note.from_tree(notation.children[0].children[0], right_hand))
    
  def from_tree(tree):
    voice = Voice()
    for child in tree.children:
      if type(child) == Token:
        voice.name = parse_escaped_string(child.value)
      else:
        for option in child.children:
          if option.data.value == 'right_hand':
            Voice.parse_hand_from_tree(option, voice.time_pattern, voice.time_pattern_indices, voice.right_pattern, True)
          elif option.data.value == 'left_hand':
            Voice.parse_hand_from_tree(option, voice.time_pattern, voice.time_pattern_indices, voice.left_pattern, False)
    
    return voice  
  
  
class ScoreStaff:
  def __init__(self, name='', display_name=True, western_notation=False):
    self.name = name
    self.display_name = display_name
    self.western_notation = western_notation
    
  def from_tree(tree):
    staff = ScoreStaff()
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
  def __init__(self, header='', layout=[], voices=[], display=None):
    self.header = header
    self.layout = layout
    self.voices = voices
    self.display = display
    
  def from_tree(tree):
    score = Score()
    for child in tree.children:
      for option in child.children:
        if option.data.value == 'score_header':
          score.header = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'score_layout':
          for staff_tree in option.children:
            score.layout.append(ScoreStaff.from_tree(staff_tree))
        elif option.data.value == 'score_voice':
          score.voices.append(Voice.from_tree(option))
          
    score.display = ScoreDisplay(score.voices)
    return score
  
  def draw(self, y_pos):
    header_text = Text(Point(ZERO, y_pos + Unit(25)), None, self.header, font=Font('Arial', Unit(10), weight=80))
    self.display.draw(Unit(25), header_text)