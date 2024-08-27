from lark import Lark
from components.document import Document

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
                | score_voice
                
    score_header : "\\header" ESCAPED_STRING
    score_layout : "\\layout" "{" staff* "}"

    staff : "\\staff" ESCAPED_STRING "{" staff_value* "}"
    staff_value : staff_display_name
                | staff_western_notation
                
    staff_display_name : "\\displayName" BOOLEAN
    staff_western_notation : "\\westernNotation" BOOLEAN
    
    score_voice : "\\voice" ESCAPED_STRING "{" voice_hand* "}"
    voice_hand : left_hand
               | right_hand
               
    left_hand : "\\left" "{" score_component* "}"
    right_hand : "\\right" "{" score_component* "}"
    
    score_component : time_signature
                    | note_duration
                    | tuplet
                    | note_notation
                  
    time_signature : "\\time" TIME_SIGNATURE
    note_duration : "\\dotValue" TIME_SIGNATURE
    tuplet : "\\tuplet" "{" tuplet_component* "}"
    tuplet_component : tuplet_duration
                     | note_notation
                     
    tuplet_duration: "\\duration" INTEGER
    
    note_notation : flip
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