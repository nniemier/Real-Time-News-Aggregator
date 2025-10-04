import json
import logging
from datetime import datetime
from confluent_kafka import Producer
from ..config import PRODUCER_CONFIG, KAFKA_TOPIC

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsProducer:
    """Base class for producing news messages to Kafka"""
    
    def __init__(self, topic=KAFKA_TOPIC):
        self.topic = topic
        self.producer = Producer(PRODUCER_CONFIG)
        logger.info(f"Kafka producer initialized for topic: {self.topic}")
    
    def delivery_callback(self, err, msg):
        """Callback function called when a message is delivered or fails"""
        if err:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(
                f"Message delivered to {msg.topic()} "
                f"[partition {msg.partition()}] at offset {msg.offset()}"
            )
    
    def create_message(self, source, title, url, **kwargs):
        """Create a standardized news message"""
        message = {
            "source": source,
            "title": title,
            "url": url,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            **kwargs  # Allow additional fields
        }
        return message
    
    def send_message(self, message):
        """Send a message to Kafka"""
        try:
            # Convert message to JSON
            message_json = json.dumps(message)
            
            # Produce to Kafka
            self.producer.produce(
                topic=self.topic,
                value=message_json.encode('utf-8'),
                key=message['url'].encode('utf-8'),  # Use URL as key for deduplication
                callback=self.delivery_callback
            )
            
            # Trigger callbacks (non-blocking)
            self.producer.poll(0)
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    def flush(self):
        """Wait for all messages to be delivered"""
        remaining = self.producer.flush(timeout=10)
        if remaining > 0:
            logger.warning(f"{remaining} messages were not delivered")
        else:
            logger.info("All messages delivered successfully")
    
    def close(self):
        """Close the producer"""
        self.flush()
        logger.info("Producer closed")