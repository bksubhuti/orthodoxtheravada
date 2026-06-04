import os

terms_dir = "/Users/bhantesubhuti/git/orthodoxtheravada/_terms"
fixed_files = []

for filename in os.listdir(terms_dir):
    if not filename.endswith(".md"):
        continue
    filepath = os.path.join(terms_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    parts = content.split("---")
    if len(parts) >= 3:
        body = parts[2]
        lines = body.split("\n")
        # If lines[0] is empty (newline after ---) and lines[1] is exactly "Verified"
        # then we have a missing blank line before Verified
        if len(lines) > 1 and lines[1] == "Verified":
            # Let's insert a blank line (which means lines[1] becomes empty, and Verified moves to lines[2])
            lines.insert(1, "")
            new_body = "\n".join(lines)
            parts[2] = new_body
            new_content = "---".join(parts)
            with open(filepath, "w", encoding="utf-8") as f_out:
                f_out.write(new_content)
            fixed_files.append(filename)

print("Automatically fixed missing blank lines in the following files:")
for f in fixed_files:
    print(f"- {f}")
print(f"Total fixed: {len(fixed_files)}")
