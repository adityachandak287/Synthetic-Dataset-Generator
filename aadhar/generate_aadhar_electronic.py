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
input_fonts_dir = os.path.join(root_dir,os.pardir,"resources","FONTS")
fonts_dir_regular = os.listdir(input_fonts_dir)
qr_dir = root_dir #os.path.join(root_dir, "aadhar")
aadhar_output_dir = os.path.join(root_dir,"output","electronic")

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

file_suffix = "_aadhar_electronic"

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
font_size_min, font_size_max = 64,64
for image_counter in range(1, num_of_images+1):
    # yolo_txt_file = output_dir+"\\"+str(image_counter)+".txt"
    yolo_txt_file = os.path.join(aadhar_output_dir,str(image_counter)+file_suffix+".txt")
    f = open(yolo_txt_file, 'w')
    # max_sizes = [720, 720, 720, 640, 512, 400]
    
    font_path = "Calibri.ttf"
    font = ImageFont.truetype(font_path, random.randint(font_size_min, font_size_max))

    aadhar_num = rstr.xeger(random.choice(sample_input_aadhar))
    font_w, font_h = font.getsize(aadhar_num)[0],font.getsize(aadhar_num)[1] 

    max_w = font_w
    max_h = round(font_w* 0.8)#random.choice(max_sizes), random.choice(max_sizes)
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
    

    qr_size = round(max_h*0.78) #random.choice([256,300,300,128])
    qr_x = round(max_w/2 - qr_size/2) #random.randint(0,max_w - qr_size)
    qr_y = round(max_h - qr_size)#random.randint(0,max_h - qr_size)
    
    # Clockwise notation
    qx1, qy1 = qr_x, qr_y
    qx2, qy2 = qr_x+qr_size, qr_y
    qx3, qy3 = qr_x+qr_size, qr_y+qr_size
    qx4, qy4 = qr_x, qr_y+qr_size

    # QR Code
    
    qr_img = Image.open(random.choice(glob.glob(qr_dir+"/qr_codes/*.png")))
    # qr_img = Image.open("QR/qr_codes/qr1_copy.png")
    res_img = qr_img.resize((qr_size, qr_size),resample=0)
    img.paste(res_img,(qr_x,qr_y),res_img.convert('RGBA'))

    curr_pos = [qr_x,qr_y]
    annotate(curr_pos,[qr_size,qr_size],4,f)
    # img.save(os.path.join(qr_dir,"tp.png"))

    
    d = ImageDraw.Draw(img)
    # num_x, num_y = random.randint(20,qr_x-font_w+40),random.randint(max_h-(font_h*3),max_h-(font_h*2))
   
    num_w, num_h = font.getsize(aadhar_num)[0],font.getsize(aadhar_num)[1]
    num_x, num_y = 0,0
    d.text((num_x, num_y), aadhar_num, font=font, fill=(0, 0, 0))
    # d.rectangle([(num_x, num_y), (num_x+font_w, num_y+font_h)], fill=None, outline=(255, 0, 0))
    annotate([num_x, num_y],[font_w, font_h],2,f)

    # random_text = rstr.xeger(r'[A-Z a-z/0-9]{18,24}:')

    # random_w, random_h = font.getsize(random_text)[0],font.getsize(random_text)[1]

    # random_x, random_y = max_w/2-random_w/2, random.randint(qr_y+qr_size,num_y-random_h)

    # d.text((random_x, random_y),random_text, font=font, fill=(0,0,0))

    
    # d.rectangle([(x1, y2), (x3, y3)], fill=None, outline=(255, 0, 0))
    # noise_size = 14
    # font = ImageFont.truetype(font_path,noise_size)
    # for noise_counter in range(random.randint(1,5)):
    #     noise_text = rstr.xeger(r'[A_Za-z0-9]{4,15}')
    #     noise_w, noise_h = font.getsize(noise_text)[0],font.getsize(noise_text)[1]
    #     if qr_x-noise_w > 0 and num_y-noise_h -20> 0:
    #         n_x, n_y = random.randint(0,qr_x-noise_w), random.randint(0,num_y-noise_h-20)
    #         if qr_x-noise_w-n_x >= 0 and num_y-noise_h-n_y >= 0:
    #             d.text((n_x,n_y),noise_text,font=font,fill = (0,0,0))
    #             # print(str(noise_counter) + " noise")
    #         # else:
    #         #     print(str(noise_text)+" skipped "+str(qr_y)+" "+str(noise_h))
    #     # else:
    #     #     print("outer skipped")# "+qr_x+" "+noise_w)

    img.save(os.path.join(aadhar_output_dir,str(image_counter)+file_suffix+".jpg"))
    f.close()
    print("Aadhar "+str(image_counter)+" is saved.")
    


    # while(True):
    #     if(checkPosition(curr_pos,[(qx1, qy1),(qx2, qy2),(qx3, qy3),(qx4, qy4)])):
    #         print("Collision",curr_pos)
    #         curr_pos[0] = qx2 + 10
    #         continue
    #     input_text = rstr.xeger(random.choice(sample_input_text))

    #     input_text_linewise = input_text.split("\n")
    #     font_w_list, font_h_list = [], []
    #     for line in input_text_linewise:
    #         font_w_list.append(font.getsize(line)[0])
    #         font_h_list.append(font.getsize(line)[1])
    #     font_w, font_h = max(font_w_list), sum(font_h_list)    

    #     # font_path = random.choice(glob.glob(input_fonts_dir+"\\*\\*.ttf"))
    #     if(input_text.find("\n") != -1):
    #         font_h += 10 * input_text.count("\n")
    #     line_h = max(font_h, line_h)
    #     spacing = [0, 0]
    #     if max_w-font_w - boundary - curr_pos[0] > 0:
    #         # spacing = [random.randint(
    #         #     0, max_w-font_w - curr_pos[0])]  # , random.randint(0, max_h-font_h - curr_pos[1])]
    #         if checkTextBox(curr_pos,font_w,font_h,[[qx1, qy1],[qx2, qy2],[qx3, qy3],[qx4, qy4]]):
    #             curr_pos[0] = qx2 + 10
    #             continue
    #         letter_w = font.getsize(' ')[0]
    #         spacing = random.choice([[letter_w],[letter_w*2],[letter_w],[letter_w*2],[letter_w*3]])
    #         curr_pos[0] += spacing[0]            # curr_pos[1] += spacing[1]
    #         d = ImageDraw.Draw(img)
    #         d.text((curr_pos[0], curr_pos[1]),
    #                input_text, font=font, fill=(0, 0, 0),)
    #         x1 = curr_pos[0]
    #         y1 = curr_pos[1]
    #         x2 = curr_pos[0] + font_w
    #         y2 = curr_pos[1]
    #         x3 = curr_pos[0] + font_w
    #         y3 = curr_pos[1] + font_h
    #         x4 = curr_pos[0]
    #         y4 = curr_pos[1] + font_h
    #         class_ = 0
    #         # d.rectangle([(x1, y2), (x3, y3)], fill=None, outline=(255, 0, 0))
    #         llst_coords = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    #         yolo_coords = convert(
    #             img.size, [float(x1), float(x3), float(y1), float(y3)])
    #         print('%d %.4f %.4f %.4f %.4f' % (
    #             class_, yolo_coords[0], yolo_coords[1], yolo_coords[2], yolo_coords[3]), file=f)
    #         curr_pos[0] += font_w
    #         # curr_pos[1] += font_h

    #     else:
    #         curr_pos[0] = 0
    #         curr_pos[1] += random.choice([line_h,line_h*2,line_h,line_h*2,line_h,line_h*2,line_h,line_h*2,line_h,line_h*2,line_h*3])
    #         line_h = 0
    #         if(curr_pos[1] + font_h >= max_h-boundary):
    #             break
    #         else:
    #             continue

    # img.save(os.path.join(qr_output_dir,str(image_counter)+"_qr.jpg"))
    # f.close()
    # print("QR "+str(image_counter)+" saved.")


# Using Matplotlib to check if a new randomly selected region coincides with any existing regions

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
#                input_text, font=font, fill=(0, 0, 0), spacing=random.randint(2, 10))

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
