# Get news from NewsAPI
import os
import requests
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
from .base import BaseCollector, Article
from typing import List, Dict, Any, Optional

# load env vars from .env file 
load_dotenv()

class NewsAPICollector(BaseCollector):
  """
  Collector for retreiving news from NewsAPI.
  """
  def __init__(self, api_key=None):
    """
    Initialize NewsAPICollector.

    Args:
      api_key (str, optional): NewsAPI key, if None, tries to get from env vars
    """
    self.api_key = api_key or os.environ["NEWS_API_KEY"]
    if not self.api_key:
      raise ValueError("NewsAPI key not found")

    self.base_url = "https://newsapi.org/v2/everything"
    self.collector_name = 'NewsAPI'

  def collect(self, days=1, **kwargs):
    """
    Fetch Aerospace and Defense news from last specified days.

    Args:
      days (int): number of days to look back for news

    Returns:
      list: List of news articles.
    """

    # Calculate day range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Format dates for api
    from_date = start_date.strftime('%Y-%m-%d')
    to_date = end_date.strftime('%Y-%m-%d')

    # Define search params
    params = {
      'apiKey': self.api_key,
      'language': 'en',
      'from': from_date,
      'to': to_date,
      'sortBy': 'relevancy',
      'pageSize': 100 # Max for free tier
    }
    
    # Aero search terms
    aero_keywords = "aerospace OR aircraft OR aviation OR space OR NASA OR SpaceX OR Boeing OR Airbus"

    # Defense search terms
    defense_keywords = "defense OR defence OR mililtary OR missile OR drone OR fighter jet OR warfare"

    # combined search query
    params['q'] = f"({aero_keywords}) AND ({defense_keywords})"

    # API request  
    response = requests.get(f"{self.base_url}", params=params)

    if response.status_code != 200:
      print(f"Error fetching news: {response.status_code}")
      print(response.text)
      return []

    # Parsing response
    data = response.json()
    articles = data.get('articles', [])

    return articles

  def search(self, **kwargs) -> List[Article]:
    pass

  def normalize_article(self, raw_article: Dict[str, Any]) -> Article:
    article = Article(
      id=self.generate_unique_id(raw_article),
      source= raw_article['source']['name'],
      title= raw_article['title'],
      description= raw_article['description'],
      url= raw_article['url'],
      author= raw_article['author'],
      content= raw_article['content'],
      image_url= raw_article['urlToImage'],
      category= None,
      collector_type = 'NewsAPICollector',
    )
    return article
  

  # def save_articles(self, articles, filename=None):
  #   """
  #   Save articles to a JSON file.

  #   Args:
  #     articles (list): List of article dictionaries
  #     filename (str, optional): Output filename. Defaults to 'aerospace_defense_news_{date}.json'
  #   """
  #   if not filename:
  #     date_str = datetime.now().strftime('%Y%m%d')
  #     filename = f"aerospace_defense_news_{date_str}.json"

  #   with open(filename, 'w', encoding='utf-8') as f:
  #     json.dump(articles, f, indent=2, ensure_ascii=False)

  #   print(f"Saved {len(articles)} articles to {filename}")
    