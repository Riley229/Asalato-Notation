from argparse import ArgumentParser
from neoscore.common import *
from neoscore.core import paper
from neoscore.western.rhythm_dot import RhythmDot
from notation_parser import parse_file
from components.document import PaperSize
from components.util import get_img_path, get_img_x_offset, get_img_y_offset, note_width, note_height, get_note_scale

def main(args):
  # parse file into document data object
  document = parse_file(args.filename)
  
  # setup neoscore
  neoscore.setup()
  if document.metadata.paper_size == PaperSize.Letter:
    neoscore.document.paper = paper.LETTER
  elif document.metadata.paper_size == PaperSize.A4:
    neoscore.document.paper = paper.A4
  
  # populate document with objects
  document.draw()
  
  # render document, either as pdf or in window
  if args.dest:
    neoscore.render_pdf(args.dest)
  else:
    neoscore.show()


if __name__ == "__main__":
  parser = ArgumentParser(prog='main.py', description='generate Asalato sheet music from text-based input files')
  parser.add_argument('filename', help='input file path')
  parser.add_argument('--dest', '-d', help='pdf output file path')
  args = parser.parse_args()
  main(args)