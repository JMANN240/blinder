import click
from PIL import Image

def calculateBraille(string):
	braille = 0x2800
	braille += 0x01 * ('1' in string)
	braille += 0x02 * ('2' in string)
	braille += 0x04 * ('3' in string)
	braille += 0x08 * ('4' in string)
	braille += 0x10 * ('5' in string)
	braille += 0x20 * ('6' in string)
	braille += 0x40 * ('7' in string)
	braille += 0x80 * ('8' in string)
	return braille

def dotOffset(dot, character_width_in_pixels, character_height_in_pixels):
	if dot in (1, 2, 3, 7):
		x_offset = 0
	elif dot in (4, 5, 6, 8):
		x_offset = int(character_width_in_pixels / 2)
	
	if dot in (1, 4):
		y_offset = 0
	elif dot in (2, 5):
		y_offset = int(character_height_in_pixels * 1 / 4)
	elif dot in (3, 6):
		y_offset = int(character_height_in_pixels * 2 / 4)
	elif dot in (7, 8):
		y_offset = int(character_height_in_pixels * 3 / 4)
	
	return (x_offset, y_offset)

@click.command()
@click.option('--filepath', help="The path to the image to blind", prompt=True, required=True, type=str)
@click.option('--width', default=40, help="The width of the art in characters", type=int)
@click.option('--aspect', default=1.3, help="The ratio of character height to character width", type=float)
@click.option('--threshold', default=0.5, help="The value threshold for white", type=float)
@click.option('--invert', default=False, help="The ratio of character height to character width", type=float)
def main(filepath, width, aspect, threshold, invert):
	width_in_characters = width
	character_aspect_ratio = aspect

	with Image.open(filepath) as image:
		height_in_characters = int((image.height / image.width) * width_in_characters / character_aspect_ratio)
		character_width_in_pixels = int(image.width / width_in_characters)
		character_height_in_pixels = int(image.height / height_in_characters)
		pixels = image.load()
		for y in range(height_in_characters):
			for x in range(width_in_characters):
				character_string = ""
				for dot in range(8):
					x_offset, y_offset = dotOffset(dot+1, character_width_in_pixels, character_height_in_pixels)
					sample_x = int(image.width * x / width_in_characters) + x_offset
					sample_y = int(image.height * y / height_in_characters) + y_offset
					pixel = pixels[sample_x, sample_y]
					r = pixel[0] / 255
					g = pixel[1] / 255
					b = pixel[2] / 255
					v = 0.299 * r + 0.587 * g + 0.114 * b
					if invert:
						v = 1 - v
					if v < threshold:
						character_string += str(dot+1)
				print(chr(calculateBraille(character_string)), end='')
			print()

if __name__ == '__main__':
	main()
