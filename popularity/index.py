import os
import json
from popularity.util import fetchFTPZip, getPubsPerOrganism, sortPubsPerOrganism, getTopGeneIDs
from utils import writeToJSONFile

NCBI_GENE_DIRECTORY = '/gene/DATA/'
GENE2PUBMED_FILE = 'gene2pubmed.gz'
COUNTS_FILE =  'gene2pubmed.txt'
TAXONS = set(['9606'])
TAXON2GENE2PUB_FILE = 'pubsPerOrganism.json'
SORT_FILE = 'sortedPubsPerOrganism.json'

def getRanks( refresh=False, n=10 ):
  if refresh:
    fetchFTPZip( NCBI_GENE_DIRECTORY, GENE2PUBMED_FILE, COUNTS_FILE )
    counts = getPubsPerOrganism( COUNTS_FILE, TAXONS )
    sortedPubsPerOrg = sortPubsPerOrganism( counts, TAXONS )
    writeToJSONFile( sortedPubsPerOrg, SORT_FILE )

  with open( SORT_FILE, 'r' ) as json_file:
    sortedPubsPerOrg = json.loads( json_file.read() )
    top = getTopGeneIDs( sortedPubsPerOrg, n )
    print( top )






