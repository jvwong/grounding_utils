def getChemicals( entityFrames ):
  TYPE_CHEMICAL = "simple-chemical"
  output = []
  ids = set()
  for frame in entityFrames:
    type = frame['type']
    xref = frame['xrefs'][0]
    xref_id = xref['id']
    if type == TYPE_CHEMICAL and xref_id not in ids:
      ids.add( xref_id )
      output.append( frame )
  return output