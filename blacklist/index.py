
import requests
import io
import csv
from urllib.parse import urlparse, urljoin, urlencode, urlunparse
from pprint import pprint

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

def build_url( baseurl, path, args_dict ):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list( urlparse( baseurl ) )
    url_parts[2] = path
    url_parts[4] = urlencode(args_dict)
    return urlunparse(url_parts)

def getTraverseValue( traverseJson ):
  output = None
  traverseEntry = traverseJson['traverseEntry'][0]
  rawValue = traverseEntry['value']
  if len( rawValue ) == 1:
    output = rawValue[0]
  else:
    output = rawValue
  return output

def doTraversal( path, uri ):
  urlPath = 'pc2/traverse'
  headers = {
    'Accept': 'application/json'
  }
  try:  
    queryParams = {
      'path': path,
      'uri': uri
    }
    objectUrl = build_url( PC_URL, urlPath, queryParams )
    r = requests.get( objectUrl, headers=headers )
    value = getTraverseValue( r.json() )
    return value
  except Exception as e:
    print( 'Error: {error}'.format( error=e ) )
  finally:
    print( 'HTTP Code: %s' % (r.status_code,) )


def getXrefInfo( uris ):  
  result = {}
  objectUri = 'http://pathwaycommons.org/pc11/SmallMolecule_d327c5852db5204a4ffb2bfa3a758f20'
  NAME_PATH = 'Entity/entityReference/name'
  XREF_BASE_PATH = 'Entity/entityReference/xref:UnificationXref/'
  xrefAttributes = [
    'db',
    'id'
  ]
  
  for xrefAttribute in xrefAttributes:
    xrefPath = urljoin( XREF_BASE_PATH, xrefAttribute )
    xrefValue = doTraversal( xrefPath, objectUri )
    result[xrefAttribute] = xrefValue

  nameValues = doTraversal( NAME_PATH, objectUri )
  result['names'] = nameValues
  return result


def makeBlacklist():
  # stream = fetchBlacklist()
  # uris = getURIs( stream, ('uri', 'h2', 'h3') )
  pprint( getXrefInfo( 'asd' ) )
