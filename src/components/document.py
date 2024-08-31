from neoscore.common import *
from components.score import Score
from components.text import DocumentText
from components.util import parse_escaped_string, parse_margin


class DocumentPaper:
  def __init__(self, size='letter'):
    self.width = None
    self.height = None
    self.margin = None
    self.margin_left = None
    self.margin_right = None
    self.margin_top = None
    self.margin_bottom =None
    self.set_defaults(size)
    
  def set_defaults(self, size):
    if size == 'letter':
      self.width = self.width if (self.width != None) else Inch(8.5)
      self.height = self.height if (self.height != None) else Inch(11)
      self.margin = self.margin if (self.margin != None) else Inch(1)
    elif size == 'A4':
      self.width = self.width if (self.width != None) else Mm(210)
      self.height = self.height if (self.height != None) else Mm(297)
      self.margin = self.margin if (self.margin != None) else Mm(20)

  def from_tree(tree):
    document_paper = DocumentPaper()
    for option in tree.children:
      subtree = option.children[0]
      if subtree.data.value == 'paper_size':
        document_paper.set_defaults(subtree.children[0].value)
      elif subtree.data.value == 'paper_margin':
        document_paper.margin = parse_margin(subtree.children[0].children[0])
      elif subtree.data.value == 'paper_margin_left':
        document_paper.margin_left = parse_margin(subtree.children[0].children[0])
      elif subtree.data.value == 'paper_margin_right':
        document_paper.margin_right = parse_margin(subtree.children[0].children[0])
      elif subtree.data.value == 'paper_margin_top':
        document_paper.margin_top = parse_margin(subtree.children[0].children[0])
      elif subtree.data.value == 'paper_margin_bottom':
        document_paper.margin_bottom = parse_margin(subtree.children[0].children[0])
    return document_paper
  
  def get_margin_top(self):
    return self.margin_top if (self.margin_top != None) else self.margin
  
  def get_margin_right(self):
    return self.margin_right if (self.margin_right != None) else self.margin
  
  def get_margin_bottom(self):
    return self.margin_bottom if (self.margin_bottom != None) else self.margin
  
  def get_margin_left(self):
    return self.margin_left if (self.margin_left != None) else self.margin
  
  def create(self):
    return Paper(self.width, self.height, self.get_margin_top(), self.get_margin_right(), self.get_margin_bottom(), self.get_margin_left())


class Metadata:
  def __init__(self, paper=DocumentPaper(), title=DocumentText(), subtitle=DocumentText(), composer=DocumentText()):
    self.paper = paper
    self.title = title
    self.subtitle = subtitle
    self.composer = composer
    
  def from_tree(tree):
    metadata = Metadata(DocumentPaper(), '', '', '')
    for child in tree.children:
      for option in child.children:
        if option.data.value == 'paper_format':
          metadata.paper = DocumentPaper.from_tree(option)
        elif option.data.value == 'title':
          metadata.title = DocumentText.from_tree(option, 'Arial', Unit(25), 50, False)
          # metadata.title = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'subtitle':
          metadata.subtitle = DocumentText.from_tree(option, 'Arial', Unit(10), 50, False)
          # metadata.subtitle = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'composer':
          metadata.composer = DocumentText.from_tree(option, 'Arial', Unit(10), 50, False)
          # metadata.composer = parse_escaped_string(option.children[0].value)
          
    return metadata
  
  def draw(self):
    half_paper_width = neoscore.document.paper.live_width / 2
    title_text = self.title.draw((half_paper_width, self.title.font_size), None, AlignmentX.CENTER)
    # title_text = Text((half_paper_width, Unit(25)), None, self.title, alignment_x=AlignmentX.CENTER, font=Font('Arial', Unit(25)))
    subtitle_text = self.subtitle.draw((ZERO, Unit(5) + self.subtitle.font_size), title_text, AlignmentX.CENTER)
    # subtitle_text = Text((ZERO, Unit(15)), title_text, self.subtitle, alignment_x=AlignmentX.CENTER, font=Font('Arial', Unit(10)))
    composer_text = self.composer.draw((half_paper_width, ZERO), subtitle_text, AlignmentX.RIGHT)
    # composer_text = Text((half_paper_width, ZERO), subtitle_text, self.composer, alignment_x=AlignmentX.RIGHT, font=Font('Arial', Unit(10)))

    return composer_text.canvas_pos().y


class Document:
  def __init__(self, metadata=Metadata(), scores=[]):
    self.metadata = metadata
    self.scores = scores
    
  def from_tree(tree):
    document = Document()
    for child in tree.children:
      if child.data.value == 'metadata':
        document.metadata = Metadata.from_tree(child)
      elif child.data.value == 'score':
        document.scores.append(Score.from_tree(child))
        
    return document
  
  def draw(self):
    y_pos = self.metadata.draw()
    for score in self.scores:
      y_pos = score.draw(y_pos)