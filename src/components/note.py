from neoscore.common import *
from neoscore.western import tuplet
from components.util import get_img_path, get_img_x_offset, get_img_y_offset, get_note_scale, note_height, note_width

class Note:
  def __init__(self, notation_id, right_hand, parameters=[]):
    self.notation_id = notation_id
    self.right_hand = right_hand
    self.parameters = parameters
    
  def from_tree(tree, right_hand):
    note = Note(tree.data.value, right_hand)
    for param in tree.children:
      note.parameters.append(param.value)
      
    return note
    
  def draw(self, pos_x, staff):
    img_path = get_img_path(self.notation_id, self.right_hand)
    pos_x = pos_x + get_img_x_offset(self.notation_id, self.right_hand)
    pos_y = -note_height(0.5) + get_img_y_offset(self.notation_id, self.right_hand)
    
    Image((pos_x, pos_y), staff, img_path, scale=get_note_scale())


class EmptyNote():
  def __init__(self):
    self.empty = True
    
  def draw(self, pos_x, staff):
    self.empty = True
    
    
class Tuplet:
  def __init__(self, right_hand, duration=1, notes=[]):
    self.right_hand = right_hand
    self.duration = duration
    self.notes = notes
    
  def draw(self, pos_x, staff):
    tuple_note_count = len(self.notes)
    tuple_note_width = note_width() * (self.duration / tuple_note_count)

    if self.right_hand:
      tuplet.Tuplet((pos_x + note_width(0.5), -note_height(0.5)), staff, (tuple_note_width * (tuple_note_count - 1), ZERO), None, indicator_text=str(tuple_note_count), font=MusicFont('Bravura', Unit(5)), bracket_dir=DirectionY.UP)
      
    for note in self.notes:
      note.draw(pos_x, staff)
      pos_x += tuple_note_width
    
  def from_tree(tree, right_hand):
    tuplet = Tuplet(right_hand, 1, [])
    for child in tree.children:
      component = child.children[0]
      if component.data.value == 'tuplet_duration':
        tuplet.duration = int(component.children[0].value)
      elif component.data.value == 'note_notation':
        tuplet.notes.append(Note.from_tree(component.children[0], right_hand))
      
    return tuplet