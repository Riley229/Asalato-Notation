from argparse import ArgumentParser
from neoscore.common import *
from notation_parser import parse_file

def main(args):
  # parse file into document data object
  document = parse_file(args.filename)
  
  # setup neoscore
  neoscore.setup()
  neoscore.document.paper = document.metadata.paper.create()
  
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