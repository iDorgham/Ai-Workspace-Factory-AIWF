import json
import os

def generate_tokens(input_json_path, output_css_path):
    """
    Extracts design tokens from a JSON manifest (e.g., from Figma) 
    and generates a Tailwind v4 compatible @theme tokens.css file.
    """
    if not os.path.exists(input_json_path):
        print(f"Error: {input_json_path} not found.")
        return

    with open(input_json_path, 'r') as f:
        tokens = json.load(f)

    css_content = "@theme {\n"
    
    # Process Colors (OKLCH)
    for color_name, value in tokens.get('colors', {}).items():
        css_content += f"  --color-{color_name.replace('_', '-')}: {value};\n"
    
    # Process Typography
    for size, value in tokens.get('font_sizes', {}).items():
        css_content += f"  --font-size-{size}: {value};\n"
        
    # Process Spacing
    for space, value in tokens.get('spacing', {}).items():
        css_content += f"  --space-{space}: {value};\n"

    css_content += "}\n"

    with open(output_css_path, 'w') as f:
        f.write(css_content)
    print(f"Tokens successfully generated at {output_css_path}")

if __name__ == "__main__":
    # Simulated execution
    print("Design Tokens Generator initialized...")
