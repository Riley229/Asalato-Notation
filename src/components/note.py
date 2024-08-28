from neoscore.common import *
from neoscore.western import tuplet
from components.util import get_img_path, get_img_x_offset, get_img_y_offset, get_note_scale, note_height, note_width, get_data_type, get_glyph_id

class Note:
  def __init__(self, notation_id, right_hand, parameters=[], modifiers=[]):
    self.notation_id = notation_id
    self.right_hand = right_hand
    self.parameters = parameters
    self.modifiers = modifiers
    
  def from_tree(tree, right_hand):
    # parse regular note, along with any parameters
    note_tree = tree.children[0].children[0]
    note = Note(note_tree.data.value, right_hand, [], [])
    for param in note_tree.children:
      note.parameters.append(param.value)
    # parse note modifiers
    if len(tree.children) > 1:
      modifier_tree = tree.children[1]
      for modifier in modifier_tree.children:
        note.modifiers.append(modifier.data.value)
      
    return note
    
  def draw(self, pos_x, staff, western_staff, include_western_notation):
    if include_western_notation:
      Chordrest(pos_x + note_width(0.5), western_staff, ['b,'], Duration(1, 8))
      
    img_path = get_img_path('note', self.notation_id, self.right_hand)
    img_pos_x = pos_x + get_img_x_offset('note', self.notation_id, self.right_hand)
    img_pos_y = -note_height(0.5) + get_img_y_offset('note', self.notation_id, self.right_hand)
    Image((img_pos_x, img_pos_y), staff, img_path, scale=get_note_scale())
    
    if len(self.parameters) > 0:
      for parameter in self.parameters:
        # for now, the only parameter is text to display above note. May need to modify in future
        Text((pos_x + note_width(0.5), -note_height(0.5)), staff, parameter, alignment_x=AlignmentX.CENTER, font=Font('Arial', Unit(5)))
    
    if len(self.modifiers) > 0:
      for modifier in self.modifiers:
        modifier_type = get_data_type('modifier', modifier)
        if modifier_type == 'glyph':
          glyph_id = get_glyph_id('modifier', modifier, self.right_hand)
          MusicText((pos_x + note_width(0.5), -note_height(0.5)), staff, glyph_id, font=MusicFont('Bravura', Unit(5)))
        elif modifier_type == 'image':
          img_path = get_img_path('modifier', modifier, self.right_hand)
          img_pos_x = pos_x + get_img_x_offset('modifier', modifier, self.right_hand)
          img_pos_y = -note_height(0.5) + get_img_y_offset('modifier', modifier, self.right_hand)
          Image((img_pos_x, img_pos_y), staff, img_path, scale=get_note_scale())


class EmptyNote():
  def __init__(self):
    pass
    
  def draw(self, pos_x, staff, western_staff, include_western_notation):
    pass
    
    
class Tuplet:
  def __init__(self, right_hand, duration=1, notes=[]):
    self.right_hand = right_hand
    self.duration = duration
    self.notes = notes
    
  def from_tree(tree, right_hand):
    tuplet = Tuplet(right_hand, 1, [])
    for child in tree.children:
      component = child.children[0]
      if component.data.value == 'tuplet_duration':
        tuplet.duration = int(component.children[0].value)
      elif component.data.value == 'note_notation':
        tuplet.notes.append(Note.from_tree(component, right_hand))
      
    return tuplet
  
  def draw(self, pos_x, staff, western_staff, include_western_notation):
    tuple_note_count = len(self.notes)
    tuple_note_width = note_width() * (self.duration / tuple_note_count)

    if self.right_hand:
      tuplet.Tuplet((pos_x + note_width(0.5), -note_height(0.5)), staff, (tuple_note_width * (tuple_note_count - 1), ZERO), None, indicator_text=str(tuple_note_count), font=MusicFont('Bravura', Unit(5)), bracket_dir=DirectionY.UP)
      
    for note in self.notes:
      note.draw(pos_x, staff, western_staff, include_western_notation)
      pos_x += tuple_note_width