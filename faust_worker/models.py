import faust
from typing import Optional, List
from datetime import datetime
from dataclasses import field 

class NewsArticle(faust.Record, serializer='json'):
    """Input news article from producers"""
    source: str
    title: str
    url: str
    timestamp: str
    
    # Optional fields that might be present
    score: Optional[int] = None
    author: Optional[str] = None
    comments: Optional[int] = None
    story_id: Optional[int] = None
    subreddit: Optional[str] = None
    post_id: Optional[str] = None
    is_self_post: Optional[bool] = None
    published: Optional[str] = None
    summary: Optional[str] = None


class ProcessedArticle(faust.Record, serializer='json'):
    """Processed article with categories"""

    # --- Required (non-default) fields first ---
    source: str
    title: str
    url: str
    timestamp: str

    categories: List[str] = field(default_factory=list)       
    matched_keywords: List[str] = field(default_factory=list) 
    processed_at: str = ""                                   
    relevance_score: float = 0.0                              

    # --- Optional / defaulted fields after ---
    score: Optional[int] = None
    author: Optional[str] = None
    comments: Optional[int] = None
    story_id: Optional[int] = None
    subreddit: Optional[str] = None
    post_id: Optional[str] = None
    is_self_post: Optional[bool] = None
    published: Optional[str] = None
    summary: Optional[str] = None