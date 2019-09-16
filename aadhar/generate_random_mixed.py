'''
Created on 17-May-2019

@author: cerelabs
'''
from __future__ import division, print_function, absolute_import
from PIL import Image, ImageDraw, ImageFont
import glob
import os
import random
# import matplotlib.path as mplPath
import numpy as np
import rstr
from shapely.geometry import Polygon, Point
import csv
# import cv2

root_dir = os.getcwd()
input_fonts_dir = os.path.join(root_dir, os.pardir, "resources", "FONTS")
fonts_dir_regular = os.listdir(input_fonts_dir)
qr_dir = root_dir
aadhar_output_dir = os.path.join(root_dir, "output", "random_mixed")

file_suffix = "_aadhar_random_mixed"


def convert(size, box):
    # size list[widht, height], box list[x1,x2,y1,y2]
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


def denormalize(size, box):
    # size list[width, height] of image, box list[x,y,w,h] from LabelImg
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]

    x = x * size[0]
    y = y * size[1]
    w = w * size[0]
    h = h * size[1]

    x1 = (2 * x - w) / 2.0
    y1 = (2 * y - h) / 2.0
    x3 = (2 * x + w) / 2.0
    y3 = (2 * y + h) / 2.0

    x4 = x1
    x2 = x3
    y4 = y3
    y2 = y1

    return [x1, y1, x2, y2, x3, y3, x4, y4]


sample_input_text = [r'\d{4} \d{4} \d{4}']


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
    # d.rectangle([(x1, y2), (x3, y3)], fill=None, outline=(255, 0, 0))
    llst_coords = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    # d = ImageDraw.Draw(img)
    # d.rectangle([(x1,y1), (x3,y3)], fill=None, outline=(255, 0, 0))

    yolo_coords = convert(
        max_size, [float(x1), float(x3), float(y1), float(y3)])
    print('%d %.4f %.4f %.4f %.4f' % (
        class_, yolo_coords[0], yolo_coords[1], yolo_coords[2], yolo_coords[3]), file=file_obj)


def annotate2(coords, class_num, file_obj, max_size):
    x1 = coords[0]
    y1 = coords[1]
    x2 = coords[2]
    y2 = coords[3]
    x3 = coords[4]
    y3 = coords[5]
    x4 = coords[6]
    y4 = coords[7]

    class_ = int(class_num)
    llst_coords = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    # d = ImageDraw.Draw(img)
    # d.rectangle([(x1,y1), (x3,y3)], fill=None, outline=(255, 0, 0))
    yolo_coords = convert(
        max_size, [float(x1), float(x3), float(y1), float(y3)])
    print('%d %.4f %.4f %.4f %.4f' % (class_, yolo_coords[0], yolo_coords[
          1], yolo_coords[2], yolo_coords[3]), file=file_obj)


def checkPosition(curr, qr_pos):
    position = Point(curr[0], curr[1])
    qrBox = Polygon(qr_pos)
    if qrBox.intersects(position):
        return True
    else:
        return False


def checkTextBox(curr, text_w, text_h, qr_pos):
    textBox = Polygon([tuple(curr), (curr[0] + text_w, curr[1]),
                       (curr[0] + text_w, curr[1] + text_h), (curr[0], curr[1] + text_h)])
    qrBox = Polygon(qr_pos)
    return textBox.intersects(qrBox)


def validatePosition(curr, size, existing):
    img_box = Polygon([tuple(curr), (curr[0] + size[0], curr[1]),
                       (curr[0] + size[0], curr[1] + size[1]), (curr[0], curr[1] + size[1])])

    flag = True
    for region in existing:
        poly = Polygon(region)
        if poly.intersects(img_box):
            flag = False
            break
    return flag


def createAnnotation(curr_size, curr, infile, outfile, max_size):
    with open(infile[:-4] + ".txt", 'rt') as csvfile:
        lines = csv.reader(csvfile, delimiter=' ')
        box = [0] * 4
        for line in lines:

            box[0] = float(line[1])
            box[1] = float(line[2])
            box[2] = float(line[3])
            box[3] = float(line[4])

            normalised_values = denormalize(curr_size, box)
            for i in range(len(normalised_values)):
                if i % 2 == 0:
                    normalised_values[i] += curr[0]
                else:
                    normalised_values[i] += curr[1]
            annotate2(normalised_values, line[0], outfile, max_size)


num_of_images = 5
count = [0, 0, 0, 0]
font_size_min, font_size_max = 10, 14
for image_counter in range(1, num_of_images + 1):

    rotate_angle = random.random() * (random.randint(-1, 1)) / 2

    regions = []

    yolo_txt_file = os.path.join(aadhar_output_dir, str(
        image_counter) + file_suffix + ".txt")
    f = open(yolo_txt_file, 'w')
    # max_sizes = [720, 720, 720, 640, 512, 400]

    boundary = 10
    curr_pos = [0, 0]
    # x_offset, y_offset = random.randint(0, round(max_w*0.2)),
    # random.randint(0, round(max_h*0.2))
    x_offset, y_offset = random.randint(0, 50), random.randint(0, 50)
    curr_pos[0] += x_offset
    curr_pos[1] += y_offset
    line_h = 0
    font_path = random.choice(glob.glob(input_fonts_dir + "/*/*.ttf"))

    x1, y1 = None, None
    img_w, img_h = None, None
    aadhar_dir = ""
    class_ = -1
    type_ = None

    max_sizes = [1200, 1080, 900, 1440]
    max_w, max_h = random.choice(max_sizes), random.choice(max_sizes)

    img = Image.new('RGB', (max_w, max_h), color=(255, 255, 255))

    for indiv_counter in range(random.randint(2, 6)):
        attempts = 0
        while(attempts < 5):
            dice = random.random()

            if dice < 0.25:
                aadhar_dir = random.choice(
                    glob.glob(root_dir + "/output/big/*.jpg"))
                class_ = 6
                type_ = "big"
                count[0] += 1
            elif dice >= 0.25 and dice < 0.5:
                aadhar_dir = random.choice(
                    glob.glob(root_dir + "/output/electronic/*.jpg"))
                class_ = 9
                type_ = "electronic"
                count[1] += 1
            elif dice >= 0.5 and dice < 0.75:
                aadhar_dir = random.choice(
                    glob.glob(root_dir + "/output/medium/*.jpg"))
                class_ = 7
                type_ = "medium"
                count[2] += 1
            else:
                aadhar_dir = random.choice(
                    glob.glob(root_dir + "/output/small/*.jpg"))
                class_ = 8
                type_ = "small"
                count[3] += 1
            aadhar = Image.open(aadhar_dir)
            # aadhar_dir = random.choice(glob.glob(root_dir + "/output/big/*.jpg"))
            # class_ = 6
            # type_ = "big"
            # count[0] += 1

            img_w, img_h = aadhar.size[0], aadhar.size[1]

            boundary = 20

            refactor = 1
            if type_ == "big" or type_ == "electronic":
                refactor = random.randint(6, 14) / 10.0
            w_1 = round(img_w * refactor)
            h_1 = round(img_h * refactor)
            x1 = random.randint(boundary, max_w - w_1 - boundary)
            y1 = random.randint(boundary, max_h - h_1 - boundary)

            attempts += 1
            # x1 = random.randint(boundary, max_w - w_1 - boundary)
            # y1 = random.randint(boundary, max_h - h_1 - boundary)

            if validatePosition([x1, y1], [w_1, h_1], regions):
                aadhar_res = aadhar.resize((w_1, h_1), resample=0)
                regions.append([(x1, y1), (x1 + w_1, y1),
                                (x1 + w_1, y1 + h_1), (x1, y1 + h_1)])
                img.paste(aadhar_res, (x1, y1), aadhar_res.convert('RGBA'))
                createAnnotation([w_1, h_1], [x1, y1],
                                 aadhar_dir, f, [max_w, max_h])
                annotate([x1, y1], aadhar_res.size,
                         [max_w, max_h], class_, f)
                attempts = 10

    for cell_counter in range(random.randint(10, 20)):
        while(True):
            font_random_path = "Calibri.ttf"
            font_random = ImageFont.truetype(
                font_random_path, random.randint(16, 36))

            input_text = rstr.xeger(r'[A-Za-z0-9]{4,15}')
            rand_w, rand_h = font_random.getsize(
                input_text)[0], font_random.getsize(input_text)[1]
            rand_x1 = random.randint(boundary, max_w - boundary - rand_w)
            rand_y1 = random.randint(boundary, max_h - boundary - rand_h)

            if validatePosition([rand_x1, rand_y1], [rand_w, rand_h], regions):
                regions.append([(rand_x1, rand_y1), (rand_x1 + rand_w, rand_y1),
                                (x1 + rand_w, y1 + rand_h), (x1, y1 + rand_h)])
                # img.paste(aadhar, (rand_x1,rand_y1), aadhar.convert('RGBA'))
                d = ImageDraw.Draw(img)
                d.text((rand_x1, rand_y1), input_text,
                       font=font_random, fill=(0, 0, 0))
                break
            else:
                continue

    # img = img.rotate(rotate_angle, expand = 1 )

    img.save(os.path.join(aadhar_output_dir, str(
        image_counter) + file_suffix + ".jpg"))
    f.close()
    # + str(rotate_angle) + str(img.size))
    print("Aadhar " + str(image_counter) + " is saved.")

print(count)
