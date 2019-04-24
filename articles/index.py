import os
from pprint import pprint

from articles.entity import filterByType, pickUnique
from articles.utils import entityFramesToDict, doNLP, addSentences
from utils import writeToJSONFile

ARTICLES = [
  { 
    'doi': 'http://dx.doi.org/10.1016/j.molcel.2017.01.019',
    'location': 'full_text/clarke.txt'  
  },
  { 
    'doi': 'http://dx.doi.org/10.1016/j.molcel.2016.12.018',
    'location': 'full_text/godfrey.txt'  
  },
  { 
    'doi': 'https://doi.org/10.1016/j.molcel.2018.04.024',
    'location': 'full_text/he.txt'  
  },
  { 
    'doi': 'http://dx.doi.org/10.1016/j.molcel.2016.11.034',
    'location': 'full_text/jeong.txt'  
  },
  { 
    'doi': 'https://doi.org/10.1016/j.molcel.2017.11.025',
    'location': 'full_text/jin.txt'  
  },
  { 
    'doi': 'http://dx.doi.org/10.1016/j.molcel.2017.02.016',
    'location': 'full_text/liu.txt'  
  },
  { 
    'doi': 'http://dx.doi.org/10.1016/j.molcel.2017.01.027',
    'location': 'full_text/qian.txt'  
  },
  { 
    'doi': 'https://doi.org/10.1016/j.molcel.2018.08.014',
    'location': 'full_text/sang.txt'  
  },
  { 
    'doi': 'http://dx.doi.org/10.1016/j.molcel.2016.12.021',
    'location': 'full_text/willemsen.txt'  
  },
  { 
    'doi': 'https://doi.org/10.1016/j.molcel.2011.01.014',
    'location': 'full_text/wong.txt'  
  },
  { 
    'doi': 'http://dx.doi.org/10.1016/j.molcel.2013.11.004',
    'location': 'full_text/yang.txt'  
  }
]

def scrapeArticleEntities():
  currentDir = os.path.dirname(os.path.realpath(__file__))
  outPath = os.path.join( currentDir, 'entities.json' )
  results = []
  for article in ARTICLES:
    path = os.path.join( currentDir, article[ 'location' ])
    print( 'Processing {name}...'.format( name=path ) )
    response = doNLP( path )
    entityFrames = response[ 'entities' ]
    sentenceFrames = response[ 'sentences' ][1:]
    entities = filterByType( entityFrames )
    entityDicts = entityFramesToDict( entities )
    addSentences( entityDicts, sentenceFrames )
    output = {
      'id': article[ 'doi' ],
      'entities' : pickUnique( entityDicts )
    }
    results.append( output )
    print( 'Finished {name}...'.format( name=path ) )    
    
  writeToJSONFile( results, outPath )