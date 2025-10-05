# Real-Time-News-Aggregator

## Access points:
- Kafka: localhost:9092
- MongoDB: localhost:27017
- Mongo Express UI: http://localhost:8081

## Commands for docker-compose

### Start all services
docker-compose up -d

### View logs
docker-compose logs -f

### Stop all services
docker-compose down

### Stop and remove volumes (deletes data)
docker-compose down -v

## Virtual enviornment

### Activate the virtual environment
.\venv\Scripts\activate

### Deactivate venv
deactivate