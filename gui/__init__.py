from pathlib import Path

def load_styles():
    style_path = Path(__file__).parent / "styles.qss"
    if style_path.exists():
        return style_path.read_text()
    return ""
