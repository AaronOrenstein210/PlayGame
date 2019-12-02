# Created on 14 November 2019
# Defines misc. functions

from pygame.font import SysFont


# Gets the biggest font that fits the text within max_w and max_H
def get_scaled_font(max_w, max_h, text, font_name):
    font_size = 0
    font = SysFont(font_name, font_size)
    w, h = font.size(text)
    while w < max_w and h < max_h:
        font_size += 1
        font = SysFont(font_name, font_size)
        w, h = font.size(text)
    return SysFont(font_name, font_size - 1)


def get_widest_string(strs, font_type):
    biggest = ""
    last_w = 0
    font = SysFont(font_type, 12)
    for str in strs:
        if font.size(str)[0] > last_w:
            biggest = str
            last_w = font.size(str)[0]
    return biggest


# Breaks a string into the minimum number of lines needed to display it
def wrap_string(str, font, w):
    strs = []
    while len(str) > 0:
        for i in reversed(range(len(str) + 1)):
            temp = str[:i]
            if font.size(temp)[0] < w:
                str = str[i:]
                strs.append(temp)
                break
    return strs


# Breaks text into the minimum number of lines needed to display it
# Divides text into words with ' ' delimiter
def wrap_text(str, font, w):
    words = []
    while str.count(" ") > 0:
        idx = str.index(" ")
        words.append(str[:idx])
        str = str[idx + 1:]
    words.append(str)
    strs = []
    line = ""
    i = 0
    # Go through each word
    while i < len(words):
        # Get the new line and check its width
        temp = line + (" " if line != "" else "") + words[i]
        # If it fits, go to the next word
        if font.size(temp)[0] < w:
            line = temp
            i += 1
        # If it doesn't and our line has other words, add the line
        elif line != "":
            strs.append(line)
            line = ""
        # Otherwise the word doesn't fit in one line so break it up
        else:
            wrap = wrap_string(temp, font, w)
            for text in wrap[:-1]:
                strs.append(text)
            if i < len(words) - 1:
                line = wrap[len(wrap) - 1]
            else:
                strs.append(wrap[len(wrap) - 1])
            i += 1
    strs.append(line)
    return strs
