# Created on 14 November 2019
# Defines Game object

from os.path import isfile
from pygame import Surface
from pygame.image import load
from pygame.transform import scale
from pygame.display import get_surface
from scripts.functions import get_scaled_font
from scripts.VerticalScroller import VerticalScroller


class Game:
    def __init__(self, name):
        self.name = name
        self.play_rect = None
        self.description = VerticalScroller((0, 0))
        if not isfile(name + "/readme"):
            with open(name + "/readme", "w+") as file:
                file.write("No Description Provided")

    def get_display(self, dim, font):
        s = Surface(dim)

        # Draw name text
        text = font.render(self.name, 1, (255, 255, 255))
        text_rect = text.get_rect(center=(int((dim[0] - dim[1]) / 2), int(dim[1] / 2)))
        s.blit(text, text_rect)

        if isfile(self.name + "/icon.png"):
            # Load image
            img = load(self.name + "/icon.png")
            # Fit it into a square
            size = img.get_size()
            frac = dim[1] / max(size)
            # Scale it and draw it
            img = scale(img, (int(size[0] * frac), int(size[1] * frac)))
            img_rect = img.get_rect(center=(dim[0] - int(dim[1] / 2), int(dim[1] / 2)))
            s.blit(img, img_rect)

        return s

    def get_description(self):
        dim = get_surface().get_size()
        self.description = VerticalScroller(dim)

        line_h = max(10, int(dim[1] / 20))

        font = get_scaled_font(dim[0], line_h, "|", "Times New Roman")
        # Split the lines into paragraphs (new line denoted by '  ')
        paragraphs = []
        with open(self.name + "/readme", 'r') as file:
            file_text = "".join(file)
            while "\n" in file_text:
                idx = file_text.index("\n")
                file_text = file_text[:idx] + " " + file_text[idx + 1:]
            while "  " in file_text:
                idx = file_text.index("  ")
                paragraphs.append(file_text[:idx])
                file_text = file_text[idx + 2:]
            if file_text != "":
                paragraphs.append(file_text)
        # Split the paragraphs into lines
        for p in paragraphs:
            lines = wrap_text(p, font, dim[0], line_h)
            # Go through each word in each line
            for line in lines:
                w = 0
                displays = []
                for word in line:
                    if "\\i" not in word:
                        # Draw it if it is a word
                        text = font.render(word, 1, (255, 255, 255))
                        displays.append(text)
                        w += font.size(word)[0]
                    else:
                        # Otherwise get image and draw it if it exists
                        # Ignore any spaces with "\" in front
                        img = word[2:]
                        if isfile(img):
                            img = load(img)
                        else:
                            img = Surface((line_h, line_h))
                        # Scale the image
                        size = img.get_size()
                        frac = line_h / max(size)
                        img = scale(img, (int(frac * size[0]), int(frac * size[1])))
                        displays.append(img)
                        w += line_h
                # Draw this line onto a surface
                s = Surface((w, line_h))
                x = 0
                for piece in displays:
                    piece_dim = piece.get_size()
                    s.blit(piece, (x, int((line_h - piece_dim[1]) / 2)))
                    x += piece_dim[0]
                # Add surface to scroller
                self.description.add_item(s, "")
        # Draw the play button
        w, h = dim[0] * .8, line_h * 3
        s = Surface((w, h))
        font = get_scaled_font(w, h, "Play! Back", "Times New Roman")
        # Play button
        text = font.render("Play!", 1, (0, 200, 0))
        s.blit(text, (0, int((h - font.size("Play!")[1]) / 2)))
        # Back button
        text = font.render("Back", 1, (200, 0, 0))
        s.blit(text, (w - font.size("Back")[0], int((h - font.size("Back")[1]) / 2)))
        self.description.add_item(s, "action")
        get_surface().fill((0, 0, 0))
        get_surface().blit(self.description.surface, (0, 0))


# Breaks a string into the minimum number of lines needed to display it
def wrap_string(string, font, w):
    strs = []
    while len(string) > 0:
        for i in reversed(range(len(string) + 1)):
            temp = string[:i]
            if font.size(temp)[0] < w:
                string = string[i:]
                strs.append(temp)
                break
    return strs


# Breaks text into the minimum number of lines needed to display it
# Divides text into words with ' ' delimiter
def wrap_text(string, font, w, img_w):
    words = []
    word = ""
    # Split into words, ignoring "\ "
    while string.count(" ") > 0:
        idx = string.index(" ")
        if idx == 0 or string[idx - 1] != "\\":
            words.append(word + string[:idx + 1])
            word = ""
        else:
            word += string[:idx - 1] + " "
        string = string[idx + 1:]
    words.append(string)
    # Stores a 2d array of words
    strs = []
    # Stores each line in an array of words
    line = []
    i = 0
    # Go through each word
    img_count = 0
    line_w = 0
    was_img = False
    while i < len(words):
        word = words[i]
        # Check if our word is an image
        is_img = "\i" in word
        # Add a space if the word is after an image
        if not is_img and was_img:
            word = " " + word
        was_img = is_img
        # Get word width
        word_w = img_w if is_img else font.size(word)[0]
        # If it fits, go to the next word
        if line_w + word_w < w:
            line.append(word)
            line_w += word_w
            i += 1
        # If it doesn't and our line has other words, add the line
        elif line != "":
            strs.append(line)
            line = []
            line_w = 0
        # Otherwise if it is an image, just add it
        elif is_img:
            strs.append([word])
        # If it is a words, break it up
        else:
            wrap = wrap_string(word, font, w)
            # Add all lines except the last one
            for text in wrap[:-1]:
                strs.append([text])
            line = wrap[-1:]
            line_w = font.size(line[0])[0]
            i += 1
    strs.append(line)
    return strs
