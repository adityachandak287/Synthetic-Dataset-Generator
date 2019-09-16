'''
Created on 04-Jun-2019

@author: Aditya Chandak
'''
from __future__ import division, print_function, absolute_import
from PIL import Image, ImageDraw, ImageFont
import glob
import os
import random
import numpy as np
import rstr
from tqdm import tqdm
# root_dir = "C:\\Users\\Aditya Chandak\\Desktop\\Projects\\CereLabs\\Dataset Generation\\DocumentGeneration"
root_dir = os.getcwd()
# input_fonts_dir = "C:\\Users\\Aditya Chandak\\Desktop\\Projects\\CereLabs\\Dataset Generation\\DocumentGeneration\\FONTS"
input_fonts_dir = os.path.join(root_dir, "FONTS")
output_dir = os.path.join(root_dir, "output")


fonts_dir_regular = os.listdir(input_fonts_dir)


def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return [x, y, w, h]


def annotate(pos, box_size, max_size, class_num, file_obj):
    curr_pos = pos
    font_w, font_h = box_size[0], box_size[1]
    x1 = curr_pos[0]
    y1 = curr_pos[1]
    x2 = curr_pos[0] + font_w
    y2 = curr_pos[1]
    x3 = curr_pos[0] + font_w
    y3 = curr_pos[1] + font_h
    x4 = curr_pos[0]
    y4 = curr_pos[1] + font_h
    class_ = class_num
    llst_coords = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    yolo_coords = convert(
        max_size, [float(x1), float(x3), float(y1), float(y3)])
    print('%d %.4f %.4f %.4f %.4f' % (
        class_, yolo_coords[0], yolo_coords[1], yolo_coords[2], yolo_coords[3]), file=file_obj)


sample_input_text = [r'[A-Za-z0-9!@#$%^&*()]{4,25}[A-Za-z0-9!@#$%^&*()]{4,15}',
                     r'[A-Za-z0-9]{1,20}[,.]{1}',
                     r'[A-Za-z0-9]{1,20}[,.?!]{1}',
                     r'[]'
                     r'[0-9]{1,4}[A-Za-z]{2,20}',
                     r'[A-Za-z]{1,3}',
                     r'\d{2}/\d{2}/\d{4}',
                     r'\d{2}/\d{2}/\d{4}',
                     r'[A-Z0-9]{10}',
                     r'[A-Z]{1,12}',
                     r'[A-Z]{4,16}[A-Z]{4,10}',
                     r'[A-Z]{1}[a-z]{6,12}[A-Z]{1}[a-z]{6,12}[A-Z]{1}[a-z]{6,12}',
                     r'[A-Z]{1}[a-z]{6,12}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1}',
                     r'\d{1,2}',
                     r'\d{1,2}',
                     r'\d{1,2}',
                     r'\d{1,2}',
                     r'\d{2,4}\d{4}\d{1,4}',
                     r'[A-Za-z]{15,35}',
                     r'[/(*&^%$#@!|\'"<>{]{1}[A-Za-z0-9]{2,18}'
                     ]


# Going through the page from top left, randomly selecting spacing and
# placing text on the image
num_of_images = 100
font_size_min, font_size_max = 10, 14
for image_counter in tqdm(range(1, num_of_images + 1)):
    # yolo_txt_file = output_dir+"\\"+str(image_counter)+".txt"
    yolo_txt_file = os.path.join(output_dir, str(image_counter) + ".txt")
    f = open(yolo_txt_file, 'w')
    max_sizes = [512, 512, 512, 640, 320, 400]
    boundary = 0
    curr_pos = [0, 0]
    # x_offset, y_offset = random.randint(
    #     0, round(max_w*0.2)), random.randint(0, round(max_h*0.2))
    x_offset, y_offset = random.randint(
        0, 20), random.randint(0, 20)
    curr_pos[0] += x_offset
    curr_pos[1] += y_offset
    line_h = 0

    input_text = rstr.xeger(random.choice(sample_input_text))

    # font_path = random.choice(glob.glob(input_fonts_dir+"\\*\\*.ttf"))
    font_path = random.choice(glob.glob(input_fonts_dir + "/*/*.ttf"))
    font = ImageFont.truetype(
        font_path, random.randint(font_size_min, font_size_max))
    input_text_linewise = input_text.split("\n")
    font_w_list, font_h_list = [], []
    for line in input_text_linewise:
        font_w_list.append(font.getsize(line)[0])
        font_h_list.append(font.getsize(line)[1])

    font_w, font_h = max(font_w_list), sum(font_h_list)

    # random.choice(max_sizes), random.choice(max_sizes)
    max_w, max_h = round(font_w * 1.2), round(font_h * 1.2)
    img = Image.new('RGB', (max_w, max_h),
                    color=(255, 255, 255))

    d = ImageDraw.Draw(img)
    x1 = random.randint(boundary, max_w - boundary - font_w)
    y1 = random.randint(boundary, max_h - boundary - font_h)
    d.text((x1, y1), input_text, font=font, fill=(0, 0, 0),)

    #annotate(pos, box_size, max_size, class_num, file_obj)
    annotate([x1, y1], [font_w, font_h], [max_w, max_h], 1, f)

    img.save(os.path.join(output_dir, str(image_counter) + ".jpg"))
    f.close()
    # print("Image " + str(image_counter) + " saved.")
