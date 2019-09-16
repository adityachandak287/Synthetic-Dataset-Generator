'''
Created by Aditya Chandak, 2019
'''
from shapely.geometry.polygon import Polygon
from PIL import Image, ImageDraw, ImageFont
import random
import os
import glob
import math
from tqdm import tqdm
import sys

'''
Arguments: 
num_of_images image_dir
num_of_images output_root image_dir
'''

root_dir = os.getcwd()
image_dir = os.path.join(root_dir, os.pardir, "resources", "aadhar_orientation_input")
output_root = os.path.join(root_dir, os.pardir, "output")

if len(sys.argv) > 2:

    if len(sys.argv) == 3:
        image_dir = sys.argv[2]
    else:
        if sys.argv[2]:
            output_root = sys.argv[2]
        if len(sys.argv) > 3:
            image_dir = sys.argv[3]

output_dir = os.path.join(output_root, "output_orientation")

if output_dir not in glob.glob(os.path.join(output_root, "*")):
    os.mkdir(output_dir)

file_suffix = "_document_rotated"


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
    yolo_coords = convert(
        max_size, [float(x1), float(x3), float(y1), float(y3)])
    print('%d %.4f %.4f %.4f %.4f' % (class_, yolo_coords[0], yolo_coords[
          1], yolo_coords[2], yolo_coords[3]), file=file_obj)


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

# def getOrientationClass(rotate_angle):
#     angle = (rotate_angle + 90) % 360
#     lower = math.floor(angle / 90.0)
#     upper = math.ceil(angle / 90.0)
#     div = angle / 90.0
#     if abs(div - lower) <= abs(div - upper):
#         return lower + 1
#     else:
#         return upper + 1
#     print(angle)


def getOrientationClass(rotate_angle):
    angle = (rotate_angle + 90) % 360
    if angle > 315 or angle <= 45:
        return 1
    elif angle > 45 and angle <= 135:
        return 2
    elif angle > 135 and angle <= 225:
        return 3
    else:
        return 4


image_list = glob.glob(image_dir + "/*.jpg")

max_w, max_h = 840, 1188
num_of_images = 5
if len(sys.argv) > 1:
    num_of_images = int(sys.argv[1])
boundary = 10
print("Saving " + str(num_of_images) + " oriented images.")
for image_counter in tqdm(range(num_of_images)):
    bg = Image.new('RGB', (max_w, max_h), color=(255, 255, 255))
    image_regions = []
    file_name = str(image_counter + 1) + file_suffix
    f = open(os.path.join(output_dir, file_name + ".txt"), "w")
    image_count = 0
    max_images = random.choice([1, 2])
    while(image_count < max_images):
        num_of_attempts = 0
        while(num_of_attempts < 5):
            image_path = random.choice(image_list)
            img = Image.open(image_path)

            rotate_angle = None
            if random.random() > 0.5:
                rotate_angle = round(random.random() * random.randint(0, 360))
            else:
                rotate_angle = random.choice([0, 90, 180, 270])
            img = img.convert('RGBA')
            img_rot = img.rotate(rotate_angle, expand=1)

            [w_1, h_1] = img_rot.size
            if max_w - boundary - w_1 > 0 and max_h - boundary - h_1 > 0:
                x1, y1 = random.randint(
                    0, max_w - boundary - w_1), random.randint(0, max_h - boundary - h_1)
                if validatePosition([x1, y1], img_rot.size, image_regions):
                    bg.paste(img_rot, (x1, y1), img_rot.convert('RGBA'))
                    image_regions.append(
                        [[x1, y1], [x1 + w_1, y1], [x1 + w_1, y1 + h_1], [x1, y1 + h_1]])
                    class_ = getOrientationClass(rotate_angle)
                    annotate([x1, y1], img_rot.size, [max_w, max_h], class_, f)

                    image_count += 1
                    break
            num_of_attempts += 1
    bg.save(os.path.join(output_dir, file_name + ".jpg"))
    # print(file_name)
print("Saved " + str(num_of_images) + " oriented images.")
