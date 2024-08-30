from lark.lexer import Token
from neoscore.western.duration import Duration
from neoscore.common import *
from components.measure import Measure, TimeSignature
from components.note import Note, EmptyNote, Tuplet
from components.util import note_height, note_width, parse_escaped_string, parse_duration


class ScoreDisplay:
  def __init__(self, voices, layout):    
    if len(layout) == 0:
      return
    voice = None
    for next_voice in voices:                     # temporary, only supports 1 voice
      if next_voice.name == layout[0].name:
        voice = next_voice
        break
      
    self.measures = []
    self.staff = layout[0]
      
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
    if self.staff == None:
      return y_offset
    
    # seperate the measures into seperate lines based on calculated widths
    lines = []
    max_line_width = neoscore.document.paper.live_width - Unit(15)
    current_line = []
    current_line_width = ZERO
    for measure in self.measures:
      measure_width = measure.get_width()
      if (current_line_width == ZERO) or (measure_width + current_line_width < max_line_width):
        current_line.append(measure)
        current_line_width += measure_width
      else:
        lines.append(current_line)
        current_line = [measure]
        current_line_width = ZERO
        
    # ensure the final line is added
    if len(current_line) > 0:
      lines.append(current_line)

    # calculate total length of all lines and create flowable/staff group objects
    total_length = len(lines) * max_line_width
    flowable = Flowable((ZERO, Unit(y_offset)), parent, total_length, Unit(110), break_threshold=Unit(300))
    staff_group = StaffGroup()
    
    # create staff objects
    Staff((ZERO, y_offset), flowable, total_length, staff_group, line_count=0) # additional staff is used to "lead" barlines
    right_staff = Staff((ZERO, y_offset + note_width(0.5)), flowable, total_length, staff_group, line_count=0)
    InstrumentName((right_staff.unit(-2), right_staff.center_y), right_staff, 'R', 'R', font=Font('Arial', Unit(10), weight=50))
    left_staff = Staff((ZERO, y_offset + note_height(1.5)), flowable, total_length, staff_group, line_count=0)
    InstrumentName((left_staff.unit(-2), left_staff.center_y), left_staff, 'L', 'L', font=Font('Arial', Unit(10), weight=50))
    Staff((ZERO, y_offset + note_height(2.0)), flowable, total_length, staff_group, line_count=0) # additional staff is used to "ground" barlines
    
    # render each line, ensuring measures fill to the end, unless rendering the final line
    x_offset = ZERO
    time_signature = None
    note_duration = None
    for line in lines:
      # calculate additional width to "inject" into each measure
      line_width = ZERO
      for measure in line:
        line_width += measure.get_width()
      added_width = (max_line_width - line_width) / len(line)
      
      # render each measure in the line
      for measure in line:
        # determine if a new time signature and/or note duration need to be rendered
        render_time_signature = (time_signature != measure.time_signature)
        time_signature = measure.time_signature
        render_note_duration = (note_duration != measure.note_duration)
        note_duration = measure.note_duration
        
        # render measure
        measure_width = measure.get_width()
        measure.draw(x_offset, measure_width + added_width, right_staff, left_staff, staff_group, render_note_duration, render_time_signature)
        x_offset += measure_width + added_width
      
    SystemLine(staff_group)   # Automatically adds barlines to the beginning of each line
    return flowable.canvas_pos().y + (flowable.height * len(lines)) + Unit(20)
  
  
class Voice:
  def __init__(self, name='', left_pattern=[], right_pattern=[], time_pattern=[], time_pattern_indices=[]):
    self.name = name
    self.left_pattern = left_pattern
    self.right_pattern = right_pattern
    self.time_pattern = time_pattern
    self.time_pattern_indices = time_pattern_indices
    
  def parse_hand_from_tree(tree, time_pattern, time_pattern_indices, hand_pattern, right_hand):
    for notation in tree.children:
      notation = notation.children[0]
      if notation.data.value == 'time_signature':
        time_pattern.append(TimeSignature.from_tree(notation))
        time_pattern_indices.append(len(hand_pattern))
      elif notation.data.value == 'note_duration':
        time_pattern.append(parse_duration(notation.children[0].value))
        time_pattern_indices.append(len(hand_pattern))
      elif notation.data.value == 'tuplet':
        tuplet = Tuplet.from_tree(notation, right_hand)
        hand_pattern.append(tuplet)
        for i in range(0, tuplet.duration - 1):
          hand_pattern.append(EmptyNote())
      elif notation.data.value == 'note_notation':
        hand_pattern.append(Note.from_tree(notation, right_hand))
    
  def from_tree(tree):
    voice = Voice('', [], [], [], [])
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
  def __init__(self, name=''):
    self.name = name
    
  def from_tree(tree):
    staff = ScoreStaff()
    for child in tree.children:
      if type(child) == Token:
        staff.name = parse_escaped_string(child.value)
    
    return staff

  
class Score:
  def __init__(self, header='', layout=[], voices=[], display=None):
    self.header = header
    self.layout = layout
    self.voices = voices
    self.display = display
    
  def from_tree(tree):
    score = Score('', [], [], None)
    for child in tree.children:
      for option in child.children:
        if option.data.value == 'score_header':
          score.header = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'score_layout':
          for staff_tree in option.children:
            score.layout.append(ScoreStaff.from_tree(staff_tree))
        elif option.data.value == 'score_voice':
          score.voices.append(Voice.from_tree(option))
          
    score.display = ScoreDisplay(score.voices, score.layout)
    return score
  
  def draw(self, y_pos):
    header_text = Text(Point(ZERO, y_pos + Unit(25)), None, self.header, font=Font('Arial', Unit(10), weight=80))
    return self.display.draw(Unit(25), header_text)