# Shared collector functionality
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional
from dataclasses import dataclass
import datetime
import hashlib

@dataclass
class Article:
  """Basic article format all data will be converted to"""
  id: str
  source: str
  title: str
  description: str
  url: str
  author: Optional[str] = None
  content: Optional[str] = None
  image_url: Optional[str] = None
  category: Optional[str] = None
  collector_type: Optional[str] = None  # Identifies which collector provided this article

class BaseCollector(ABC):
  """Abstract base class all collectors must implement"""

  @abstractmethod
  def collect(self, **kwargs) -> List[Article]:
    """
    Collects articles from the source.

    Args: 
      **kwargs: Optional parameters, specific to each collector type
        (e.g. keywords, categories, dates)
    Returns: 
      List of normalized Article objects
    """
    pass


  @abstractmethod
  def search(self, query: str, **kwargs) -> List[Article]:
    """
    Search for articles matching a specific query

    Args:
      query: Search term
      **kwargs: Additional params

    Returns: 
      List of matching articles
    """
    pass


  def normalize_article(self, raw_article: Dict[str, Any]) -> Article:
    """
    Convert source specific article to the standard article model. Can be implemented or extended

    Args:
      raw_article: Raw article from specific source

    Returns:
      Article object
    """
    
    raise NotImplementedError("Did not implement normalize_article")

  def generate_unique_id(self, article_data: Dict[str, Any]) -> str:
    """
    Generate a unique ID for each article to help with deduplication.

    Args:
      article_data: Raw or processed article data

    Returns:
      str: unique article id
    """

    url = article_data.get('url', '')
    title = article_data.get('title', '')
    unique_string = f"{url}:{title}"
    return hashlib.md5(unique_string.encode()).hexdigest()