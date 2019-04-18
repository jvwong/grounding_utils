import ftplib
import zlib
import csv

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


def countByOrganism( csvReader ):
  output = {}
  for row in csvReader:
      print('taxon: {taxon} - gene ID: {gene}'.format( taxon=row['tax_id'], gene=row['GeneID'] ) )
  return output

def loadCountData( path ):
  fields = ('tax_id', 'GeneID', 'PubMed_ID')
  counts = {}
  with open( path, 'r' ) as tsvfile:
    reader = csv.DictReader( tsvfile, delimiter='\t', fieldnames=fields )
    for row in reader:
      print('taxon: {taxon} - gene ID: {gene}'.format( taxon=row['tax_id'], gene=row['GeneID'] ) )
  return counts
  
def countsByOrganism( path, taxons ):
  csvReader = loadCountData( path )
  counts = countByOrganism( csvReader )
  
