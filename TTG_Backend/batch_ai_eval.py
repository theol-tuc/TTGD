import os
from glob import glob
import subprocess
import json

challenges_dir = os.path.join(os.path.dirname(__file__), 'Challenges')
cleaned_files = glob(os.path.join(challenges_dir, '*_clean.gv'))

results = []

for gv_file in cleaned_files:
    print(f"Evaluating {os.path.basename(gv_file)} ...")
    proc = subprocess.run(
        ['python', 'gpt4v_graph_eval.py', gv_file],
        capture_output=True, text=True
    )
    output_lines = proc.stdout.strip().splitlines()
    try:
        result_json = json.loads(output_lines[-1])
        results.append({
            "Puzzle": os.path.basename(gv_file),
            "Status": result_json.get("status", "unknown"),
            "Response Time": result_json.get("response_time", "-"),
            "Answer": result_json.get("answer", "")[:50],
            "Error": result_json.get("error", "")
        })
    except Exception as e:
        results.append({
            "Puzzle": os.path.basename(gv_file),
            "Status": "error",
            "Response Time": "-",
            "Answer": f"Could not parse result: {e}",
            "Error": proc.stdout.strip()[-200:]
        })

# Print summary table
print("\nSummary:\n")
print(f"{'Puzzle':<25} {'Status':<10} {'Response Time':<15} {'Answer (truncated)':<50} {'Error':<30}")
print("-" * 140)
for r in results:
    print(f"{r['Puzzle']:<25} {r['Status']:<10} {r['Response Time']:<15} {r['Answer']:<50} {r['Error']:<30}")

# Save to file
with open("ai_eval_summary.txt", "w") as f:
    f.write(f"{'Puzzle':<25} {'Status':<10} {'Response Time':<15} {'Answer (truncated)':<50} {'Error':<30}\n")
    f.write("-" * 140 + "\n")
    for r in results:
        f.write(f"{r['Puzzle']:<25} {r['Status']:<10} {r['Response Time']:<15} {r['Answer']:<50} {r['Error']:<30}\n") 