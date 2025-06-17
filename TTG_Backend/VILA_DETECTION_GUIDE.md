# VILA Response Detection Guide

## 🎯 Purpose
This guide helps you determine whether the responses you receive from VILA are real or dummy.

## 🔍 How to Detect

### 1. Response Structure Analysis

#### Real VILA Response:
```json
{
  "status": "success",
  "executed_components": ["add_component(...)", "add_component(...)"],
  "raw_response": {
    "id": "chatcmpl-...",
    "object": "chat.completion",
    "created": 1234567890,
    "model": "nvidia/vila",
    "choices": [
      {
        "message": {
          "content": "add_component(0.12, 0.12, 0.36, 0.36, 'A', 'green')..."
        }
      }
    ],
    "usage": {...}
  },
  "recommended_move": "add_component(...)",
  "confidence": 0
}
```

#### Dummy Response:
```json
{
  "status": "success",
  "executed_components": ["add_component(ramp_left, 1, 2)", "add_component(bit_right, 3, 4)"],
  "raw_response": {
    "choices": [
      {
        "message": {
          "content": "add_component(ramp_left, 1, 2)\nadd_component(bit_right, 3, 4)"
        }
      }
    ],
    "dummy_analysis": "VILA API key not configured. Please set VILA_API_KEY environment variable."
  },
  "recommended_move": "add_component(ramp_left, 1, 2)",
  "confidence": 0
}
```

### 2. Real Response Indicators:
- ✅ `raw_response` field includes `id`, `object`, `created`, `model`
- ✅ `model` equals `"nvidia/vila"`
- ✅ `choices[0].message.content` includes complex and diverse commands
- ✅ No `dummy_analysis` field
- ✅ No `error` field

### 3. Dummy Response Indicators:
- ❌ `dummy_analysis` field exists
- ❌ `error` field exists
- ❌ Fixed content: `"add_component(ramp_left, 1, 2)"` and `"add_component(bit_right, 3, 4)"`
- ❌ Missing `id`, `object`, `created`, `model` fields in `raw_response`

## 🧪 Detection Tests

### Test 1: Check with API Key
```bash
python test_vila_detection.py
```

### Test 2: Check without API Key
```bash
python test_vila_no_key.py
```

### Test 3: Simple Test
```bash
python test_vila_simple.py
```

## 🔧 Configuration

### To get real responses:
1. Create `.env` file in `TTG_Backend` folder
2. Add your API key:
   ```
   VILA_API_KEY=your_nvidia_api_key_here
   VILA_API_URL=https://ai.api.nvidia.com/v1/vlm/nvidia/vila
   ```

### To test dummy:
- Remove API key or ignore `.env` file

## 📊 Practical Examples

### Real Response:
```
🤖 VILA Analysis: add_component(0.12, 0.12, 0.36, 0.36, 'A', 'green')
add_component(0.12, 0.36, 0.36, 0.6, 'A', 'green')
add_component(0.12, 0.6, 0.36, 0.84, 'A', 'green')...
```

### Dummy Response:
```
🤖 VILA Analysis: add_component(ramp_left, 1, 2)
add_component(bit_right, 3, 4)
```

## 🎯 Conclusion

- **Real Response**: Includes precise coordinates, colors, and diverse commands
- **Dummy Response**: Includes fixed and simple commands with specific coordinates

## 💡 Important Notes

1. **API Key**: Without a valid API key, you will always receive dummy responses
2. **Internet Connection**: Internet connection is required to receive real responses
3. **Server**: Make sure the FastAPI server is running (`python run.py`)
4. **Image**: The image must be valid and processable

## 🚀 Running Tests

```bash
# Start server
python run.py

# In another terminal
python test_vila_detection.py
``` 