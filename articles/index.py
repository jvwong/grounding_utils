import os
from pprint import pprint

from articles.entity import filterByType, pickUnique
from articles.utils import writeToJSONFile, entityFramesToDict, doNLP, addSentences
    
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