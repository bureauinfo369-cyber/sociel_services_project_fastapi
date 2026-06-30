import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Ensure the path reflects where you copied the font in your Dockerfile
font_path = os.path.join(os.path.dirname(__file__), "fonts", "Arial.ttf")
pdfmetrics.registerFont(TTFont("Arial", font_path))