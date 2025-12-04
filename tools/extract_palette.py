from PIL import Image
import os

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def rgba_str(rgb, a=1.0):
    return f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {a})'

def extract_palette(path, ncolors=5):
    img = Image.open(path).convert('RGB')
    # Resize to speed up
    img = img.resize((120, 120))
    # Quantize to reduce number of colors
    result = img.convert('P', palette=Image.ADAPTIVE, colors=ncolors)
    palette = result.getpalette()
    color_counts = sorted(result.getcolors(), reverse=True)
    colors = []
    for count, idx in color_counts:
        rgb = palette[idx*3:idx*3+3]
        colors.append(tuple(rgb))
    return colors

def pick_colors(colors):
    # Choose first as primary, second as secondary, darkest as overlay base
    primary = colors[0]
    secondary = colors[1] if len(colors) > 1 else colors[0]
    # compute brightness
    def brightness(c):
        return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]
    overlay_base = min(colors, key=brightness)
    return primary, secondary, overlay_base

def write_css(primary, secondary, overlay_base, out_path):
    css = f":root {{\n"
    css += f"  --hero-accent1: {rgb_to_hex(primary)};\n"
    css += f"  --hero-accent2: {rgb_to_hex(secondary)};\n"
    css += f"  --hero-overlay1: {rgba_str(overlay_base, 0.6)};\n"
    css += f"  --hero-overlay2: {rgba_str(overlay_base, 0.28)};\n"
    css += f"}}\n"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print(f'Wrote palette CSS to {out_path}')

def main():
    cwd = os.path.dirname(os.path.dirname(__file__))
    img_path = os.path.join(cwd, 'static', 'images', 'hero.jpg')
    out_path = os.path.join(cwd, 'static', 'hero_palette.css')
    if not os.path.exists(img_path):
        print('hero.jpg not found at', img_path)
        print('Please copy your hero image to static/images/hero.jpg and re-run this script.')
        return 2
    try:
        colors = extract_palette(img_path, ncolors=6)
    except Exception as e:
        print('Error reading image:', e)
        return 3
    primary, secondary, overlay_base = pick_colors(colors)
    write_css(primary, secondary, overlay_base, out_path)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
