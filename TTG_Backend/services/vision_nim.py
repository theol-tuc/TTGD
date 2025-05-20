import requests

NIM_API_KEY = "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"  # کلید واقعی‌ات رو بذار اینجا

ASSET_URL = "https://api.nvcf.nvidia.com/v2/nvcf/assets"
INFER_URL = "https://ai.api.nvidia.com/v1/vlm/nvidia/vila"

def upload_asset(file: bytes, filename: str, content_type: str):
    headers = {
        "Authorization": f"Bearer {NIM_API_KEY}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    response = requests.post(
        ASSET_URL,
        headers=headers,
        json={"contentType": content_type, "description": "Uploaded via FastAPI"},
        timeout=300, # 5 minutes timeout for asset creation
    )
    response.raise_for_status()
    upload_url = response.json()["uploadUrl"]
    asset_id = response.json()["assetId"]

    upload_headers = {
        "x-amz-meta-nvcf-asset-description": "Uploaded via FastAPI",
        "content-type": content_type
    }

    upload_response = requests.put(
        upload_url,
        data=file,
        headers=upload_headers,
        timeout=60,
    )
    upload_response.raise_for_status()

    return asset_id

def delete_asset(asset_id: str):
    headers = {"Authorization": f"Bearer {NIM_API_KEY}"}
    requests.delete(f"{ASSET_URL}/{asset_id}", headers=headers)

def send_to_vila(image_bytes: bytes, filename: str):
    ext = filename.split('.')[-1].lower()
    content_type = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
    asset_id = upload_asset(image_bytes, filename, content_type)

    media_tag = f'<img src="data:{content_type};asset_id,{asset_id}" />'
    messages = [{
        "role": "user",
        "content": (
            "This image is from the game Turing Tumble. In this game, marbles fall from the top and interact with mechanical components to compute logic. "
            "The objective is to solve a logic challenge by placing ramps, crossovers, gears, and bits. "
            f"Please analyze this image and explain what kind of logic mechanism is shown. Then give me hints or steps I can follow to solve this challenge. {media_tag}"
        )
    }]

    headers = {
        "Authorization": f"Bearer {NIM_API_KEY}",
        "Content-Type": "application/json",
        "NVCF-INPUT-ASSET-REFERENCES": asset_id,
        "NVCF-FUNCTION-ASSET-IDS": asset_id,
        "Accept": "application/json"
    }

    payload = {
        "model": "nvidia/vila",
        "messages": messages,
        "temperature": 0.2,
        "top_p": 0.7,
        "max_tokens": 1024,
        "seed": 50
    }

    response = requests.post(INFER_URL, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()

    delete_asset(asset_id)
    print("VILA API response:", result)

    return result