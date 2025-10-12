import faust
import logging
from datetime import datetime
from typing import List, Tuple, Dict
from models import NewsArticle, ProcessedArticle
from faust_config import (
    FAUST_APP_ID,
    FAUST_BROKER,
    INPUT_TOPIC,
    OUTPUT_TOPIC,
    CATEGORIES,
    MIN_SCORE
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Faust app
app = faust.App(
    FAUST_APP_ID,
    broker=FAUST_BROKER,
    value_serializer='json',
)

# Define topics
input_topic = app.topic(INPUT_TOPIC, value_type=NewsArticle)
output_topic = app.topic(OUTPUT_TOPIC, value_type=ProcessedArticle)


def categorize_article(article: NewsArticle) -> Tuple[List[str], List[str], float]:
    """
    Categorize an article based on keywords in title and summary.
    
    Returns:
        (categories, matched_keywords, relevance_score)
    """
    # Combine title and summary for matching
    text = article.title.lower()
    if article.summary:
        text += " " + article.summary.lower()
    
    matched_categories = []
    matched_keywords = []
    keyword_matches = 0
    
    # Check each category
    for category, keywords in CATEGORIES.items():
        category_matched = False
        
        for keyword in keywords:
            if keyword.lower() in text:
                if not category_matched:
                    matched_categories.append(category)
                    category_matched = True
                
                if keyword not in matched_keywords:
                    matched_keywords.append(keyword)
                    keyword_matches += 1
    
    # Calculate relevance score (number of unique keywords matched)
    relevance_score = keyword_matches
    
    return matched_categories, matched_keywords, relevance_score


def should_process_article(article: NewsArticle) -> bool:
    """
    Determine if article should be processed based on filters.
    """
    # Filter by score if present
    if article.score is not None and article.score < MIN_SCORE:
        return False
    
    return True


@app.agent(input_topic)
async def process_news(articles):
    """
    Main processing agent that consumes from news-articles
    and produces to processed-news.
    """
    async for article in articles:
        try:
            logger.info(f"Processing: {article.title[:50]}...")
            
            # Apply filters
            if not should_process_article(article):
                logger.info(f"Skipped (low score): {article.title[:50]}")
                continue
            
            # Categorize
            categories, keywords, relevance = categorize_article(article)
            
            # Only process if at least one category matched
            if not categories:
                logger.info(f"No categories matched: {article.title[:50]}")
                continue
            
            # Create processed article
            processed = ProcessedArticle(
                # Original fields
                source=article.source,
                title=article.title,
                url=article.url,
                timestamp=article.timestamp,
                score=article.score,
                author=article.author,
                comments=article.comments,
                story_id=article.story_id,
                subreddit=article.subreddit,
                post_id=article.post_id,
                is_self_post=article.is_self_post,
                published=article.published,
                summary=article.summary,
                # Processing metadata
                categories=categories,
                matched_keywords=keywords,
                processed_at=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                relevance_score=relevance
            )
            
            # Send to output topic
            await output_topic.send(value=processed)
            
            logger.info(
                f"✓ Processed: {article.title[:50]} | "
                f"Categories: {', '.join(categories)} | "
                f"Relevance: {relevance}"
            )
            
        except Exception as e:
            logger.error(f"Error processing article: {e}", exc_info=True)


@app.timer(interval=60.0)
async def print_stats():
    """Print processing stats every minute"""
    logger.info("=" * 50)
    logger.info("Faust worker is running and processing news articles...")
    logger.info(f"Input topic: {INPUT_TOPIC}")
    logger.info(f"Output topic: {OUTPUT_TOPIC}")
    logger.info(f"Categories: {len(CATEGORIES)}")
    logger.info("=" * 50)


@app.command()
async def show_categories():
    """Show configured categories and keywords"""
    print("\n=== Configured Categories ===\n")
    for category, keywords in CATEGORIES.items():
        print(f"{category}:")
        print(f"  Keywords: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
        print(f"  Total: {len(keywords)} keywords\n")


if __name__ == '__main__':
    app.main()