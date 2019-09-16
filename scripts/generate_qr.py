'''
Created on 25-May-2019

@author: Aditya Chandak
'''
from __future__ import division, print_function, absolute_import
from PIL import Image, ImageDraw, ImageFont
import glob
import os
import random
import numpy as np
import rstr
import sys
from tqdm import tqdm
from shapely.geometry import Polygon, Point


'''
Arguments: num_of_images fonts_dir output_root qr_codes
'''

root_dir = os.getcwd()
input_fonts_dir = os.path.join(root_dir, os.pardir, "resources", "FONTS")
output_root = os.path.join(root_dir, os.pardir, "output")
qr_dir = os.path.join(root_dir, os.pardir, "resources", "qr_codes")

if len(sys.argv) > 2:
    if sys.argv[2]:
        input_fonts_dir = sys.argv[2]
    if len(sys.argv) > 3:
        output_root = sys.argv[3]
    if len(sys.argv) > 4:
        qr_dir = sys.argv[4]

# output_dir = os.path.join(output_root, "output_form")
qr_output_dir = os.path.join(output_root, "output_qr")

if qr_output_dir not in glob.glob(os.path.join(output_root,"*")):
    os.mkdir(qr_output_dir)

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

# Every word should be annotated. Spaces removed
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
# background = Image.new('RGB', (1200,1200), (128, 128, 128))

# img_w = 128
# qr_img = Image.open(random.choice(glob.glob(qr_dir+"/*")))
# qr_img = Image.open("QR/qr1.png")

# res_img = qr_img.resize((img_w, img_w),resample=0)

# background.paste(res_img,(0,0))
# background.paste(res_img,(0,256))

# d = ImageDraw.Draw(background)
# d.text((0,128*3),"Hello Test Data", fill=(0, 0, 0))

# background.save(os.path.join(qr_dir,"tp.png"))


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

# Going through the page from top left, randomly selecting spacing and
# placing text on the image
num_of_images = 5
if len(sys.argv) > 1:
    num_of_images = int(sys.argv[1])
font_size_min, font_size_max = 10, 14
print("Saving " + str(num_of_images) + " QR images.")
for image_counter in tqdm(range(1, num_of_images + 1)):
    # yolo_txt_file = output_dir+"\\"+str(image_counter)+".txt"
    yolo_txt_file = os.path.join(qr_output_dir, str(image_counter) + "_qr.txt")
    f = open(yolo_txt_file, 'w')
    max_sizes = [720, 720, 720, 640, 512, 400]
    max_w, max_h = random.choice(max_sizes), random.choice(max_sizes)
    img = Image.new('RGB', (max_w, max_h),
                    color=(255, 255, 255))
    boundary = 10
    curr_pos = [0, 0]
    # x_offset, y_offset = random.randint(0, round(max_w*0.2)), random.randint(0, round(max_h*0.2))
    x_offset, y_offset = random.randint(
        0, 50), random.randint(0, 50)
    curr_pos[0] += x_offset
    curr_pos[1] += y_offset
    line_h = 0
    font_path = random.choice(glob.glob(input_fonts_dir + "/*/*.ttf"))
    font = ImageFont.truetype(
        font_path, random.randint(font_size_min, font_size_max))

    qr_size = 128
    qr_w, wr_h = qr_size, qr_size  # random.choice([256,300,300,128])
    qr_x = random.randint(0, max_w - qr_size)
    qr_y = random.randint(0, max_h - qr_size)

    # Clockwise notation
    qx1, qy1 = qr_x, qr_y
    qx2, qy2 = qr_x + qr_size, qr_y
    qx3, qy3 = qr_x + qr_size, qr_y + qr_size
    qx4, qy4 = qr_x, qr_y + qr_size

    qr_img = Image.open(random.choice(glob.glob(qr_dir + "/*.png")))
    # qr_img = Image.open("QR/qr_codes/qr1_copy.png")
    res_img = qr_img.resize((qr_w, wr_h), resample=0)
    img.paste(res_img, (qr_x, qr_y), res_img.convert('RGBA'))
    # img.save(os.path.join(qr_dir,"tp.png"))

    while(True):
        if(checkPosition(curr_pos, [(qx1, qy1), (qx2, qy2), (qx3, qy3), (qx4, qy4)])):
            # print("Collision",curr_pos)
            curr_pos[0] = qx2 + 10
            continue
        input_text = rstr.xeger(random.choice(sample_input_text))

        input_text_linewise = input_text.split("\n")
        font_w_list, font_h_list = [], []
        for line in input_text_linewise:
            font_w_list.append(font.getsize(line)[0])
            font_h_list.append(font.getsize(line)[1])
        font_w, font_h = max(font_w_list), sum(font_h_list)

        # font_path = random.choice(glob.glob(input_fonts_dir+"\\*\\*.ttf"))
        if(input_text.find("\n") != -1):
            font_h += 10 * input_text.count("\n")
        line_h = max(font_h, line_h)
        spacing = [0, 0]
        if max_w - font_w - boundary - curr_pos[0] > 0:
            # spacing = [random.randint(
            # 0, max_w-font_w - curr_pos[0])]  # , random.randint(0,
            # max_h-font_h - curr_pos[1])]
            if checkTextBox(curr_pos, font_w, font_h, [[qx1, qy1], [qx2, qy2], [qx3, qy3], [qx4, qy4]]):
                curr_pos[0] = qx2 + 10
                continue
            letter_w = font.getsize(' ')[0]
            spacing = random.choice(
                [[letter_w], [letter_w * 2], [letter_w], [letter_w * 2], [letter_w * 3]])
            curr_pos[0] += spacing[0]            # curr_pos[1] += spacing[1]
            d = ImageDraw.Draw(img)
            d.text((curr_pos[0], curr_pos[1]),
                   input_text, font=font, fill=(0, 0, 0),)
            x1 = curr_pos[0]
            y1 = curr_pos[1]
            x2 = curr_pos[0] + font_w
            y2 = curr_pos[1]
            x3 = curr_pos[0] + font_w
            y3 = curr_pos[1] + font_h
            x4 = curr_pos[0]
            y4 = curr_pos[1] + font_h
            class_ = 0
            # d.rectangle([(x1, y2), (x3, y3)], fill=None, outline=(255, 0, 0))
            llst_coords = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            yolo_coords = convert(
                img.size, [float(x1), float(x3), float(y1), float(y3)])
            print('%d %.4f %.4f %.4f %.4f' % (
                class_, yolo_coords[0], yolo_coords[1], yolo_coords[2], yolo_coords[3]), file=f)
            curr_pos[0] += font_w
            # curr_pos[1] += font_h

        else:
            curr_pos[0] = 0
            curr_pos[1] += random.choice([line_h, line_h * 2, line_h, line_h * 2,
                                          line_h, line_h * 2, line_h, line_h * 2, line_h, line_h * 2, line_h * 3])
            line_h = 0
            if(curr_pos[1] + font_h >= max_h - boundary):
                break
            else:
                continue

    img.save(os.path.join(qr_output_dir, str(image_counter) + "_qr.jpg"))
    f.close()
    # print("QR " + str(image_counter) + " saved.")
print("Saved " + str(num_of_images) + " QR images.")

# Using Matplotlib to check if a new randomly selected region coincides
# with any existing regions

# for image_counter in range(1, num_of_images+1):
#     text_regions = []
#     yolo_txt_file = output_dir+"\\"+str(image_counter)+".txt"
#     f = open(yolo_txt_file, 'w')
#     img = Image.new('RGB', (max_w, max_h),
#                     color=(255, 255, 255))
#     max_sizes = [512, 512, 512, 640, 320, 400]
#     max_w, max_h = random.choice(max_sizes), random.choice(max_sizes)

#     num_of_words = 0
#     for text_counter in range(random.randint(10, 25)):
#         input_text = random.choice(sample_input_text)
#         font_path = random.choice(glob.glob(input_fonts_dir+"\\*\\*.ttf"))
#         font_size_min, font_size_max = 10, 24
#         font = ImageFont.truetype(
#             font_path, random.randint(font_size_min, font_size_max))

#         # get linewise maximum wd and ht
#         input_text_linewise = input_text.split("\n")
#         font_w_list, font_h_list = [], []
#         for line in input_text_linewise:
#             font_w_list.append(font.getsize(line)[0])
#             font_h_list.append(font.getsize(line)[1])

#         font_w, font_h = max(font_w_list), sum(font_h_list)
#         font_random_x1, font_random_y1 = None, None
#         while(True):
#             while(True):
#                 if max_w > font_w and max_h > font_h:
#                     font_random_x1 = random.randint(0, (max_w - font_w))
#                     font_random_y1 = random.randint(0, (max_h - font_h))
#                     break
#                 else:
#                     font = ImageFont.truetype(
#                         font_path, random.randint(font_size_min, font_size_max))
#                     # get linewise maximum wd and ht
#                     input_text_linewise = input_text.split("\n")
#                     font_w_list, font_h_list = [], []
#                     for line in input_text_linewise:
#                         font_w_list.append(font.getsize(line)[0])
#                         font_h_list.append(font.getsize(line)[1])
#                     font_w, font_h = max(font_w_list), sum(font_h_list)

#             x1 = font_random_x1
#             y1 = font_random_y1
#             x2 = font_random_x1+font_w
#             y2 = font_random_y1
#             x3 = font_random_x1+font_w
#             y3 = font_random_y1+font_h
#             x4 = font_random_x1
#             y4 = font_random_y1+font_h

#             X, Y = np.mgrid[x1:x3, y1:y3]
#             larr_all_coords = np.vstack((X.ravel(), Y.ravel()))
#             llst_all_coords = list(zip(*larr_all_coords))
#             all_coords = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

#             if(len(text_regions) > 0):
#                 lbol_is_region_contains_point = True
#                 for region in text_regions:
#                     bbPath = mplPath.Path(np.array(region))
#                     for coord in llst_all_coords:
#                         lbol_is_region_contains_point = bbPath.contains_point(
#                             coord)
#                         if lbol_is_region_contains_point:
#                             break
#                     if lbol_is_region_contains_point:
#                         break
#                 if lbol_is_region_contains_point:
#                     continue

#             if (max_w-x1) > font_w and max_h-y1 > font_h:
#                 text_regions.append([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
#                 # print(text_regions)
#                 break
#             else:
#                 continue

#         d = ImageDraw.Draw(img)
#         # letter_offset = 0
#         # letter_w = font.getsize("k")[0]
#         # for letter in input_text:
#         #     spacing = 2  # random.randint(0, 10)
#         #     d.text((font_random_x1 + letter_w*letter_offset + letter_w * spacing, font_random_y1),
#         #            letter, font=font, fill=(0, 0, 0), spacing=3)
#         #     letter_offset += 1
#         d.text((font_random_x1, font_random_y1),
# input_text, font=font, fill=(0, 0, 0), spacing=random.randint(2, 10))

#         x1 = font_random_x1
#         y1 = font_random_y1
#         x2 = font_random_x1 + font_w
#         y2 = font_random_y1
#         x3 = font_random_x1 + font_w
#         y3 = font_random_y1 + font_h
#         x4 = font_random_x1
#         y4 = font_random_y1 + font_h
#         class_ = 0
#         # d.rectangle([(x1, y2), (x3, y3)], fill=None, outline=(255, 0, 0))
#         llst_coords = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
#         yolo_coords = convert(
#             img.size, [float(x1), float(x3), float(y1), float(y3)])
#         print('%d %.4f %.4f %.4f %.4f' % (
#             class_, yolo_coords[0], yolo_coords[1], yolo_coords[2], yolo_coords[3]), file=f)
#     # img.save(output_dir+"\\"+font_dir+"_"+str(text_counter)+"_" +
#     #          str(font_dir_counter)+"_"+str(font_counter)+".jpg")
#     img.save(output_dir+"\\"+str(image_counter)+".jpg")
#     f.close()
#     print("Image "+str(image_counter)+" saved.")
