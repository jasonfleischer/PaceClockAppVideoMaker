#!/usr/bin/python3

from PIL import Image, ImageDraw
import cairosvg

class ImageGenerator:

    @staticmethod
    def generate_background(destination_path, width, height, color = (255, 0, 0)):
        image = Image.new("RGB", (width, height), color=color)
        draw = ImageDraw.Draw(image)
        image.save(destination_path)
        image.close()

    @staticmethod
    def generate_background_gradient(destination_path, width, height, color1 = (255, 0, 0), color2 = (0, 0, 255), vertical=True):
        image = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(image)
        if vertical :
            for y in range(height):
                r = int((color2[0] - color1[0]) * (y / height) + color1[0])
                g = int((color2[1] - color1[1]) * (y / height) + color1[1])
                b = int((color2[2] - color1[2]) * (y / height) + color1[2])
                draw.line((0, y, width, y), fill=(r, g, b))
        else:
            for x in range(width):
                r = int((color2[0] - color1[0]) * (x / width) + color1[0])
                g = int((color2[1] - color1[1]) * (x / width) + color1[1])
                b = int((color2[2] - color1[2]) * (x / width) + color1[2])
                draw.line((x, 0, x, height), fill=(r, g, b))
        image.save(destination_path)
        image.close()

    @staticmethod
    def convert_svg_to_png(source_path, destination_path):
        cairosvg.svg2png(url=source_path, write_to=destination_path)

    @staticmethod
    def generate_image_with_background_color(source_path_with_alpha, destination_path, color=(255, 0, 0)):
        image = Image.open(source_path_with_alpha)
        width, height = image.size
        new_image = Image.new("RGB", (width, height), color)
        mask = image.convert("RGBA").split()[-1]
        new_image.paste(image, (0, 0), mask)
        new_image.save(destination_path)
        image.close()
        new_image.close()
