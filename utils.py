import requests
import json

def pickEntityFields( entityFrame ):
  xref = entityFrame['xrefs'][0]
  entityType = entityFrame['type']
  text = entityFrame['text']
  return {
    'text': text,
    'xref_id': xref['id'],
    'namespace': xref['namespace'],
    'type': entityType
  }

def listToTsv( data, outfile ):
  with open( outfile, 'w' ) as file:
    for element in data:
      for entry in element:
        file.write(entry + '\t')
      file.write('\n')

def dictToJSON( data, outfile ):
  with open( outfile, 'w' ) as file:
    file.write( json.dumps( data, indent=True ) )

def entityFramesToList( entityFrames ):
  HEADERS = ['type', 'text', 'xref_namespace', 'xref_id']
  output = [ HEADERS ]
  for entityFrame in entityFrames:    
    fields = pickEntityFields( entityFrame )
    output.append( [ fields['type'], fields['text'], fields['namespace'], fields['xref_id'] ])
  return output

def entityFramesToDict( entityFrames ):
  output = []
  for entityFrame in entityFrames:    
    fields = pickEntityFields( entityFrame )
    output.append( fields )
  return output


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
  except:
    print( 'Error' )
  finally:
    print( 'HTTP Code: %s' % (r.status_code,) )