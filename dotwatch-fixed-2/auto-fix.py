#!/usr/bin/env python3
"""
DotWatch Auto-Fix Script
Automatically applies user-account dynamic changes to ALL HTML files.

Usage:
    1. Put this script in the ROOT of your project (next to index.html)
    2. Run: python auto-fix.py
    3. Done! All HTML files are updated automatically.
"""

import os
import re
import sys

# What to find and replace in each HTML file
OLD_LOGIN_LINK = r'<a href="[^"]*login[^"]*" class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*حساب کاربری\s*</span>\s*</a>'

NEW_CONTAINER = '<div id="user-account-container"></div>'

AUTH_SCRIPT = '<script src="./js/auth.js"></script>'

def get_relative_prefix(filepath):
    """Calculate how many ../ we need from this file to reach root."""
    rel = os.path.relpath(filepath)
    depth = rel.count(os.sep)
    if depth == 0:
        return './'
    return '../' * depth

def fix_html_file(filepath):
    """Apply fixes to a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    prefix = get_relative_prefix(filepath)

    # 1. Replace the static login link with dynamic container
    # Use a more flexible regex
    pattern = r'<a\s+href="[^"]*login/index\.html"\s+class="action-btn"\s*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*حساب کاربری\s*</span>\s*</a>'
    content = re.sub(pattern, NEW_CONTAINER, content, flags=re.DOTALL)

    # Also try without the specific href pattern (broader match)
    if 'user-account-container' not in content:
        pattern2 = r'<a\s+[^>]*class="action-btn"[^>]*>\s*<svg[^>]*>.*?</svg>\s*<span>\s*حساب کاربری\s*</span>\s*</a>'
        content = re.sub(pattern2, NEW_CONTAINER, content, count=1, flags=re.DOTALL)

    # 2. Add auth.js script tag before closing </body> or before other scripts
    if 'auth.js' not in content:
        # Try to insert before </body>
        if '</body>' in content:
            # Insert before the last </body>
            content = content.replace(
                '</body>',
                f'  <!-- User Auth -->\n  <script src="{prefix}js/auth.js"></script>\n</body>',
                1
            )
        else:
            # Fallback: append at end
            content += f'\n<script src="{prefix}js/auth.js"></script>\n'

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def find_html_files(root_dir):
    """Find all HTML files recursively."""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden folders and common non-project folders
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
        for fname in filenames:
            if fname.endswith('.html'):
                html_files.append(os.path.join(dirpath, fname))
    return html_files

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    print("=" * 60)
    print("   DotWatch Auto-Fix: Dynamic User Account")
    print("=" * 60)
    print(f"\nScanning directory: {root}\n")

    html_files = find_html_files(root)

    if not html_files:
        print("❌ No HTML files found!")
        sys.exit(1)

    print(f"Found {len(html_files)} HTML file(s):\n")

    modified = 0
    for filepath in html_files:
        rel_path = os.path.relpath(filepath, root)
        was_modified = fix_html_file(filepath)
        status = "✅ Modified" if was_modified else "⏭️  Skipped (already fixed or no match)"
        print(f"  {status}  →  {rel_path}")
        if was_modified:
            modified += 1

    print(f"\n{'=' * 60}")
    print(f"Done! {modified} file(s) modified.")
    print(f"{'=' * 60}")
    print("""
Next steps:
  1. Copy auth.js to your js/ folder
  2. Append user-account.css to your css/style.css
  3. Open any page and test!
""")

if __name__ == '__main__':
    main()