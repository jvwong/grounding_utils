ENTITY_TYPES = set([
  "simple-chemical"
])

def filterEntities( entityFrames ):
  output = []
  ids = set()
  for frame in entityFrames:
    entityType = frame['type']
    xref_id = frame['xrefs'][0]['id']
    
    if entityType in ENTITY_TYPES and xref_id not in ids:
      ids.add( xref_id )
      output.append( frame )
      
  return output