import sys
import re
import os
from glob import glob
import subprocess

def clean_gv_file(input_path, output_path):
    with open(input_path, 'r') as infile:
        lines = infile.readlines()

    cleaned_lines = []
    inside_digraph = False
    digraph_started = False

    macro_pattern = re.compile(r'GAME_BOARD_NODES|GAME_BOARD_EDGES|OBJECTIVE_STYLE|GRAPH_STYLE|NODE_STYLE|EDGE_STYLE|\$')

    for line in lines:
        # Remove preprocessor lines
        if line.strip().startswith('#'):
            continue
        # Remove macro placeholders and lines with template variables
        if macro_pattern.search(line):
            continue
        # Only keep the first digraph block
        if 'digraph' in line and '{' in line:
            if digraph_started:
                continue  # skip any additional digraphs
            digraph_started = True
            inside_digraph = True
            cleaned_lines.append(line)
            continue
        if inside_digraph:
            cleaned_lines.append(line)
            if '}' in line:
                inside_digraph = False
        elif not digraph_started:
            cleaned_lines.append(line)

    with open(output_path, 'w') as outfile:
        outfile.writelines(cleaned_lines)

    print(f"Cleaned file written to: {output_path}")


def batch_clean_gv_files(directory):
    gv_files = glob(os.path.join(directory, '*.gv'))
    cleaned_files = []
    for gv_file in gv_files:
        if gv_file.endswith('_clean.gv'):
            continue  # skip already cleaned files
        base, ext = os.path.splitext(gv_file)
        output_file = base + '_clean.gv'
        clean_gv_file(gv_file, output_file)
        cleaned_files.append(output_file)
    return cleaned_files


def run_dot_on_files(gv_files):
    results = {}
    for gv_file in gv_files:
        try:
            subprocess.run(['dot', '-Tpng', gv_file, '-O'], check=True, capture_output=True)
            results[gv_file] = 'success'
        except subprocess.CalledProcessError as e:
            results[gv_file] = f'error: {e.stderr.decode().strip()}'
    return results


if __name__ == "__main__":
    # If no arguments, batch clean all .gv files in Challenges and run dot
    if len(sys.argv) == 1:
        challenges_dir = os.path.join(os.path.dirname(__file__), 'Challenges')
        print(f"Batch cleaning all .gv files in {challenges_dir} ...")
        cleaned_files = batch_clean_gv_files(challenges_dir)
        print("\nRunning dot on all cleaned files...")
        results = run_dot_on_files(cleaned_files)
        print("\nSummary:")
        for f, status in results.items():
            print(f"{os.path.basename(f)}: {status}")
    # If two arguments, clean a single file
    elif len(sys.argv) == 3:
        clean_gv_file(sys.argv[1], sys.argv[2])
    else:
        print("Usage:")
        print("  python clean_gv_template.py <input_file.gv> <output_file.gv>")
        print("  python clean_gv_template.py   # batch clean all .gv files in Challenges and run dot")

    cleaned_dir = os.path.join(os.path.dirname(__file__), 'Challenges')
    cleaned_files = glob(os.path.join(cleaned_dir, '*_clean.gv'))

    for gv_file in cleaned_files:
        print(f"Evaluating {gv_file} ...")
        # Replace the following line with your actual evaluation command
        subprocess.run(['python', 'gpt4v_graph_eval.py', gv_file]) 