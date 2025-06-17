import asyncio
import requests
from api import app
from hypercorn.config import Config
from hypercorn.asyncio import serve

def check_llm_server():
    try:
        response = requests.post(
            "http://localhost:8001/generate",
            json={"prompt": "Hello", "max_tokens": 5}
        )
        if response.status_code == 200:
            print("✅ LLaMA server is reachable.")
        else:
            print("⚠️ LLaMA server returned unexpected status:", response.status_code)
    except Exception as e:
        print("❌ Could not connect to LLaMA server:", e)
        print("\nMake sure you have an active SSH tunnel with:")
        print("ssh -L 8001:localhost:8001 mtko19@cloud-247.rz.tu-clausthal.de")

config = Config()
config.bind = ["127.0.0.1:8000"]

async def main():
    await serve(app, config)

if __name__ == "__main__":
    check_llm_server()
    asyncio.run(main()) 