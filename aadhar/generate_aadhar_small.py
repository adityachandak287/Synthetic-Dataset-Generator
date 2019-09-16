'''
Created on 17-May-2019

@author: cerelabs
'''
from __future__ import division, print_function, absolute_import
from PIL import Image, ImageDraw, ImageFont
import glob
import os
import random
import matplotlib.path as mplPath
import numpy as np
import rstr
from shapely.geometry import Polygon, Point

root_dir = os.getcwd()
# input_fonts_dir = os.path.join(root_dir, "FONTS")
input_fonts_dir = os.path.join(root_dir,os.pardir,"resources","FONTS")
# output_dir = os.path.join(root_dir, "output_form")
fonts_dir_regular = os.listdir(input_fonts_dir)
qr_dir = root_dir # os.path.join(root_dir, "aadhar")
aadhar_output_dir = os.path.join(root_dir,"output","small")
small_dir = os.path.join(root_dir,"small")

def convert(size, box):
    # size list[widht, height], box list[x1,x2,y1,y2]
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return [x, y, w, h]

def denormalize(size, box):
    # size list[width, height] of image, box list[x,y,w,h] from LabelImg
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    
    x = x*size[0]
    y = y*size[1]
    w = w*size[0]
    h = h*size[1]


    x1 = (2*x-w)/2.0
    y1 = (2*y-h)/2.0
    x3 = (2*x+w)/2.0
    y3 = (2*y+h)/2.0

    x4 = x1
    x2 = x3
    y4 = y3
    y2 = y1
    
    return [x1,y1,x2,y2,x3,y3,x4,y4]

sample_input_text = [r'[A-Za-z0-9!@#$%^&*()]{4,25}[A-Za-z0-9!@#$%^&*()]{4,15}',
                     r'[A-Za-z0-9]{1,20}[,.]{1}',
                     r'[A-Za-z0-9]{1,20}[,.]{1}',
                     r'[0-9]{1,4}[A-Za-z]{2,20}',
                     r'[A-Za-z]{1,3}',
                     r'\d{2}/\d{2}/\d{4}',
                     r'\d{2}/\d{2}/\d{4}',
                     r'[A-Z0-9]{10}',
                     r'[A-Z]{1,12}',
                     r'[A-Z]{4,16}[A-Z]{4,10}',
                     r'[A-Z]{1}[a-z]{6,12}[A-Z]{1}[a-z]{6,12}[A-Z]{1}[a-z]{6,12}',
                     r'[A-Z]{1}[a-z]{6,12}',
                     r'\d{1,2}',
                     r'\d{1,2}',
                     r'\d{1,2}',
                     r'\d{2,4}\d{4}\d{1,4}',
                     r'[A-Za-z]{15,35}'
                     ]       

sample_input_aadhar = [r'\d{4} \d{4} \d{4}']   

bottom_text = [r'[A-Za-z]{4,10}[ ]{1,3}[A-Za-z]{4,10}[ ]{1,3}[A-Za-z]{4,10}'] 

file_suffix = "_aadhar_small"

class_code = {
    "num_small": 0,
    "num_med":1,
    "num_large": 2,
    "qr": 4,
    "big_box": 6,
    "small_box": 7
}

sizes = {   
        "qrsmall":  [320,200],
        "qrbig": [320,240],
        "numsmall":[320, 30]
        }   

def annotate(pos, box_size, class_num, file_obj):
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
    yolo_coords = convert(
        img.size, [float(x1), float(x3), float(y1), float(y3)])
    print('%d %.4f %.4f %.4f %.4f' % (
        class_, yolo_coords[0], yolo_coords[1], yolo_coords[2], yolo_coords[3]), file=file_obj)


def checkPosition(curr, qr_pos):
    position = Point(curr[0],curr[1])
    qrBox = Polygon(qr_pos)
    if qrBox.intersects(position):
        return True
    else:
        return False

def checkTextBox(curr,text_w,text_h, qr_pos):
    textBox = Polygon([tuple(curr),(curr[0]+text_w,curr[1]),(curr[0]+text_w,curr[1]+text_h),(curr[0],curr[1]+text_h)])
    qrBox = Polygon(qr_pos)
    return textBox.intersects(qrBox)

# Going through the page from top left, randomly selecting spacing and placing text on the image
num_of_images = 5
font_size_min, font_size_max = 18,18
for image_counter in range(1, num_of_images+1):
    # yolo_txt_file = output_dir+"\\"+str(image_counter)+".txt"
    yolo_txt_file = os.path.join(aadhar_output_dir,str(image_counter)+file_suffix+".txt")
    f = open(yolo_txt_file, 'w')
    max_sizes = [720, 720, 720, 640, 512, 400]
    max_w, max_h = 320, 64#random.choice(max_sizes), random.choice(max_sizes)
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
    # font_path = random.choice(glob.glob(input_fonts_dir+"/*/*.ttf"))
    font_path = os.path.join(input_fonts_dir, "Calibri", "Calibri.ttf")#"/home/cerelabs/Workarea/Aditya/DatasetCreation/FONTS/Calibri/Calibri.ttf"
    # font_path = random.choice(glob.glob(input_fonts_dir+"Kruti Dev/*.ttf"))
    # font_path = "home/cerelabs/Workarea/Aditya/DatasetCreation/FONTS/Kruti Dev/Kruti_Dev_010.ttf"

    
    font = ImageFont.truetype(font_path, random.randint(font_size_min, font_size_max))
    
    # d.rectangle([(x1, y2), (x3, y3)], fill=None, outline=(255, 0, 0))
    aadhar_num = rstr.xeger(sample_input_aadhar[0])
    num_w, num_h = font.getsize(aadhar_num)[0],font.getsize(aadhar_num)[1]

    d = ImageDraw.Draw(img)
    num_x, num_y = max_w/2 - num_w/2, max_h/4 - num_h/2
    d.text((num_x, num_y), aadhar_num, font=font, fill=(0, 0, 0))
    
    # num_w, num_h = font.getsize(aadhar_num)

    annotate([num_x, num_y],[num_w, num_h],0,f)

    d.line([(0,max_h/2),(max_w, max_h/2)],fill=(0,0,0),width=2)

    if random.random() > 0.5:
        qr_img = Image.open(random.choice(glob.glob(small_dir+"/*.jpg")))
        # qr_img = Image.open("QR/qr_codes/qr1_copy.png")
        res_img = qr_img.resize((max_w, round(max_h/2)-10),resample=0)
        img.paste(res_img,(0,round(max_h/2) + 5),res_img.convert('RGBA'))
    else:
        bottom_font = ImageFont.truetype(font_path, random.randint(font_size_min, font_size_max))
        random_text = rstr.xeger(random.choice(bottom_text))
        bottom_x, bottom_y = round(max_w/2 - bottom_font.getsize(random_text)[0]/2), round(0.75*max_h - bottom_font.getsize(random_text)[1]/2)
        d.text((bottom_x,bottom_y),random_text, font = bottom_font, fill = (0,0,0))


    img.save(os.path.join(aadhar_output_dir,str(image_counter)+file_suffix+".jpg"))
    f.close()
    print("Aadhar "+str(image_counter)+" is saved.")
    


    