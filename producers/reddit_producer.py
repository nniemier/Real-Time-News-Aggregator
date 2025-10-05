import time
import requests
import logging
from .kafka_producer import NewsProducer
from .config import REDDIT_SUBREDDIT_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedditProducer(NewsProducer):
    """Producer for Reddit posts"""
    
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'News-Aggregator-Bot/1.0'
        })
    
    def fetch_subreddit_posts(self, subreddit, limit=25):
        """Fetch hot posts from a subreddit"""
        try:
            url = REDDIT_SUBREDDIT_URL.format(subreddit, limit)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            logger.info(f"Fetched {len(posts)} posts from r/{subreddit}")
            return posts
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching r/{subreddit}: {e}")
            return []
    
    def produce_subreddit(self, subreddit, limit=25):
        """Fetch and produce posts from a subreddit to Kafka"""
        posts = self.fetch_subreddit_posts(subreddit, limit)
        
        produced_count = 0
        for post_data in posts:
            post = post_data.get('data', {})
            
            # Skip stickied posts
            if post.get('stickied', False):
                continue
            
            # Determine the URL (some posts are self-posts)
            url = post.get('url', '')
            if post.get('is_self', False):
                url = f"https://reddit.com{post.get('permalink', '')}"
            
            # Create message
            message = self.create_message(
                source=f"Reddit - r/{subreddit}",
                title=post.get('title', 'No title'),
                url=url,
                score=post.get('score', 0),
                author=post.get('author', 'unknown'),
                comments=post.get('num_comments', 0),
                subreddit=subreddit,
                post_id=post.get('id', ''),
                is_self_post=post.get('is_self', False)
            )
            
            # Send to Kafka
            self.send_message(message)
            produced_count += 1
        
        logger.info(f"Produced {produced_count} posts from r/{subreddit}")
        return produced_count


def main():
    """Main function to run the Reddit producer"""
    producer = RedditProducer()
    
    # List of subreddits to monitor
    subreddits = [
        'technology',
        'programming',
        'worldnews',
        'news',
        'science'
    ]
    
    try:
        logger.info("Starting Reddit producer...")
        
        total_produced = 0
        for subreddit in subreddits:
            count = producer.produce_subreddit(subreddit, limit=10)
            total_produced += count
            
            # Be respectful to Reddit's API
            time.sleep(2)
        
        logger.info(f"Total posts produced: {total_produced}")
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    except Exception as e:
        logger.error(f"Error in main: {e}")
    finally:
        producer.close()


if __name__ == "__main__":
    main()