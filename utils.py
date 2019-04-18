import json

def writeToJSONFile( data, outfile ):
  with open( outfile, 'w' ) as file:
    file.write( json.dumps( data, indent=True ) )