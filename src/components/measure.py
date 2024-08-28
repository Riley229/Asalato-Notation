import neoscore.western.time_signature as time_signature

from neoscore.common import *
from neoscore.western.rhythm_dot import RhythmDot
from components.util import note_width, note_height

class Measure:
  def __init__(self, time_signature, note_duration, right_pattern=[], left_pattern=[]):
    self.time_signature = time_signature
    self.note_duration = note_duration
    self.right_pattern = right_pattern
    self.left_pattern = left_pattern
    
  def expected_note_count(self):
    return (self.time_signature.beats_per_measure() * (self.note_duration.fraction.denominator / self.note_duration.fraction.numerator)) / 4
  
  def minimum_width(self):
    return len(self.right_pattern) * note_width()
    
  def draw(self, pos_x, right_staff, left_staff, western_staff, staff_group, render_note_duration, render_time_signature, include_western_notation):
    if render_note_duration:
      MetronomeMark((pos_x, -note_height(0.5) - Unit(13)), right_staff, notehead_tables.STANDARD.short, '')
      Text((pos_x + Unit(12), -note_height(0.5) - Unit(10)), right_staff, '=')
      create_metronome_note((pos_x + Unit(22), -note_height(0.5) - Unit(10)), self.note_duration, right_staff)
      
    if render_time_signature:
      time_signature_pos_x = pos_x
      if render_note_duration:
        time_signature_pos_x += Unit(50)
      meter = Meter.numeric(self.time_signature.top_value, self.time_signature.bottom_value)
      MusicText((time_signature_pos_x, -note_height(0.5) - Unit(22)), right_staff, meter.upper_text_glyph_names[0])
      MusicText((time_signature_pos_x, -note_height(0.5) - Unit(10)), right_staff, meter.lower_text_glyph_names[0])
      if include_western_notation:
        time_signature.TimeSignature(pos_x, western_staff, (self.time_signature.top_value, self.time_signature.bottom_value))
    
    for i in range(0, len(self.right_pattern)):
      self.right_pattern[i].draw(pos_x, right_staff, western_staff, include_western_notation)
      self.left_pattern[i].draw(pos_x, left_staff, western_staff, include_western_notation)      
      pos_x += note_width()

    Barline(pos_x, staff_group)    
    
def create_metronome_note(position, duration, parent):
  notehead = notehead_tables.STANDARD.lookup_duration(duration.display.base_duration)
  notehead_object = MetronomeMark(position, parent, notehead, '')
  if duration.display.requires_stem:
    stem = Stem((Unit(5.5), ZERO), notehead_object, DirectionY.UP, Unit(20))
  if duration.display.flag_count:
    Flag((stem.pen.thickness / -2, ZERO), stem.end_point, duration, stem.direction)
  dot_start_x = Unit(8)
  for i in range(duration.display.dot_count):
    RhythmDot((dot_start_x, ZERO), notehead_object)
    dot_start_x += Unit(4)
    
    
class TimeSignature:
  def __init__(self, top_value=4, bottom_value=4):
    self.top_value = top_value
    self.bottom_value = bottom_value
    
  def beats_per_measure(self):
    return self.top_value * (4 / self.bottom_value)
  
  def from_tree(tree):
    components = tree.children[0].value.split('/')
    return TimeSignature(int(components[0]), int(components[1]))