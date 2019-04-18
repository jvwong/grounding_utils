import os
from popularity.util import fetchFTPZip, getPubsPerOrganism, sortPubsPerOrganism
from utils import writeToJSONFile

NCBI_GENE_DIRECTORY = '/gene/DATA/'
GENE2PUBMED_FILE = 'gene2pubmed.gz'
COUNTS_FILE =  'gene2pubmed.txt'
TAXONS = set(['9606'])
TAXON2GENE2PUB_FILE = 'pubsPerOrganism.json'
SORT_FILE = 'sortedPubsPerOrganism.json'

def getRanks( refresh=False ):
  if refresh:
    fetchFTPZip( NCBI_GENE_DIRECTORY, GENE2PUBMED_FILE, COUNTS_FILE )
  counts = getPubsPerOrganism( COUNTS_FILE, TAXONS )
  sortedPubsPerOrg = sortPubsPerOrganism( counts, TAXONS )
  top = sortedPubsPerOrg['9606'][:10]
  topIds = [ entry['geneID'] for entry in top ]
  print( topIds )
  # writeToJSONFile( sort, SORT_FILE )




