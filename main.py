import os
from entity import filterEntityFrames
from utils import writeToJSONFile, entityFramesToDict, doNLP, addSentences
from pprint import pprint

def main():
  FULL_TEXT_DIR = 'full_text'
  OUTPUT_FILE_NAME = 'entities2.json'
  OUTPUT_PATH = os.path.join( FULL_TEXT_DIR, OUTPUT_FILE_NAME )
  outputDict = []

  for filename in os.listdir( FULL_TEXT_DIR ):
      if filename.endswith(".txt"):
        path = os.path.join( FULL_TEXT_DIR, filename )
        print( 'Processing {fname}...'.format( fname=filename ))
        response = doNLP( path )
        entityFrames = response[ 'entities' ]
        sentenceFrames = response[ 'sentences' ][1:]
        entities = filterEntityFrames( entityFrames )
        entityDicts = entityFramesToDict( entities )
        addSentences( entityDicts, sentenceFrames )
        outputDict = outputDict + entityDicts
      else:
        continue

  writeToJSONFile( outputDict, OUTPUT_PATH )

main()

