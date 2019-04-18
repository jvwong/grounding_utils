from popularity.index import getRanks, getTopGenes

# --------- Article processing ----------------------
# from articles.index import scrapeArticleEntities
# FULL_TEXT_DIR = 'full_text'
# OUTPUT_FILE_NAME = 'entities.json'
# OUTPUT_PATH = os.path.join( FULL_TEXT_DIR, OUTPUT_FILE_NAME )


# --------- Popularity ranking ----------------------
def main():
  taxon_ids=['9606']
  getTopGenes( 10 )

main()

