import os
import re
import csv

def extract_bolded_terms(directory):
    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    results = {}
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = bold_pattern.findall(content)
                results[filename] = [m for m in matches if any(c in m for c in 'āīūṃñṅṇṭḍḷ')]
    return results

def load_reference_words(csv_path):
    reference = set()
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                reference.add(row[0].lower())
    return reference

def audit():
    lists_dir = "_lists/"
    csv_path = "words.csv"
    
    found_terms = extract_bolded_terms(lists_dir)
    reference = load_reference_words(csv_path)
    
    mismatches = []
    for filename, terms in found_terms.items():
        for term in terms:
            # Clean term for comparison (remove punctuation, split if needed)
            clean_term = term.strip().split()[0].rstrip('.,:;')
            if clean_term.lower() not in reference:
                mismatches.append((filename, term))
    
    return mismatches

if __name__ == "__main__":
    mismatches = audit()
    for filename, term in mismatches:
        print(f"File: {filename}, Term: {term}")
