from collectors.news_api import NewsAPICollector


if __name__ == '__main__':
  NewsAPI_collector = NewsAPICollector()
  NewsAPI_articles = NewsAPI_collector.collect(days=1)

  print(f"Found {len(NewsAPI_articles)} aerospace and defense news articles from NewsAPI")

  # Print headline and source of first 5 articles
  for i, article in enumerate(NewsAPI_articles[:5]):
    NewsAPI_collector.normalize_article(article)
    print(f"{i+1}. {article['title']} ({article['source']})")

  NewsAPI_collector.save_articles(NewsAPI_articles)
  