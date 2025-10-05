import time
import feedparser
import logging
from kafka_producer import NewsProducer
from .config import RSS_FEEDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RSSProducer(NewsProducer):
    """Producer for RSS feeds"""
    
    def __init__(self):
        super().__init__()
    
    def fetch_feed(self, feed_url):
        """Fetch and parse an RSS feed"""
        try:
            logger.info(f"Fetching feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                logger.warning(f"Feed parsing warning for {feed_url}: {feed.bozo_exception}")
            
            entries = feed.entries
            feed_title = feed.feed.get('title', 'Unknown Feed')
            
            logger.info(f"Fetched {len(entries)} entries from '{feed_title}'")
            return entries, feed_title
        except Exception as e:
            logger.error(f"Error fetching feed {feed_url}: {e}")
            return [], "Unknown Feed"
    
    def produce_feed(self, feed_url):
        """Fetch and produce articles from an RSS feed to Kafka"""
        entries, feed_title = self.fetch_feed(feed_url)
        
        produced_count = 0
        for entry in entries:
            # Extract relevant fields
            title = entry.get('title', 'No title')
            url = entry.get('link', '')
            published = entry.get('published', '')
            author = entry.get('author', 'unknown')
            summary = entry.get('summary', '')
            
            # Skip if no URL
            if not url:
                continue
            
            # Create message
            message = self.create_message(
                source=f"RSS - {feed_title}",
                title=title,
                url=url,
                author=author,
                published=published,
                summary=summary[:200] if summary else ''  # Truncate summary
            )
            
            # Send to Kafka
            self.send_message(message)
            produced_count += 1
        
        logger.info(f"Produced {produced_count} articles from '{feed_title}'")
        return produced_count
    
    def produce_all_feeds(self, feed_urls):
        """Produce articles from multiple RSS feeds"""
        total_produced = 0
        
        for feed_url in feed_urls:
            count = self.produce_feed(feed_url)
            total_produced += count
            
            # Small delay between feeds
            time.sleep(1)
        
        return total_produced


def main():
    """Main function to run the RSS producer"""
    producer = RSSProducer()
    
    # You can add more RSS feeds here
    feeds = RSS_FEEDS + [
        'https://feeds.bbci.co.uk/news/technology/rss.xml',  # BBC Tech
        'https://www.theverge.com/rss/index.xml',  # The Verge
    ]
    
    try:
        logger.info("Starting RSS feed producer...")
        
        total = producer.produce_all_feeds(feeds)
        logger.info(f"Total articles produced: {total}")
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        producer.close()


if __name__ == "__main__":
    main()