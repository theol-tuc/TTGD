import asyncio
import logging
from datetime import datetime
from api import app
from hypercorn.config import Config
from hypercorn.asyncio import serve

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'vila_analysis_{datetime.now().strftime("%Y%m%d")}.log')
    ]
)

config = Config()
config.bind = ["127.0.0.1:8000"]
config.cors_origins = ["http://localhost:3000"]
config.accesslog = logging.getLogger('hypercorn.access')

async def main():
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())