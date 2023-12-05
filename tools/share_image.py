import PIL.Image as PIL_Image
from PIL import ImageDraw, ImageFont
from tools.path import (
    PATH_IMAGES,
    PATH_TEXT_FONT,
    PATH_TITLE_FONT
)


def create_image_to_share(score, ending_title, back_image_path):
    """
    Generate an image to share it.
    """

    # Load the images
    back_image = PIL_Image.open(back_image_path)
    tombstone_image = PIL_Image.open(PATH_IMAGES + "ending_background.png",)

    # Resize and paste the tombstone
    tombstone_image = tombstone_image.resize((1024 - 584, 1024 - 584))
    back_image.paste(tombstone_image, (584, 584, 1024, 1024),
                     mask=tombstone_image)

    # Load the font
    title_font = ImageFont.truetype(PATH_TITLE_FONT, 60)
    font = ImageFont.truetype(PATH_TEXT_FONT, 40)

    # Add the text
    draw_image = ImageDraw.Draw(back_image)
    draw_image.text(((1024 + 584) / 2, 910), "Score : " + str(score),
                    font=font, fill=(0, 0, 0), align="center", anchor="mm")
    new_ending_title = ending_title
    for i, car in enumerate(ending_title):
        if i > 10 and car == " ":
            new_ending_title = ending_title[:i] + \
                "\n" + ending_title[i + 1:]
    draw_image.multiline_text(((1024 + 584) / 2, 810), new_ending_title,
                              font=font, fill=(0, 0, 0), align="center", anchor="mm")
    draw_image.text(((1024 + 584) / 2, 710), "POSTRIAS", font=title_font,
                    fill=(0, 0, 0), align="center", anchor="mm")

    # Save the image
    back_image.save("./share_image.png")


if __name__ == "__main__":
    create_image_to_share(100, "La fin de la Science",
                          "./resources/images/ending_order_max.jpg")
