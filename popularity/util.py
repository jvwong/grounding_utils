import ftplib
import zlib

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
  
