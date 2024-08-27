from argparse import ArgumentParser
from neoscore.common import *
from neoscore.core import paper
from neoscore.western.rhythm_dot import RhythmDot
from notation_parser import parse_file
from document import PaperSize
from util import get_img_path, get_img_x_offset, get_img_y_offset, note_width, note_height, get_note_scale

def main(args):
  # parse file into document data object
  data = parse_file(args.filename)
  
  # setup neoscore
  neoscore.setup()
  if data.metadata.paper_size == PaperSize.Letter:
    neoscore.document.paper = paper.LETTER
  elif data.metadata.paper_size == PaperSize.A4:
    neoscore.document.paper = paper.A4
  
  # populate document with objects
  current_y_pos = create_title_block(data.metadata.title, data.metadata.subtitle, data.metadata.composer)
  for score in data.scores:
    current_y_pos = create_score(score.header, score.layout, score.segments, current_y_pos)
  
  # render document, either as pdf or in window
  if args.dest:
    neoscore.render_pdf(args.dest)
  else:
    neoscore.show()
    
def create_title_block(title, subtitle, composer):
  half_paper_width = neoscore.document.paper.live_width / 2
  title_text = Text((half_paper_width, Unit(25)), None, title, alignment_x = AlignmentX.CENTER, font=Font('Arial', Unit(25)))
  subtitle_text = Text((ZERO, Unit(15)), title_text, subtitle, alignment_x = AlignmentX.CENTER, font=Font('Arial', Unit(10)))
  composer_text = Text((half_paper_width, ZERO), subtitle_text, composer, alignment_x = AlignmentX.RIGHT, font=Font('Arial', Unit(10)))

  return composer_text.canvas_pos().y
  
def create_score(header, layout, segments, starting_y_pos):
  length = (neoscore.document.paper.live_width - Unit(30)) * 3
  header_text = Text(Point(ZERO, starting_y_pos + Unit(25)), None, header, font=Font('Arial', Unit(10), weight=80))
  flowable = Flowable((ZERO, Unit(25)), header_text, length, Unit(110), break_threshold=Unit(300))
  staff_group = StaffGroup()
  
  staff_y_offset = Unit(25)
  for staff in layout:
    if staff.western_notation:
      staff_y_offset = create_western_staff(staff.name, staff.display_name, segments, staff_y_offset, flowable, staff_group)
    else:
      staff_y_offset = create_staff(staff.name, staff.display_name, segments, staff_y_offset, flowable, staff_group)
  
  SystemLine(staff_group)   # Automatically adds barlines to the beginning of each line
  return flowable.canvas_pos().y + flowable.height + Unit(50)

def create_staff(name, display_name, segments, y_offset, flowable, staff_group):
  length = (neoscore.document.paper.live_width - Unit(30)) * 3
  
  # create staff objects
  Staff((ZERO, y_offset), flowable, length * 3, staff_group, line_count=0) # additional staff is used to "lead" barlines
  right_staff_object = Staff((ZERO, y_offset + note_width(0.5)), flowable, length, staff_group, line_count=0)
  InstrumentName((right_staff_object.unit(-2), right_staff_object.center_y), right_staff_object, 'R', 'R', font=Font('Arial', Unit(10), weight=50))
  left_staff_object = Staff((ZERO, y_offset + note_height(1.5)), flowable, length, staff_group, line_count=0)
  InstrumentName((left_staff_object.unit(-2), left_staff_object.center_y), left_staff_object, 'L', 'L', font=Font('Arial', Unit(10), weight=50))
  Staff((ZERO, y_offset + note_height(2.0)), flowable, length, staff_group, line_count=0) # additional staff is used to "ground" barlines

  # populate with notes, time signatures, notations, etc.
  right_x_offset = Unit(10)
  left_x_offset = Unit(10)
  prev_time_signature = None
  prev_dot_value = None
  
  for segment in segments:
    notes_per_measure = segment.notes_per_measure()
    # display dot value
    if (segment.dot_value != None) and ((prev_dot_value == None) or (segment.dot_value.top_value != prev_dot_value.top_value) or (segment.dot_value.bottom_value != prev_dot_value.bottom_value)):
      MetronomeMark((right_x_offset, -note_height(0.5) - Unit(13)), right_staff_object, notehead_tables.STANDARD.short, '')
      Text((right_x_offset + Unit(12), -note_height(0.5) - Unit(10)), right_staff_object, '=')
      duration = Duration(segment.dot_value.top_value, segment.dot_value.bottom_value)
      create_note((right_x_offset + Unit(22), -note_height(0.5) - Unit(10)), duration, right_staff_object)
    # display time signature
    if (segment.time_signature != None) and ((prev_time_signature == None) or (segment.time_signature.top_value != prev_time_signature.top_value) or (segment.time_signature.bottom_value != prev_time_signature.bottom_value)):
      x_pos = right_x_offset
      if segment.dot_value != prev_dot_value:
        x_pos += Unit(50)
      meter = Meter.numeric(segment.time_signature.top_value, segment.time_signature.bottom_value)
      MusicText((x_pos, -note_height(0.5) - Unit(22)), right_staff_object, meter.upper_text_glyph_names[0])
      MusicText((x_pos, -note_height(0.5) - Unit(10)), right_staff_object, meter.lower_text_glyph_names[0])
      
    prev_dot_value = segment.dot_value
    prev_time_signature = segment.time_signature
    
    for voice in segment.voices:
      right_note = 0
      right_measure = 0
      left_note = 0
      left_measure = 0
      
      # skip if voice doesn't correspond to staff
      if voice.name != name:
        continue
      
      # populate right staff
      for note in voice.right_pattern:
        img_path = get_img_path(note, True)
        img_x_offset = get_img_x_offset(note, True)
        img_y_offset = get_img_y_offset(note, True)
        # render note
        Image((right_x_offset + img_x_offset, img_y_offset - note_height(0.5)), right_staff_object, img_path, scale=get_note_scale())
        right_x_offset += note_width()
        right_note += 1
        if right_note == notes_per_measure:
          # render barline (will go across both staves)
          Barline(right_x_offset + Unit(9), staff_group)
          right_note = 0
          right_measure += 1
          right_x_offset += Unit(20)
      
      # populate left staff
      for note in voice.left_pattern:
        img_path = get_img_path(note, False)
        img_x_offset = get_img_x_offset(note, False)
        img_y_offset = get_img_y_offset(note, False)
        # render note
        Image((left_x_offset + img_x_offset, img_y_offset - note_height(0.5)), left_staff_object, img_path, scale=get_note_scale())
        left_x_offset += note_width()
        left_note += 1
        if left_note == notes_per_measure:
          left_note = 0
          left_measure += 1
          left_x_offset += Unit(20)
          
      if (left_measure != right_measure) or (left_note != right_note):
        # TODO: better error handling
        print('ERROR: left/right voices have mismatching beats')
        return
      elif (right_note != 0):
        # TODO: better error handling
        print('ERROR: missing beats at end of final measure. Must be a full measure')
        return
  
  return y_offset + note_height(2.0) + Unit(20)

def create_note(position, duration, parent):
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

def create_western_staff(name, display_name, segments, y_offset, flowable, group):
  length = neoscore.document.paper.live_width - Unit(30)
  notation_x_offset = ZERO
  
  # create basic staff object
  staff_object = Staff((ZERO, y_offset), flowable, length * 3, group, line_count=1)
  Clef(ZERO, staff_object, 'percussion_1')
  if display_name:
    InstrumentName((staff_object.unit(-2), staff_object.center_y), staff_object, name, '', font=Font('Arial', Unit(10)))
    
  # populate with notes, time signatures, notations, etc.
  for segment in segments:
    # define time signature
    if segment.time_signature != None:
      TimeSignature(notation_x_offset, staff_object, (segment.time_signature.top_value, segment.time_signature.bottom_value))
      notation_x_offset += Unit(10)
 
  return y_offset + Unit(30)
  
if __name__ == "__main__":
  parser = ArgumentParser(prog='main.py', description='generate Asalato sheet music from text-based input files')
  parser.add_argument('filename', help='input file path')
  parser.add_argument('--dest', '-d', help='pdf output file path')
  args = parser.parse_args()
  main(args)