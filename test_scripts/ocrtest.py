import pytesseract
from PIL import Image, ImageDraw, ImageFont

pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'

custom_config = r'--psm 11'
lang = 'eng'

img = Image.open('images2/dialog/2.jpg')  # Load an image
text = pytesseract.image_to_alto_xml(img,lang=lang,config=custom_config)  # Convert the image to text

file_path = 'ocr.xml'  # Update this to your desired file path

# Open the file and write the string to it
with open(file_path, 'wb') as file:
    file.write(text)

d = pytesseract.image_to_data(img,lang=lang,config=custom_config, output_type=pytesseract.Output.DICT)


# Create a draw object
draw = ImageDraw.Draw(img)
font_path = "fonts/msy.ttf"  # Update this path to your font file
font = ImageFont.truetype(font_path, size=12)  # Set the size appropriate to your image

# Iterate over each text line
print(d)
n_boxes = len(d['level'])
for i in range(n_boxes):
    # if int(d['conf'][i]) > 80:  # Check if confidence is greater than 80
        if d['text'][i].strip() != '':  # Check if there is text
            # Get the position and dimensions
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            # Draw the rectangle
            draw.rectangle([x, y, x + w, y + h], outline='red')
            # Encode text to UTF-8 to handle Unicode characters
            text = d['text'][i].encode('utf-8').decode('utf-8')
            # Write the text with specified font
            draw.text((x, y - 10), text, fill='red', font=font)


# Save or display the image
img.save('highlighted_image.jpg')
img.show()