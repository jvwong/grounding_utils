from collections import OrderedDict

ENTITY_TYPES = set([
  'simple-chemical',
  'gene-or-gene-product',
  'protein'
])

def pickUnique( entities ):
  return list( OrderedDict( [ (e['xref_id'] + e['namespace'], e) for e in entities ] ).values() )

def filterByType( entityFrames ):
  output = []
  ids = set()
  for frame in entityFrames:
    entityType = frame['type']
    xref_id = frame['xrefs'][0]['id']
    
    if entityType in ENTITY_TYPES and xref_id not in ids:
      ids.add( xref_id )
      output.append( frame )
      
  return output