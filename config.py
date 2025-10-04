import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'news-articles')

# Producer configuration
PRODUCER_CONFIG = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'client.id': 'news-producer',
    'acks': 'all',  # Wait for all replicas to acknowledge
    'retries': 3,
    'compression.type': 'gzip'
}

# API endpoints
HACKER_NEWS_TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
HACKER_NEWS_ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

# Reddit (no auth required for public feeds)
REDDIT_SUBREDDIT_URL = 'https://www.reddit.com/r/{}/hot.json?limit={}'

# RSS Feeds (examples)
RSS_FEEDS = [
    'https://hnrss.org/newest',  # Hacker News RSS
    'https://news.ycombinator.com/rss',
    'https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml'
]