from neoscore.common import *
from neoscore.core import paper
from components.score import Score
from components.util import parse_escaped_string, parse_paper_size


class Metadata:
  def __init__(self, paper_size=paper.LETTER, title='', subtitle='', composer=''):
    self.paper_size = paper_size
    self.title = title
    self.subtitle = subtitle
    self.composer = composer
    
  def from_tree(tree):
    metadata = Metadata()
    for child in tree.children:
      for option in child.children:
        if option.data.value == 'paper_size':
          metadata.papersize = parse_paper_size(option.children[0].value)
        elif option.data.value == 'title':
          metadata.title = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'subtitle':
          metadata.subtitle = parse_escaped_string(option.children[0].value)
        elif option.data.value == 'composer':
          metadata.composer = parse_escaped_string(option.children[0].value)
          
    return metadata
  
  def draw(self):
    half_paper_width = neoscore.document.paper.live_width / 2
    title_text = Text((half_paper_width, Unit(25)), None, self.title, alignment_x=AlignmentX.CENTER, font=Font('Arial', Unit(25)))
    subtitle_text = Text((ZERO, Unit(15)), title_text, self.subtitle, alignment_x=AlignmentX.CENTER, font=Font('Arial', Unit(10)))
    composer_text = Text((half_paper_width, ZERO), subtitle_text, self.composer, alignment_x=AlignmentX.RIGHT, font=Font('Arial', Unit(10)))

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