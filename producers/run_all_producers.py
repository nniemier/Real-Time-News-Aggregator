import time
import logging
from .hacker_news_producer import HackerNewsProducer
from .reddit_producer import RedditProducer
from .rss_producer import RSSProducer
from .config import RSS_FEEDS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_all_producers():
    """Run all news producers sequentially"""
    
    total_messages = 0
    
    # 1. Hacker News
    logger.info("=" * 50)
    logger.info("Running Hacker News Producer")
    logger.info("=" * 50)
    hn_producer = HackerNewsProducer()
    try:
        count = hn_producer.produce_stories(limit=15)
        total_messages += count
    finally:
        hn_producer.close()
    
    time.sleep(2)
    
    # 2. Reddit
    logger.info("=" * 50)
    logger.info("Running Reddit Producer")
    logger.info("=" * 50)
    reddit_producer = RedditProducer()
    try:
        subreddits = ['technology', 'programming', 'worldnews']
        for subreddit in subreddits:
            count = reddit_producer.produce_subreddit(subreddit, limit=10)
            total_messages += count
            time.sleep(2)
    finally:
        reddit_producer.close()
    
    time.sleep(2)
    
    # 3. RSS Feeds
    logger.info("=" * 50)
    logger.info("Running RSS Producer")
    logger.info("=" * 50)
    rss_producer = RSSProducer()
    try:
        count = rss_producer.produce_all_feeds(RSS_FEEDS)
        total_messages += count
    finally:
        rss_producer.close()
    
    logger.info("=" * 50)
    logger.info(f"All producers completed! Total messages: {total_messages}")
    logger.info("=" * 50)


def run_continuous(interval_minutes=15):
    """Run all producers continuously at specified intervals"""
    logger.info(f"Starting continuous mode (interval: {interval_minutes} minutes)")
    
    try:
        while True:
            run_all_producers()
            logger.info(f"Sleeping for {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        logger.info("Continuous mode stopped by user")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        # Run continuously
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        run_continuous(interval_minutes=interval)
    else:
        # Run once
        run_all_producers()