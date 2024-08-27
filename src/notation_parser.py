from lark import Lark
from document import Document, TimeSignature, PaperSize

notation_parser = Lark(r"""
    // Rules
    value : score* metadata? score*
    
    metadata : "\\meta" "{" meta_value* "}"
    meta_value : paper_size 
               | title 
               | subtitle
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
    segment_dot_value : "\\dotValue" TIME_SIGNATURE
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
    flip_grab : "FI+"
    flop_grab : "FO+"
    click_flip : "CI"
    click_flop : "CO"
    click_flip_grab : "CI+"
    click_flop_grab : "CO+"
    den_down : "DD"
    den_up : "DU"
    den_down_grab : "DD+"
    den_up_grab : "DU+"
    airturn : "AT"
    airturn_fake : "AF"
    flip_throw : "FI*(" FLOAT ")"
    flop_throw : "FO*(" FLOAT ")"
    airturn_throw : "AT*(" FLOAT ")"
    rest : "."
    shake : "|"
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
    return Document.from_tree(notation_tree)