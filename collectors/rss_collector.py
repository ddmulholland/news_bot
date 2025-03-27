# Collect from RSS feeds

import feedparser
import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .base import BaseCollector

@dataclass
class RSSArticle:
  title: str
  description: str
  url: str
  published_at: datetime.datetime
  source_name: str
  author: Optional[str] = None
  content: Optional[str] = None
  image_url: Optional[str] = None

class RSSCollector(BaseCollector)