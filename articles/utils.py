import requests

def pickEntityFields( entityFrame ):
  xref = entityFrame['xrefs'][0]
  entityType = entityFrame['type']
  text = entityFrame['text']
  sentence_id = entityFrame['sentence']
  return {
    'text': text,
    'xref_id': xref['id'],
    'namespace': xref['namespace'],
    'type': entityType,
    'sentence_id': sentence_id
  }

def entityFramesToDict( entityFrames ):
  output = []
  for entityFrame in entityFrames:
    entityFields = pickEntityFields( entityFrame )
    output.append( entityFields )
  return output

def addSentences( entityDicts, sentenceFrames ):
  for entityDict in entityDicts:
    entityDict['sentence'] = next(sentence['text'] for sentence in sentenceFrames if sentence['frame-id'] == entityDict['sentence_id'])
    del entityDict['sentence_id']

# Send to Reach
def doNLP( filename = 'test.txt' ):
  REACH_URL = 'http://reach.baderlab.org/api/uploadFile'
  files = {'file': open(filename,'rb')}
  headers = {
    'Accept': 'application/json'
  }
  data = {'output': 'fries'}

  try:
    r = requests.post( REACH_URL, headers=headers, files=files, data=data )
    response = r.json() #dict
    events = response['events']['frames']
    entities = response['entities']['frames']
    sentences = response['sentences']['frames']
    return {
      'events': events,
      'entities': entities,
      'sentences': sentences
    }
  except Exception as e:
    print( 'Error: {error}'.format( error=e ) )
  finally:
    print( 'HTTP Code: %s' % (r.status_code,) )