import os
from chemicals import getChemicals
from utils import listToTsv, entityFramesToList, doNLP

def main():
  FULL_TEXT_DIR = 'full_text'
  OUTPUT_FILE_NAME = 'chemicals.txt'
  OUTPUT_PATH = os.path.join( FULL_TEXT_DIR, OUTPUT_FILE_NAME )
  entityFrames = []
  for filename in os.listdir( FULL_TEXT_DIR ):
      if filename.endswith(".txt"):
        path = os.path.join( FULL_TEXT_DIR, filename )
        response = doNLP( path )
        entityFrames = entityFrames + response[ 'entities' ]
      else:
        continue
  chemicals = getChemicals( entityFrames )
  asList = entityFramesToList( chemicals )
  listToTsv( asList, OUTPUT_PATH )

main()

