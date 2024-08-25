from lark import Lark
from lark.lexer import Token
from Document import Document, Score, Staff, ScoreSegment, Voice, TimeSignature, PaperSize

notation_parser = Lark(r"""
    // Rules
    value : score* metadata? score*
    
    metadata : "\\meta" "{" meta_value* "}"
    meta_value : paper_size 
               | title 
               | subtitle \
              | composer
              
    paper_size : "\\papersize" PAPERSIZE
    title : "\\title" ESCAPED_STRING
    subtitle : "\\subtitle" ESCAPED_STRING
    composer : "\\composer" ESCAPED_STRING
                    
    score : "\\score" "{" score_value* "}"
    score_value : score_header 
                | score_layout 
                | score_segment
                
    score_header : "\\header" ESCAPED_STRING
    score_layout : "\\layout" "{" staff* "}"
    score_segment : "\\segment" "{" segment_value* "}"

    staff : "\\staff" ESCAPED_STRING "{" staff_value* "}"
    staff_value : staff_display_name
                | staff_western_notation
                
    staff_display_name : "\\displayName" BOOLEAN
    staff_western_notation : "\\westernNotation" BOOLEAN
    
    segment_value : segment_time
                  | segment_dot_value
                  | segment_voice
                  
    segment_time : "\\time" TIME_SIGNATURE
    segment_dot_value : "\\dotValue" INTEGER
    segment_voice : "\\voice" ESCAPED_STRING "{" voice_component* "}"
    
    voice_component : left_voice_component
                    | right_voice_component
                    
    left_voice_component : "\\left" "{" notation* "}"
    right_voice_component : "\\right" "{" notation* "}"
    
    notation : flip
             | flop
             | flip_grab
             | flop_grab
             | click_flip
             | click_flop
             | click_flip_grab
             | click_flop_grab
             | den_down
             | den_up
             | den_down_grab
             | den_up_grab
             | airturn
             | airturn_fake
             | flip_throw
             | flop_throw
             | airturn_throw
             | rest
             | shake
             | catch
    
    // Asalato Notations
    flip : "FI"
    flop : "FO"
    flip_grab : "FI\+"
    flop_grab : "FO\+"
    click_flip : "CI"
    click_flop : "CO"
    click_flip_grab : "FI\+"
    click_flop_grab : "FO\+"
    den_down : "DD"
    den_up : "DU"
    den_down_grab : "DD\+"
    den_up_grab : "DU\+"
    airturn : "AT"
    airturn_fake : "AF"
    flip_throw : "FI\*\(" FLOAT "\)"
    flop_throw : "FO\*\(" FLOAT "\)"
    airturn_throw : "AT\*\(" FLOAT "\)"
    rest : "."
    shake : "\|"
    catch : "x"
    
    // Terminals
    BOOLEAN : "true" | "false"
    INTEGER : /[0-9]+/
    FLOAT : /[0-9]+[.]?[0-9]*/
    COMMENT : "#" /[^\n]*/ "\n"
    PAPERSIZE : "letter" | "A4"
    TIME_SIGNATURE : /[0-9]+\/[0-9]+/
    
    // Lark
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
    %ignore COMMENT
    """, start='value')

def parse_file(filename):
  with open(filename) as file:
    notation_tree = notation_parser.parse(file.read())
    document = Document()
    for child in notation_tree.children:
      if child.data.value == 'metadata':
        parse_meta(child, document)
      elif child.data.value == 'score':
        parse_score(child, document)
    
def parse_meta(meta_tree, document):
  for child in meta_tree.children:
    for option in child.children:
      if option.data.value == 'paper_size':
        document.metadata.papersize = parse_papersize(option.children[0].value)
      elif option.data.value == 'title':
        document.metadata.title = parse_escaped_string(option.children[0].value)
      elif option.data.value == 'subtitle':
        document.metadata.subtitle = parse_escaped_string(option.children[0].value)
      elif option.data.value == 'composer':
        document.metadata.composer = parse_escaped_string(option.children[0].value)

def parse_score(score_tree, document):
  score = Score()
  for child in score_tree.children:
    for option in child.children:
      if option.data.value == 'score_header':
        score.header = parse_escaped_string(option.children[0].value)
      elif option.data.value == 'score_layout':
        parse_score_layout(option, score)
      elif option.data.value == 'score_segment':
        parse_score_segment(option, score)
        
  document.scores.append(score)
  
def parse_score_layout(layout_tree, score):
  for staff_tree in layout_tree.children:
    staff = Staff()
    for child in staff_tree.children:
      if type(child) == Token:
        staff.name = child.value
      else:
        for option in child.children:
          if option.data.value == 'staff_display_name':
            staff.display_name = parse_boolean(option.children[0].value)
          elif option.data.value == 'staff_western_notation':
            staff.western_notation = parse_boolean(option.children[0].value)
    score.layout.append(staff)
  
def parse_score_segment(segment_tree, score):
  segment = ScoreSegment()
  for child in segment_tree.children:
    for option in child.children:
      if option.data.value == 'segment_time':
        segment.time_signature = parse_time_signature(option.children[0].value)
      elif option.data.value == 'segment_dot_value':
        segment.dot_value = int(option.children[0].value)
      elif option.data.value == 'segment_voice':
        parse_score_segment_voice(option, segment)
        
  score.segments.append(segment)
        
def parse_score_segment_voice(voice_tree, segment):
  voice = Voice()
  for child in voice_tree.children:
    if type(child) == Token:
      voice.name = child.value
    else:
      for option in child.children:
        if option.data.value == 'right_voice_component':
          for notation in option.children:
            voice.right_pattern.append(notation.children[0].data.value)
        elif option.data.value == 'left_voice_component':
          for notation in option.children:
            voice.left_pattern.append(notation.children[0].data.value)
    
  segment.voices.append(voice)
  
def parse_papersize(str):
  if str == 'letter':
    return PaperSize.Letter
  else:
    return PaperSize.A4

def parse_time_signature(str):
  time = TimeSignature()
  components = str.split('/')
  time.top_value = int(components[0])
  time.bottom_value = int(components[1])
  
def parse_boolean(str):
  if str == 'true':
    return True
  else:
    return False
  
def parse_escaped_string(str):
  return str[1:-1]

parse_file('../examples/test')