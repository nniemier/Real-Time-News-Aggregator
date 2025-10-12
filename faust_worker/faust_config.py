import os
from dotenv import load_dotenv

load_dotenv()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9093')

# Topics
INPUT_TOPIC = 'news-articles'
OUTPUT_TOPIC = 'processed-news'

# Faust app configuration
FAUST_APP_ID = 'news-processor'
FAUST_BROKER = f'kafka://{KAFKA_BOOTSTRAP_SERVERS}'

# Category keywords (case-insensitive matching)
CATEGORIES = {
    'AI': [
        'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
        'neural network', 'llm', 'chatgpt', 'gpt', 'openai', 'anthropic', 'claude',
        'gemini', 'copilot', 'midjourney', 'stable diffusion', 'transformer',
        'generative ai', 'nlp', 'computer vision'
    ],
    'Programming': [
        'python', 'javascript', 'java', 'typescript', 'rust', 'go', 'golang',
        'programming', 'coding', 'developer', 'software development', 'code',
        'github', 'git', 'api', 'framework', 'library', 'backend', 'frontend',
        'react', 'vue', 'angular', 'node.js', 'django', 'flask'
    ],
    'Cybersecurity': [
        'security', 'cybersecurity', 'breach', 'vulnerability', 'hack', 'hacker',
        'exploit', 'malware', 'ransomware', 'phishing', 'encryption', 'zero-day',
        'penetration testing', 'firewall', 'authentication', 'data breach',
        'cyber attack', 'infosec'
    ],
    'Tech': [
        'technology', 'tech', 'startup', 'silicon valley', 'venture capital',
        'innovation', 'software', 'hardware', 'semiconductor', 'chip',
        'apple', 'google', 'microsoft', 'amazon', 'meta', 'tesla',
        'smartphone', 'laptop', 'gadget', 'cloud computing', 'saas'
    ],
    'Web3': [
        'blockchain', 'cryptocurrency', 'bitcoin', 'ethereum', 'crypto',
        'web3', 'nft', 'defi', 'smart contract', 'dao', 'metaverse',
        'solana', 'polygon', 'binance'
    ],
    'Data Science': [
        'data science', 'data analysis', 'analytics', 'big data', 'data engineering',
        'data visualization', 'statistics', 'pandas', 'numpy', 'jupyter',
        'tableau', 'sql', 'database', 'etl', 'data pipeline'
    ],
    'DevOps': [
        'devops', 'docker', 'kubernetes', 'k8s', 'ci/cd', 'jenkins', 'gitlab',
        'aws', 'azure', 'gcp', 'cloud', 'infrastructure', 'terraform',
        'ansible', 'monitoring', 'deployment'
    ],
    'Sports': [
        'sports', 'football', 'basketball', 'soccer', 'baseball', 'tennis',
        'nba', 'nfl', 'fifa', 'olympics', 'world cup', 'champions league',
        'premier league', 'athletics', 'boxing', 'mma', 'ufc'
    ],
    'Science': [
        'science', 'research', 'study', 'physics', 'chemistry', 'biology',
        'space', 'astronomy', 'nasa', 'spacex', 'rocket', 'climate',
        'environment', 'medical', 'health', 'medicine', 'vaccine'
    ]
}

# Minimum score threshold for filtering (optional)
MIN_SCORE = os.getenv('MIN_SCORE', 0)  # 0 = no filtering