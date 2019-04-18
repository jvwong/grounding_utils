import os
from popularity.util import fetchFTPZip, countsByOrganism

NCBI_GENE_DIRECTORY = '/gene/DATA/'
GENE2PUBMED_FILE = 'gene2pubmed.gz' 
COUNTS_FILE =  'gene2pubmed.txt'
    
def getRanks():
  # fetchFTPZip( NCBI_GENE_DIRECTORY, GENE2PUBMED_FILE, COUNTS_FILE )
  taxons = [ '9606' ]
  countsByOrganism( COUNTS_FILE, taxons )
  