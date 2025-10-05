import time
import requests
import logging
from .kafka_producer import NewsProducer
from .config import HACKER_NEWS_TOP_STORIES_URL, HACKER_NEWS_ITEM_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HackerNewsProducer(NewsProducer):
    """Producer for Hacker News articles"""
    
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'News-Aggregator-Bot/1.0'})
    
    def fetch_story(self, story_id):
        """Fetch a single story by ID"""
        try:
            url = HACKER_NEWS_ITEM_URL.format(story_id)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching story {story_id}: {e}")
            return None
    
    def fetch_top_stories(self, limit=10):
        """Fetch top stories from Hacker News"""
        try:
            response = self.session.get(HACKER_NEWS_TOP_STORIES_URL, timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:limit]
            
            logger.info(f"Fetched {len(story_ids)} top story IDs")
            return story_ids
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching top stories: {e}")
            return []
    
    def produce_stories(self, limit=10):
        """Fetch and produce top stories to Kafka"""
        story_ids = self.fetch_top_stories(limit)
        
        produced_count = 0
        for story_id in story_ids:
            story = self.fetch_story(story_id)
            
            if story and story.get('type') == 'story':
                # Create message
                message = self.create_message(
                    source="Hacker News",
                    title=story.get('title', 'No title'),
                    url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    score=story.get('score', 0),
                    author=story.get('by', 'unknown'),
                    comments=story.get('descendants', 0),
                    story_id=story_id
                )
                
                # Send to Kafka
                self.send_message(message)
                produced_count += 1
                
                # Be nice to the API
                time.sleep(0.1)
        
        logger.info(f"Produced {produced_count} Hacker News stories")
        return produced_count


def main():
    """Main function to run the Hacker News producer"""
    producer = HackerNewsProducer()
    
    try:
        logger.info("Starting Hacker News producer...")
        
        # Fetch and produce top 20 stories
        producer.produce_stories(limit=20)
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        producer.close()


if __name__ == "__main__":
    main()