import os
from entity import filterByType, pickUnique
from utils import writeToJSONFile, entityFramesToDict, doNLP, addSentences
from pprint import pprint
    
def scrapeArticleEntities( inDir, outPath ):
  results = []
  for filename in os.listdir( inDir ):
      if filename.endswith(".txt"):
        path = os.path.join( inDir, filename )
        print( 'Processing {fname}...'.format( fname=filename ))
        response = doNLP( path )
        entityFrames = response[ 'entities' ]
        sentenceFrames = response[ 'sentences' ][1:]
        entities = filterByType( entityFrames )
        entityDicts = entityFramesToDict( entities )
        addSentences( entityDicts, sentenceFrames )
        results = results + entityDicts
      else:
        continue

  output = pickUnique( results ) 
  writeToJSONFile( output, outPath )

def main():
  FULL_TEXT_DIR = 'full_text'
  OUTPUT_FILE_NAME = 'entities.json'
  OUTPUT_PATH = os.path.join( FULL_TEXT_DIR, OUTPUT_FILE_NAME )

  scrapeArticleEntities( FULL_TEXT_DIR, OUTPUT_PATH )

main()

