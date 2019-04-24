import os
from popularity.index import getRanks, getTopGenes
from articles.index import scrapeArticleEntities

def main():
  scrapeArticleEntities()
  
main()

