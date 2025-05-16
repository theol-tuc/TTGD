import asyncio
from api import app
from hypercorn.config import Config
from hypercorn.asyncio import serve

config = Config()
config.bind = ["127.0.0.1:8000"]
config.cors_origins = ["http://localhost:3000"]

async def main():
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())