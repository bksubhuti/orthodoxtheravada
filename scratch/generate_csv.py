import re
import csv
import os

def generate_csv():
    combined_path = '/Users/bhantesubhuti/git/orthodoxtheravada/_terms/combined_glossary_files.txt'
    output_path = '/Users/bhantesubhuti/git/orthodoxtheravada/glossary_status.csv'
    
    with open(combined_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by the header pattern
    pattern = re.compile(r'==> (.*?) <==\n')
    parts = pattern.split(content)
    
    file_blocks = []
    for i in range(1, len(parts), 2):
        filename = parts[i]
        file_content = parts[i+1]
        file_blocks.append((filename, file_content))
        
    print(f"Read {len(file_blocks)} files from combined_glossary_files.txt")
    
    csv_rows = []
    for filename, file_content in file_blocks:
        # Extract slug
        slug = os.path.splitext(filename)[0]
        link = f"https://orthodoxtheravada.org/glossary/{slug}/"
        
        # Check if verified: look for a standalone line with "verified" or "verfied" (case-insensitive)
        lines = file_content.split('\n')
        is_verified = False
        
        # Find where frontmatter ends
        fm_count = 0
        fm_end = -1
        for idx, line in enumerate(lines):
            if line.strip() == '---':
                fm_count += 1
                if fm_count == 2:
                    fm_end = idx
                    break
        
        # Look for verified within a few lines after frontmatter
        if fm_end != -1:
            for l in lines[fm_end+1:fm_end+5]:
                clean_line = l.strip().lower().rstrip(':').strip()
                if clean_line in ['verified', 'verfied']:
                    is_verified = True
                    break
                    
        verified_str = "Yes" if is_verified else "No"
        csv_rows.append({
            'link': link,
            'filename': filename,
            'verified': verified_str
        })
        
    # Write to CSV
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['link', 'filename', 'verified'])
        writer.writeheader()
        writer.writerows(csv_rows)
        
    print(f"Successfully generated CSV at: {output_path}")
    print(f"Total rows: {len(csv_rows)}")
    
    # Let's see how many are verified vs unverified
    verified_count = sum(1 for row in csv_rows if row['verified'] == 'Yes')
    unverified_count = sum(1 for row in csv_rows if row['verified'] == 'No')
    print(f"Verified count: {verified_count}")
    print(f"Unverified count: {unverified_count}")

if __name__ == '__main__':
    generate_csv()
