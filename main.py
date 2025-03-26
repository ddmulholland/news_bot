from collectors.news_api import NewsAPICollector


if __name__ == '__main__':
  collector = NewsAPICollector()
  articles = collector.get_aero_news(days=1)

  print(f"Found {len(articles)} aerospace and defense news articles")

  # Print headline and source of first 5 articles
  for i, article in enumerate(articles[:5]):
    print(f"{i+1}. {article['title']} ({article['source']['name']})")

  collector.save_articles(articles)
  