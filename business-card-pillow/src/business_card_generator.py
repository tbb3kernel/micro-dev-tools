from PIL import Image, ImageDraw, ImageFont
import argparse
from enum import Enum
import os
from typing import Dict, Tuple, Optional

class Color(Enum):
    """
    Represents available color themes for the business card.

    Each color theme is a dictionary containing RGB tuples for 'background',
    'text', and 'border'.
    """
    BLACK_WHITE = {
        "background": (255, 255, 255),  # White (RGB)
        "text": (0, 0, 0),        # Black (RGB)
        "border": (0, 0, 0)        # Black (RGB)
    }
    BLUE_GOLD = {
        "background": (173, 216, 230),  # Light Blue
        "text": (0, 0, 139),        # Dark Blue
        "border": (255, 215, 0)       # Gold
    }
    GRAY_RED = {
        "background": (211, 211, 211), # Light Gray
        "text": (139, 0, 0),       # Dark Red
        "border": (255, 0, 0)       # Red
    }
    WHITE_DARKGRAY = {
        "background": (255, 255, 255),  # White
        "text": (105, 105, 105),      # Dark Gray
        "border": (169, 169, 169)      # Dark Gray
    }

    @classmethod
    def names(cls) -> list[str]:
        """
        Returns a list of valid color theme names.

        Returns:
            list[str]: A list of lowercase color theme names.
        """
        return [name.lower() for name in cls.__members__]



def create_business_card_image(
    name: str,
    title: str,
    company: str,
    contact: Dict[str, str],
    color_theme: str = "black_white",
    output_format: str = "png",
    output_filename: Optional[str] = None,
    font_path: Optional[str] = None,  # Add font_path argument
) -> Image.Image | str | None:
    """
    Creates a business card image using Pillow or generates an SVG representation.

    Args:
        name: The person's full name.
        title: The person's job title.
        company: The company or institution name.
        contact: A dictionary of contact information (e.g., phone, email, website).
        color_theme: The color theme to use (from the Color enum). Defaults to "black_white".
        output_format: The image format ("png", "jpeg", "svg"). Defaults to "png".
        output_filename: Optional filename. If None, a default is generated.
        font_path: Optional path to a TrueType font file (.ttf). If None, a default
                   bundled font will be used.

    Returns:
        The PIL Image object (for PNG/JPEG), the SVG string (for SVG), or None if an error occurs.

    Raises:
        ValueError: If the color theme is invalid.
    """

    try:
        theme = Color[color_theme.upper()].value
    except KeyError:
        raise ValueError(f"Invalid color theme: {color_theme}.  Available themes: {', '.join(Color.names())}")

    card_width = 400
    card_height = 250
    border_width = 5
    padding = 20
    font_size = 20

    # --- Font Handling ---
    if font_path:
        font_file = font_path  # Use the provided font path
    else:
        # Use a bundled font (relative path)
        script_dir = os.path.dirname(__file__)  # Get directory of the script
        font_file = os.path.join(script_dir, "OpenSans-Regular.ttf") # Use relative path

    try:
        font = ImageFont.truetype(font_file, size=font_size)
        title_font = ImageFont.truetype(font_file, size=int(font_size * 0.8))
        contact_font = ImageFont.truetype(font_file, size=int(font_size * 0.7))
    except IOError:
        print("Error: Could not load font file.  Using a default font.")
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        contact_font = ImageFont.load_default()


    if output_format.lower() == "svg":
        return create_svg_business_card(name, title, company, contact, theme, card_width, card_height, border_width, padding, font_file, font_size)

    # PNG/JPEG creation using Pillow:
    image = Image.new("RGB", (card_width, card_height), theme["background"])
    draw = ImageDraw.Draw(image)

    # Draw border
    draw.rectangle(
        [(0, 0), (card_width - 1, card_height - 1)],
        outline=theme["border"],
        width=border_width
    )

    # --- Text Placement ---
    y_offset = padding + border_width
    name_bbox = draw.textbbox((0, 0), name, font=font)
    draw.text(((card_width - name_bbox[2]) / 2, y_offset), name, font=font, fill=theme["text"])
    y_offset += name_bbox[3] + padding // 2

    title_bbox = draw.textbbox((0,0), title, font=title_font)
    draw.text(((card_width - title_bbox[2]) / 2, y_offset), title, font=title_font, fill=theme["text"])
    y_offset += title_bbox[3] + padding // 2

    company_bbox = draw.textbbox((0,0), company, font=title_font)
    draw.text(((card_width - company_bbox[2]) / 2, y_offset), company, font=title_font, fill=theme["text"])
    y_offset += company_bbox[3] + padding

    # Contact Information
    draw.line(((card_width/4, y_offset) ,(card_width*3/4, y_offset)), fill=theme["border"], width=2)
    y_offset += padding // 2

    contact_lines = []
    if "phone" in contact:
        contact_lines.append(f"Phone: {contact['phone']}")
    if "email" in contact:
        contact_lines.append(f"Email: {contact['email']}")
    if "website" in contact:
        contact_lines.append(f"Website: {contact['website']}")
    if "address" in contact:
        contact_lines.append(f"Address: {contact['address']}")

    for line in contact_lines:
        line_bbox = draw.textbbox((0,0), line, font=contact_font)
        draw.text(((card_width - line_bbox[2]) / 2, y_offset), line, font=contact_font, fill=theme["text"])
        y_offset += line_bbox[3] + padding // 4


    # --- Output ---
    if output_filename is None:
        output_filename = f"{name.replace(' ', '_')}_business_card.{output_format.lower()}"
    else:
        base, ext = os.path.splitext(output_filename)
        if ext.lower() != f".{output_format.lower()}":
           output_filename = f"{base}.{output_format.lower()}"

    try:
        image.save(output_filename)
        print(f"Business card saved as {output_filename}")
        return image
    except (IOError, KeyError) as e:
        print(f"Error saving image: {e}")
        return None

def create_svg_business_card(
    name: str,
    title: str,
    company: str,
    contact: Dict[str, str],
    theme: Dict[str, Tuple[int, int, int]],
    card_width: int,
    card_height: int,
    border_width: int,
    padding: int,
    font_file: str,
    font_size: int,
) -> str:
    """
    Creates an SVG representation of a business card.

    Args:
        name: The person's name.
        title: The person's job title.
        company: The company name.
        contact: A dictionary of contact information.
        theme: A dictionary containing color theme information.
        card_width: The width of the card.
        card_height: The height of the card.
        border_width: The width of the border.
        padding: The padding around text elements.
        font_file: The font file to use (for font-family).
        font_size: The base font size.

    Returns:
        A string containing the SVG code.
    """
    title_font_size = int(font_size * 0.8)
    contact_font_size = int(font_size * 0.7)

    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Converts an RGB tuple to a hexadecimal color string."""
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    bg_color = rgb_to_hex(theme["background"])
    text_color = rgb_to_hex(theme["text"])
    border_color = rgb_to_hex(theme["border"])

    svg_lines = [
        f'<svg width="{card_width}" height="{card_height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="100%" height="100%" fill="{bg_color}" />',
        f'  <rect x="{border_width / 2}" y="{border_width / 2}" width="{card_width - border_width}" height="{card_height - border_width}" stroke="{border_color}" stroke-width="{border_width}" fill="none" />',
    ]

    y_offset = padding + border_width
    svg_lines.append(f'  <text x="{card_width / 2}" y="{y_offset + font_size}" text-anchor="middle" font-family="{font_file}" font-size="{font_size}" fill="{text_color}">{name}</text>')
    y_offset += font_size + padding // 2

    svg_lines.append(f'  <text x="{card_width / 2}" y="{y_offset + title_font_size}" text-anchor="middle" font-family="{font_file}" font-size="{title_font_size}" fill="{text_color}">{title}</text>')
    y_offset += title_font_size + padding // 2

    svg_lines.append(f'  <text x="{card_width / 2}" y="{y_offset + title_font_size}" text-anchor="middle" font-family="{font_file}" font-size="{title_font_size}" fill="{text_color}">{company}</text>')
    y_offset += title_font_size + padding

    svg_lines.append(f'  <line x1="{card_width / 4}" y1="{y_offset}" x2="{card_width * 3 / 4}" y2="{y_offset}" stroke="{border_color}" stroke-width="2" />')
    y_offset += padding // 2


    contact_lines = []
    if "phone" in contact:
        contact_lines.append(f"Phone: {contact['phone']}")
    if "email" in contact:
        contact_lines.append(f"Email: {contact['email']}")
    if "website" in contact:
        contact_lines.append(f"Website: {contact['website']}")
    if "address" in contact:
        contact_lines.append(f"Address: {contact['address']}")

    for line in contact_lines:
        svg_lines.append(f'  <text x="{card_width / 2}" y="{y_offset + contact_font_size}" text-anchor="middle" font-family="{font_file}" font-size="{contact_font_size}" fill="{text_color}">{line}</text>')
        y_offset += contact_font_size + padding // 4

    svg_lines.append('</svg>')
    return "\n".join(svg_lines)


def main():
    """
    Parses command-line arguments and generates a business card.
    """
    parser = argparse.ArgumentParser(
        description="Create a professional business card image.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter  # Show default values
    )
    parser.add_argument("name", help="Your full name")
    parser.add_argument("title", help="Your job title")
    parser.add_argument("company", help="Your company or institution name")
    parser.add_argument("-p", "--phone", help="Your phone number")
    parser.add_argument("-e", "--email", help="Your email address")
    parser.add_argument("-w", "--website", help="Your website URL")
    parser.add_argument("-a", "--address", help="Your address")
    parser.add_argument(
        "-c", "--color",
        choices=Color.names(),
        default="black_white",
        help="Color theme"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["png", "jpeg", "svg"],
        default="png",
        help="Output image format"
    )
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("--font", help="Path to a TrueType font file (.ttf)")  # Add --font option

    args = parser.parse_args()

    contact_info = {
        key: value for key, value in vars(args).items() if key in ["phone", "email", "website", "address"] and value
    }
    try:
        card_image = create_business_card_image(
            args.name, args.title, args.company, contact_info, args.color, args.format, args.output, args.font  # Pass font path
        )
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()