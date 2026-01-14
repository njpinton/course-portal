#!/usr/bin/env python3
"""
Clean up Module 00 slides:
1. Remove decorative images (keep only data visualizations/graphs)
2. Fix remaining LaTeX commands that weren't translated
"""

import json
import re

def load_slides(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_slides(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def cleanup_latex(content):
    """Fix remaining LaTeX commands that weren't properly translated."""

    # Remove tikzpicture environments (can't render in browser)
    content = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',
                     '<div class="info"><p><em>See visual diagram in lecture materials</em></p></div>',
                     content, flags=re.DOTALL)

    # Convert \begin{exampleblock}{Title}...\end{exampleblock} to div
    def replace_exampleblock(match):
        title = match.group(1)
        body = match.group(2).strip()
        if title:
            return f'<div class="example"><h4>{title}</h4>{body}</div>'
        return f'<div class="example">{body}</div>'

    content = re.sub(r'\\begin\{exampleblock\}\{([^}]*)\}(.*?)\\end\{exampleblock\}',
                     replace_exampleblock, content, flags=re.DOTALL)

    # Remove algorithmic environments - convert to simple list
    def replace_algorithmic(match):
        algo_content = match.group(1)
        # Convert \STATE to list items
        lines = []
        for line in algo_content.split('\n'):
            line = line.strip()
            if line.startswith('\\STATE'):
                lines.append('<li>' + line.replace('\\STATE', '').strip() + '</li>')
            elif line.startswith('\\FOR') or line.startswith('\\REPEAT') or line.startswith('\\UNTIL') or line.startswith('\\ENDFOR'):
                # Simplify control flow
                cleaned = line.replace('\\FOR', '<strong>For</strong>').replace('\\REPEAT', '<strong>Repeat</strong>')
                cleaned = cleaned.replace('\\UNTIL', '<strong>Until</strong>').replace('\\ENDFOR', '')
                if cleaned.strip():
                    lines.append('<li>' + cleaned.strip() + '</li>')
        if lines:
            return '<ol class="algorithm">' + '\n'.join(lines) + '</ol>'
        return ''

    content = re.sub(r'\\begin\{algorithmic\}\[1\](.*?)\\end\{algorithmic\}',
                     replace_algorithmic, content, flags=re.DOTALL)

    # Remove {\small ...} wrapper but keep content
    content = re.sub(r'\{\\small\s+([^}]+)\}', r'\1', content)

    # Remove remaining \\ line breaks that aren't in math
    # Be careful not to affect $$ blocks
    def fix_linebreaks(match):
        text = match.group(0)
        # Don't touch if it's inside $$ blocks
        if '$$' in text:
            return text
        return text.replace('\\\\', '<br>')

    # Remove stray backslashes from text (but not in math)
    content = re.sub(r'\\&', '&amp;', content)

    # Fix arrows
    content = re.sub(r'\$\\rightarrow\$', '→', content)

    return content

def remove_decorative_images(content):
    """Remove decorative stock images, keep only data visualization graphs."""

    # Images to remove (decorative/stock images)
    decorative_images = [
        'aihistory.jpg',
        'mlapps.jpg',
        'robot.jpg',
        'dataprep.jpg',
        'ethics.jpg',
    ]

    for img in decorative_images:
        # Remove the entire figure element containing this image
        pattern = rf'<figure class="slide-figure">\s*<img src="[^"]*{re.escape(img)}"[^>]*>\s*<figcaption>[^<]*</figcaption>\s*</figure>'
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    return content

def cleanup_slides(data):
    """Apply all cleanup operations to slides."""
    slides = data['slides']

    for slide in slides:
        content = slide['content']

        # Remove decorative images
        content = remove_decorative_images(content)

        # Fix remaining LaTeX
        content = cleanup_latex(content)

        # Clean up excessive whitespace
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        content = content.strip()

        slide['content'] = content

        # Update hasVisualization flag
        slide['hasVisualization'] = '<img src=' in content

    return data

def main():
    input_path = 'static/data/courses/cmsc173/module-00-slides.json'

    print(f"Loading {input_path}...")
    data = load_slides(input_path)

    print("Cleaning up slides...")
    cleaned_data = cleanup_slides(data)

    print(f"Saving to {input_path}...")
    save_slides(cleaned_data, input_path)

    # Count remaining images
    img_count = sum(1 for s in cleaned_data['slides'] if '<img src=' in s['content'])
    print(f"\nDone! Cleaned up Module 00:")
    print(f"  - Removed decorative images")
    print(f"  - Fixed LaTeX commands")
    print(f"  - Remaining data visualizations: {img_count}")

if __name__ == "__main__":
    main()
