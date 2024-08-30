from lark import Lark
from components.document import Document

notation_parser = Lark(r"""
    // Rules
    value : score* metadata? score*
    
    metadata : "\\meta" "{" meta_value* "}"
    meta_value : paper_format
               | title
               | subtitle
               | composer
               
    paper_format : "\\paper" "{" paper_option* "}"
    paper_option : paper_size
                 | paper_margin
                 | paper_margin_left
                 | paper_margin_right
                 | paper_margin_top
                 | paper_margin_bottom
              
    paper_size : "\\size" PAPERSIZE
    paper_margin : "\\margin" margin
    paper_margin_left : "\\marginLeft" margin
    paper_margin_right : "\\marginRight" margin
    paper_margin_top : "\\marginTop" margin
    paper_margin_bottom : "\\marginBottom" margin
    
    margin : (inch | millimeter)
    inch : FLOAT "in"
    millimeter : FLOAT "mm"
    
    title : "\\title" ESCAPED_STRING ("{" text_formatting? "}")?
    subtitle : "\\subtitle" ESCAPED_STRING ("{" text_formatting? "}")?
    composer : "\\composer" ESCAPED_STRING ("{" text_formatting? "}")?
    
    text_formatting : font? fontsize?
                    | fontsize font
    font : "\\font" ESCAPED_STRING
    fontsize : "\\fontSize" FLOAT
                    
    score : "\\score" "{" score_value* "}"
    score_value : score_header
                | score_layout
                | score_voice
                
    score_header : "\\header" ESCAPED_STRING ("{" text_formatting? "}")?
    score_notation_scale : "\\notationScale" FLOAT
    score_staff_spacing : "\\staffSpacing" FLOAT
    
    score_layout : "\\layout" "{" (staff | extend_last_line | notation_scale | staff_spacing)* "}"
    staff : "\\staff" ESCAPED_STRING
    extend_last_line : "\\extendLastLine"
    notation_scale : "\\notationScale" FLOAT
    staff_spacing : "\\staffSpacing" FLOAT
    
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
    
    note_notation : note note_modifier*
    
    note : flip
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
         
    note_modifier : knock
                  | accent
                  | staccato
                  | tenuto
                  | staccatissimo
                  | marcato
                  | marcato_staccato
                  | accent_staccato
                  | tenuto_staccato
                  | tenuto_accent
                  | stress
                  | unstress
                  | marcato_tenuto
                  | dynamic_pppppp
                  | dynamic_ppppp
                  | dynamic_pppp
                  | dynamic_ppp
                  | dynamic_pp
                  | dynamic_p
                  | dynamic_mp
                  | dynamic_mf
                  | dynamic_f
                  | dynamic_ff
                  | dynamic_fff
                  | dynamic_ffff
                  | dynamic_fffff
                  | dynamic_ffffff
                  
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
    flip_throw : "FI*" FLOAT
    flop_throw : "FO*" FLOAT
    airturn_throw : "AT*" FLOAT
    rest : "."
    shake : "|"
    catch : "x"
    
    // Asalato Modifiers
    knock : "\\knock"
    
    // Accidentals
    accent : "\\accent"
    staccato : "\\staccato"
    tenuto : "\\tenuto"
    staccatissimo : "\\staccatissimo"
    marcato : "\\marcato"
    marcato_staccato : "\\marcatoStaccato"
    accent_staccato : "\\accentStaccato"
    tenuto_staccato : "\\tenutoStaccato"
    tenuto_accent : "\\tenutoAccent"
    stress : "\\stress"
    unstress : "\\unstress"
    marcato_tenuto : "\\marcatoTenuto"
    
    // Dynamics
    dynamic_pppppp : "\\pppppp"
    dynamic_ppppp : "\\ppppp"
    dynamic_pppp : "\\pppp"
    dynamic_ppp : "\\ppp"
    dynamic_pp : "\\pp"
    dynamic_p : "\\p"
    dynamic_mp : "\\mp"
    dynamic_mf : "\\mf"
    dynamic_f : "\\f"
    dynamic_ff : "\\ff"
    dynamic_fff : "\\fff"
    dynamic_ffff : "\\ffff"
    dynamic_fffff : "\\fffff"
    dynamic_ffffff : "\\ffffff"
    
    // Terminals
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