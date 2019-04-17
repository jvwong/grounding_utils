from popularity.util import fetchFTPZip

NCBI_GENE_DIRECTORY = '/gene/DATA/'
GENE2PUBMED_FILE = 'gene2pubmed.gz' 
OUTFILE =  'gene2pubmed.txt'
  
def getRanks():
  fetchFTPZip( NCBI_GENE_DIRECTORY, GENE2PUBMED_FILE, OUTFILE )