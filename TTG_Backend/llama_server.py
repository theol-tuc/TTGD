from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama
import os

app = FastAPI()

# Initialize the LLaMA model
model_path = "/scratch/mtko19/models/llama3/llama-pro-8b-instruct.Q4_K_M.gguf"
print(f"🤖 Loading model from: {model_path}")
llm = Llama(model_path=model_path, n_ctx=2048)

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.3

@app.post("/generate")
async def generate(req: GenerateRequest):
    try:
        print(f"\n⏳ Prompt received:\n{req.prompt}\n")
        
        output = llm(
            req.prompt,
            max_tokens=req.max_tokens,
            temperature=req.temperature,
            stop=["</s>"],
            echo=False
        )
        
        print(f"\n🧠 Raw output:\n{output}")
        
        if not output or not output.get("choices"):
            raise HTTPException(status_code=500, detail="No output generated")
            
        response_text = output["choices"][0]["text"]
        print(f"\n✨ Final response:\n{response_text}")
        
        return {"output": response_text}
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting LLaMA server on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)