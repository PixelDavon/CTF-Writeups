import os
import sys
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print('Usage: python new.py "Tracebash CTF"')
        sys.exit(1)

    ctf_name = sys.argv[1]
    ctf_root = os.path.join("Writeups", ctf_name)
    template_file = "TEMPLATE.md"
    current_date = datetime.now().strftime("%B %Y")

    if not os.path.exists(ctf_root):
        print(f"Error: Directory '{ctf_root}' does not exist.")
        sys.exit(1)
    if not os.path.exists(template_file):
        print(f"Error: Template '{template_file}' does not exist.")
        sys.exit(1)


    with open(template_file, 'r') as f:
        template_content = f.read()

    # Get the depth of the root to calculate levels correctly
    root_depth = ctf_root.rstrip(os.path.sep).count(os.path.sep)

    for root, dirs, files in os.walk(ctf_root):
        # Calculate current depth
        current_depth = root.rstrip(os.path.sep).count(os.path.sep) - root_depth
        
        # We only want to process folders at depth 2 (e.g., Writeups/CTF/Category/Challenge)
        if current_depth != 2:
            continue

        readme_path = os.path.join(root, "README.md")
        
        if os.path.exists(readme_path):
            continue

        category = os.path.basename(os.path.dirname(root))
        challenge_name = os.path.basename(root)
        
        # Fill template...
        filled = template_content.replace("**CTF:** EventName Year", f"**CTF:** {ctf_name}")
        filled = filled.replace("**Category:** Category", f"**Category:** {category}")
        filled = filled.replace("**Date:** Month YYYY or YYYY", f"**Date:** {current_date}")
        filled = filled.replace("# Challenge Name", f"# {challenge_name}")
        
        with open(readme_path, 'w') as f:
            f.write(filled)
        print(f"[+][CREATED] {readme_path} (Cat: {category})")

if __name__ == "__main__":
    main()