
import requests
import io
import csv
from urllib.parse import urlparse, urljoin, urlencode, urlunparse
from pprint import pprint
from utils import writeToJSONFile

PC_URL = 'https://www.pathwaycommons.org/'
  

def asStream( data ):
  return io.StringIO( data ) 

def getURIs( dataStream, headers ):
  reader = csv.DictReader( dataStream, delimiter='\t', fieldnames=headers ) # OrderedDict
  return [ entry['uri'] for entry in reader ]

# Fetch from PC
def fetchBlacklist( path = 'archives/PC2/v11/blacklist.txt' ):
  BLACKLIST_URL = urljoin( PC_URL, path )
  headers = {
    'Accept': 'text/plain'
  }
  
  try:
    r = requests.get( BLACKLIST_URL, headers=headers )
    return asStream( r.text )
  except Exception as e:
    print( 'Error: {error}'.format( error=e ) )
  finally:
    print( 'HTTP Code: %s' % (r.status_code,) )

def getEntryValue( traverseEntry, first=False ):
  value=traverseEntry['value']
  if first:
    value=value[0]
  return value  

def getTraverseEntries( traverseJson ):
  return traverseJson['traverseEntry']

def doTraversal( path, uris ):
  urlPath = 'pc2/traverse'
  headers = {
    'Accept': 'application/json'
  }
  try:  
    queryParams = {
      'path': path,
      'uri': ','.join( uris )
    }
    url = urljoin( PC_URL, urlPath )
    r = requests.post( url, headers=headers, data=queryParams )
    entries = getTraverseEntries( r.json() )
    return entries
  except Exception as e:
    print( 'Error: {error}'.format( error=e ) )
  # finally:
  #   print( 'HTTP Code: %s' % (r.status_code,) )

def fillInValues( output, entries, attribute ):
  for entry in entries:
    uri = entry['uri']
    value = getEntryValue( entry )
    if len( value ) == 0:
      continue
    match = next( ( d for d in output if d['uri'] == uri ), None )
    if match:
      match[attribute]=value
    else:
      output.append({ 
        'uri': uri, 
        attribute: value 
      })

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def getXrefInfo( uris ):
  result = []
  NAME_PATH = 'Entity/entityReference/name'
  XREF_BASE_PATH = 'Entity/entityReference/xref:UnificationXref/'
  xrefAttributes = [  
    'id',
    'db'
  ]
  uriChunks = list( chunks( uris, 100 ) )
  
  for uriChunk in uriChunks:
    for xrefAttribute in xrefAttributes:
      xrefPath = urljoin( XREF_BASE_PATH, xrefAttribute )
      xrefEntries = doTraversal( xrefPath, uriChunk )
      fillInValues( result, xrefEntries, xrefAttribute )

    nameEntries = doTraversal( NAME_PATH, uriChunk )
    fillInValues( result, nameEntries, 'names' )
  return result

def filterXrefInfo( xrefInfo ):
  filtered = []
  for entry in xrefInfo:
    

def makeBlacklist():
  stream = fetchBlacklist()
  uris = getURIs( stream, ('uri', 'h2', 'h3') )[:100]
  print( 'number of items: {num}'.format(num=len(uris)) )
  rawXrefInfo = getXrefInfo( uris )
  xrefInfo = filterXrefInfo( rawXrefInfo )
  writeToJSONFile( xrefInfo, 'blacklist.json' )
