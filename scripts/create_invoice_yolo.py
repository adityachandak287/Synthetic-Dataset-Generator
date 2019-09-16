import os
import glob
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from tqdm import tqdm

csv_path = "/home/cerelabs-014/workarea/Aditya/InvoiceDetection/invoice_list.csv"
image_dir = os.path.join(os.getcwd(), "images")

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

csv = pd.read_csv(csv_path)

for index, row in tqdm(csv.iterrows()):
	img_path = os.path.join(image_dir, row["File"])
	img = Image.open(img_path)
	with open(img_path[:-4] + ".txt", "w") as f:
		annotate((0,0), img.size, img.size, row["Class"], f)

	if index == 2:
		break


# print(csv)
