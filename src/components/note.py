from neoscore.common import *
from neoscore.western import tuplet
from components.util import get_img_path, get_x_offset, get_y_offset, get_note_scale, note_height, note_width, get_data_type, get_glyph_id, get_y_alignment_offset, get_y_alignment

class Note:
  def __init__(self, notation_id, right_hand, parameters=[], modifiers=[]):
    self.notation_id = notation_id
    self.right_hand = right_hand
    self.parameters = parameters
    self.modifiers = modifiers
    
  def from_tree(tree, right_hand):
    note = None
    for option in tree.children:
      # parse regular note, along with any parameters
      if option.data.value == 'note':
        note = Note(option.children[0].data.value, right_hand, [], [])
        for param in option.children[0].children:
          note.parameters.append(param.value)
      # parse note modifiers
      elif option.data.value == 'note_modifier':
        note.modifiers.append(option.children[0].data.value)
      
    return note
  
  def get_width(self):
    return note_width()
  
  def get_top_padding(self):
    # for any articulations, add top padding in tuplets
    for modifier in self.modifiers:
      modifier_type = get_data_type('modifier', modifier)
      modifier_alignment = get_y_alignment('modifier', modifier, self.right_hand)
      if modifier_type == 'glyph' and modifier_alignment == 'top':
        return Unit(10)
    return ZERO
    
  def draw(self, pos_x, width, staff):
    offset_x = (width - self.get_width()) / 2
    img_path = get_img_path('note', self.notation_id, self.right_hand)
    img_pos_x = pos_x + get_x_offset('note', self.notation_id, self.right_hand) + offset_x
    img_pos_y = get_y_offset('note', self.notation_id, self.right_hand)
    Image((img_pos_x, img_pos_y), staff, img_path, scale=get_note_scale())
    
    for parameter in self.parameters:
      # for now, the only parameter is text to display above note. May need to modify in future
      Text((pos_x + (width / 2), -note_height(0.5) - Unit(2)), staff, parameter, alignment_x=AlignmentX.CENTER, font=Font('Arial', Unit(7)))
    
    for modifier in self.modifiers:
      # handle modifier glyphs (articulations, dynamics)
      modifier_type = get_data_type('modifier', modifier)
      if modifier_type == 'glyph':
        glyph_id = get_glyph_id('modifier', modifier, self.right_hand)
        glyph_pos_x = pos_x + get_x_offset('modifier', modifier, self.right_hand) + offset_x
        glyph_pos_y = get_y_offset('modifier', modifier, self.right_hand)
        glyph_alignment = get_y_alignment('modifier', modifier, self.right_hand)
        glyph = MusicText((glyph_pos_x, glyph_pos_y), staff, glyph_id, font=MusicFont('Bravura', Unit(4)), alignment_x=AlignmentX.CENTER)
        if glyph_alignment == 'bottom':
          glyph.y += glyph.music_chars[0].bounding_rect.height
      # handle modifier images (knocks) -> all images "hug" notes for now
      elif modifier_type == 'image':
        img_path = get_img_path('modifier', modifier, self.right_hand)
        img_pos_x = pos_x + get_x_offset('modifier', modifier, self.right_hand) + offset_x
        img_pos_y = get_y_alignment_offset('note', self.notation_id, 'modifier', modifier, self.right_hand)
        Image((img_pos_x, img_pos_y), staff, img_path, scale=get_note_scale())


class EmptyNote():
  def __init__(self):
    pass
  
  def get_width(self):
    return ZERO
  
  def get_top_padding(self):
    return ZERO
    
  def draw(self, pos_x, width, staff):
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
  
  def get_width(self):
    if len(self.notes) == 0:
      return ZERO
    
    note_width = self.notes[0].get_width()
    return note_width * (len(self.notes) / self.duration)
  
  def draw(self, pos_x, width, staff):
    tuple_note_count = len(self.notes)
    tuple_note_width = (width * self.duration)  / tuple_note_count
    tuple_start_x = pos_x
    top_padding = ZERO

    for note in self.notes:
      if note.get_top_padding() > top_padding:
        top_padding = note.get_top_padding()
      note.draw(pos_x, tuple_note_width, staff)
      pos_x += tuple_note_width
      
    if self.right_hand:      
      tuple_bar_width = tuple_note_width * (tuple_note_count - 1)
      tuplet.Tuplet((tuple_start_x + (tuple_note_width / 2), -note_height(0.5) - top_padding), staff, (tuple_bar_width, ZERO), None, indicator_text=str(tuple_note_count), font=MusicFont('Bravura', Unit(4)), bracket_dir=DirectionY.UP)