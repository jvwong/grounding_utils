import ftplib
import zlib
import io
import csv

from utils import writeToJSONFile

# Fetch from NCBI FTP site
def fetchFTPZip( archiveDir, archiveFile, outfile ):
  NCBI_FTP_URL = 'ftp.ncbi.nlm.nih.gov'
  USER='anonymous'
  PASSWORD='user@email.com'
  decomp = zlib.decompressobj( 16+zlib.MAX_WBITS )

  try:
    ftp = ftplib.FTP( NCBI_FTP_URL )
    ftp.login( user=USER, passwd=PASSWORD )
    ftp.cwd( archiveDir )

    with open( outfile, 'wb' ) as localfile:
      def next_packet( data ):
        localfile.write( decomp.decompress( data ) )
      ftp.retrbinary( 'RETR ' + archiveFile, next_packet )
      ftp.quit()

  except Exception as e:
    print( 'Error: {error}'.format( error=e ) )

def updateCounts( counts, entry ):
  tax_id = entry['tax_id']
  geneID = entry['GeneID']
  pubMed_ID = entry['PubMed_ID']
  if tax_id in counts:
    if geneID in counts[tax_id]:
      counts[tax_id][geneID].append( pubMed_ID )
    else:
      counts[tax_id][geneID] = [ pubMed_ID ]
  else:
    counts[tax_id] = { geneID: [ pubMed_ID ] }


def pubsByOrganism( dataStream, taxons, headers ):
  counts = {}
  reader = csv.DictReader( dataStream, delimiter='\t', fieldnames=headers ) # OrderedDict
  for entry in reader:
    if entry['tax_id'] in taxons:
      updateCounts( counts, entry )
  return counts

def getDataStream( path ):
  with open( path, 'r' ) as localfile:
    return io.StringIO( localfile.read() ) #in-memory

def getPubsPerOrganism( path, taxons ):
  headers = ('tax_id', 'GeneID', 'PubMed_ID')
  dataStream = getDataStream( path, )
  counts = pubsByOrganism( dataStream, taxons, headers )
  return counts

def sortPubsPerOrganism( counts, taxons ):
  output = {}
  for tax_id in taxons:
    orgPubs = counts[tax_id]
    orgPubsAsList = list( { 'geneID': geneID, 'PubMed_IDs': pubs } for geneID, pubs in orgPubs.items() )
    sortedByCount = sorted( orgPubsAsList, key = lambda x: len( x['PubMed_IDs'] ), reverse=True )
    output[ tax_id ] = sortedByCount
  return output

# def getTop