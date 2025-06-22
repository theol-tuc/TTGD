import os
import glob
import time
import openai
from graphviz import Source
from tabulate import tabulate
import json

# Config
CHALLENGE_DIR = os.path.join(os.path.dirname(__file__), 'Challenges')
API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    API_KEY = input('Enter your OpenAI API key: ').strip()
openai.api_key = API_KEY

# Find all .gv files
gv_files = glob.glob(os.path.join(CHALLENGE_DIR, '*.gv'))

results = []

def gv_to_png(gv_path):
    png_path = gv_path + '.png'
    s = Source.from_file(gv_path)
    s.format = 'png'
    s.render(filename=gv_path, cleanup=True)
    return png_path

def send_to_gpt4v(image_path):
    with open(image_path, 'rb') as img_file:
        image_bytes = img_file.read()
    start = time.time()
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a Turing Tumble puzzle solver. Analyze the puzzle image and describe the solution steps."},
            {"role": "user", "content": "Solve this puzzle.", "image": image_bytes}
        ],
        max_tokens=512
    )
    elapsed = time.time() - start
    answer = response.choices[0].message.content if hasattr(response.choices[0].message, 'content') else str(response)
    return answer, elapsed

def check_solution(response_text):
    # Placeholder: implement actual solution checking logic
    return 'success' if response_text and len(response_text) > 10 else 'fail'

def print_json_summary(puzzle, status, response_time, answer, error=None):
    summary = {
        "puzzle": puzzle,
        "status": status,
        "response_time": response_time,
        "answer": answer[:100],
    }
    if error:
        summary["error"] = error
    print(json.dumps(summary))

print("\nGPT-4V Graph Puzzle Evaluation\n" + "="*50)
print(f"Found {len(gv_files)} .gv files in {CHALLENGE_DIR}\n")

for gv_file in gv_files:
    print(f"Processing: {os.path.basename(gv_file)} ...", end=' ')
    try:
        png_path = gv_to_png(gv_file)
        answer, resp_time = send_to_gpt4v(png_path)
        status = check_solution(answer)
        results.append({
            'Puzzle': os.path.basename(gv_file),
            'Status': status,
            'Response Time (s)': f"{resp_time:.2f}",
            'Answer': answer[:60] + ('...' if len(answer) > 60 else '')
        })
        print(f"{status} ({resp_time:.2f}s)")
        print_json_summary(os.path.basename(gv_file), status, f"{resp_time:.2f}", answer[:100])
    except Exception as e:
        results.append({
            'Puzzle': os.path.basename(gv_file),
            'Status': 'error',
            'Response Time (s)': '-',
            'Answer': str(e)
        })
        print(f"error: {e}")
        print_json_summary(os.path.basename(gv_file), 'error', '-', '', str(e))

# Print results table
print("\nResults Summary:\n")
print(tabulate(
    [[r['Puzzle'], r['Status'], r['Response Time (s)'], r['Answer']] for r in results],
    headers=["Puzzle", "Status", "Response Time (s)", "Answer (truncated)"],
    tablefmt="fancy_grid"
)) 