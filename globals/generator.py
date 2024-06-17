"""
    Eid image generator class 
"""
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass
from uuid import uuid4

@dataclass
class EidBuilder:
    """
        EidBuilder Class for generate automatic image

        Args:
            bg_img_path : Eid img saved path in system
            usr_img_path : incoming user image
            usr_name : incoming username

        Output saved in output_path
    """
    bg_img_path:str
    usr_img_path:str
    usr_name:str

    def run (self) : 
        # Load the two images
        background_image = Image.open(self.bg_img_path)
        overlay_image = Image.open(self.usr_img_path)

        # Convert the overlay image to have an alpha channel
        overlay_image = overlay_image.convert("RGBA")
        if overlay_image.width > 1000:
            overlay_image = overlay_image.resize((
                overlay_image.width // 13,
                overlay_image.height //  13
            ))
        else:
            overlay_image = overlay_image.resize((
                overlay_image.width // 2,
                overlay_image.height //  2
            ))

        font = ImageFont.truetype("globals/screens/Cairo-Regular.ttf", size=24)
        draw = ImageDraw.Draw(background_image)

        text = self.usr_name
        text_count = len(text) * 12 + 4
        text_y =  296
        text_x = (background_image.width // 2) - text_count // 2

        draw.text(xy=(text_x, text_y), text=text, font=font, fill=(255, 255, 255))

        # Get the size of the background image
        bg_width, bg_height = background_image.size

        # Get the size of the overlay image
        overlay_width, overlay_height = overlay_image.size

        # Calculate the position to place the overlay image
        x = (bg_width - overlay_width) // 2
        y = (bg_height - overlay_height) // 2


        # Paste the overlay image onto the background image
        background_image.paste(overlay_image, (x, y), overlay_image)

        # Save the resulting image
        self.output_path = f'media/download/{uuid4()}.png'
        background_image.save(self.output_path)

