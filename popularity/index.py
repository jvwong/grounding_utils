import os
import json
import pprint
from popularity.util import fetchFTPZip, getPubsPerOrganism, sortPubsPerOrganism, getTopGeneIDs
from utils import writeToJSONFile

NCBI_GENE_DIRECTORY = '/gene/DATA/'
GENE2PUBMED_FILE = 'gene2pubmed.gz'
COUNTS_FILE =  'gene2pubmed.txt'
TAXONS = set([
  '9606',  # h. sapiens
  '10090', # m. musculus
  '4932', # s. cervisiae
  '7227', # d. melonogaster
  '83333',  # e. coli
  '6239', # c. elegans
  '3702', # a. thaliana
  '10116', # r. norvegicus
  '7955' # d. rerio
])
TAXON2GENE2PUB_FILE = 'pubsPerOrganism.json'
SORT_FILE = 'sortedPubsPerOrganism.json'

def getRanks():
  fetchFTPZip( NCBI_GENE_DIRECTORY, GENE2PUBMED_FILE, COUNTS_FILE )
  counts = getPubsPerOrganism( COUNTS_FILE, TAXONS )
  sortedPubsPerOrg = sortPubsPerOrganism( counts, TAXONS )
  writeToJSONFile( sortedPubsPerOrg, SORT_FILE )

def getTopGenes( num ):
  with open( SORT_FILE, 'r' ) as json_file:
    sortedPubsPerOrg = json.loads( json_file.read() )
    top = getTopGeneIDs( sortedPubsPerOrg, TAXONS, num )
    pprint.pprint( top )






