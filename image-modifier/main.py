from PIL import Image, ImageDraw, ImageFont

def create_modified_image(cloudlet_name):
    # Open the image
    image = Image.open('cloudleton.png')

    # Initialize the drawing context with the image
    draw = ImageDraw.Draw(image)

    # Define the text and font to use
    text = cloudlet_name
    font = ImageFont.truetype('Heebo-Medium.ttf', size=730)

    # Get the text size
    text_width, text_height = draw.textsize(text, font)

    # Calculate the position of the text
    x = (image.width - text_width) / 2
    y = (image.height - text_height) * 0.72

    # Draw the white text on the image
    draw.text((x, y), text, font=font, fill=(255, 255, 255), stroke_width=30, stroke_fill='black')

    # Save the modified image
    image.save('final_cloudleton.png')
