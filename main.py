import os
from entity import filterEntities
from utils import dictToJSON, entityFramesToDict, doNLP
from pprint import pprint

def main():
  FULL_TEXT_DIR = 'full_text'
  OUTPUT_FILE_NAME = 'entities.txt'
  OUTPUT_PATH = os.path.join( FULL_TEXT_DIR, OUTPUT_FILE_NAME )
  entityFrames = []
  for filename in os.listdir( FULL_TEXT_DIR ):
      if filename.endswith(".txt"):
        path = os.path.join( FULL_TEXT_DIR, filename )
        response = doNLP( path )
        entityFrames = entityFrames + response[ 'entities' ]
      else:
        continue
  entities = filterEntities( entityFrames )
  data = entityFramesToDict( entities )
  dictToJSON( data, OUTPUT_PATH )

main()

