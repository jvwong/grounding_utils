import requests

# Send to Reach
def makeRequest( filename = 'test.txt' ):
  REACH_URL = 'http://reach.baderlab.org/api/uploadFile'
  files = {'file': open(filename,'rb')}
  headers = {
    'Accept': 'application/json'
  }
  data = {'output': 'fries'}

  try:
    r = requests.post(REACH_URL, headers=headers, files=files, data=data)
    print('HTTP Code: %s' % (r.status_code,))
    response = r.json() #dict
    events = response['events']['frames']
    entities = response['entities']['frames']
    return {'events': events, 'entities': entities}
  except:
    print('Error')

def getChemicals( entityFrames ):
  TYPE_CHEMICAL = "simple-chemical"
  output = []
  ids = set()
  for frame in entityFrames:
    type = frame['type']
    xref = frame['xrefs'][0]
    xref_id = xref['id']
    if type == TYPE_CHEMICAL and xref_id not in ids:
      ids.add(xref_id)
      output.append(frame)
  return output

def entityFramesToList( entityFrames ):
  HEADERS = ['type', 'text', 'xref_namespace', 'xref_id']
  output = [ HEADERS ]
  for entityFrame in entityFrames:
    xref = entityFrame['xrefs'][0]
    type = entityFrame['type']
    text = entityFrame['text']
    output.append([ type, text, xref['namespace'], xref['id'] ])
  return output

def listToTsv( list, outfile ):
  with open(outfile, 'w') as file:
    for element in list:
      for entry in element:
        file.write(entry + '\t')
      file.write('\n')

def main():
  response = makeRequest( 'he_molcell.txt' )
  chemicals = getChemicals( response['entities'] )
  asList = entityFramesToList( chemicals )
  listToTsv( asList, 'chemicals.txt' )


main()

