# Synthetic Image Data Generation CLI
This tool generates images for training deep learning models. Annotations are created in YOLO format.

[Readme](aadhar/readme_aadhar.md) for [Aadhar Data Generation Tool](aadhar).
## Command Line Arguments:
* [generate_text.py](scripts/generate_text.py)
   ```cmd
   python generate_text.py [num_of_images] [FONTS directory] [Output root directory]
   ```

* [generate_form.py](scripts/generate_form.py)
   ```cmd
   python generate_form.py [num_of_images] [FONTS directory] [Output root directory]
   ```
* [generate_qr.py](scripts/generate_qr.py)
   ```cmd
   python generate_qr.py [num_of_images] [FONTS directory] [Output root directory] [Directory containing QR code PNG images]
   ```
* [orientation_dataset.py](scripts/orientation_dataset.py)

   Default output_root
 
   ```cmd
   python orientation_dataset.py [num_of_images] [Directory containing images to be rotated]
   ```

   Specify output_root
   ```cmd
   python orientation_dataset.py [num_of_images] [Output root directory] [Directory containing images to be rotated]
   ```


## Common variables:
* `sample_input_text`: List of regular expressions to choose from while generating random text
	
* `num_of_images`: Number of images to be generated. (Default 5 if not specified by command line arguments)
	
* `font_size_min, font_size_max`: Minimum and Maximum font size to randomly choose from
	
* `max_sizes`: List of maximum dimensions of each image. Width and height will be randomly chosen from this list
* `max_w, max_h`: Width and Height of an image being generated	

   Example:

   ```python
   max_w, max_h = 1050, 1485 #To set fixed width and height
   
   max_w, max_h = random.choice(max_sizes), random.choice(max_sizes) #To choose width and height randomly from max_sizes list)
   ```

* `font_w, font_h`: width and height of box bounding the text generated

* `file_suffix`: File name suffix to be added to each image being saved

* `boundary`: Boundary to be maintained around the borders of the image

* `font_path`: Path to font file (Randomly chosen from input_fonts_dir)


## Script Specific Variables:
* [generate_text.py](scripts/generate_text.py) and [generate_form.py](scripts/generate_form.py):
   
   `line_h`: Line height. (Maximum height of text placed in that line)
* [orientation_dataset.py](scripts/orientation_dataset.py):
 
   `rotate_angle`: Angle to rotate the image with
_____

# Synthetic Aadhaar Data Generation

### Run the following scripts to create different small regions found in Aadhaar Cards:
```cmd
python generate_aadhar_big.py
python generate_aadhar_electronic.py
python generate_aadhar_med.py
python generate_aadhar_small.py
```
### Run the following scripts to create synthetic Aadhaar Card dataset:
* [generate_aadhar.py](aadhar/generate_aadhar.py) to generate Aadhar structured images with the following types of Aadhar placed on the image:
   * [Big](aadhar/generate_aadhar_big.py) / [Electronic](generate_aadhar_electronic.py)
   * [Medium](aadhar/generate_aadhar_med.py) (Bottom)
   * [Small](aadhar/generate_aadhar_small.py) (Back)

* [generate_aadhar_types.py](aadhar/generate_aadhar_types.py) to create images containing only one of the aadhar region types

* [generate_random_mixed.py](aadhar/generate_random_mixed.py) to create images with randomly selected aadhar region types placed randomly

* [generate_back_patch.py](aadhar/generate_back_patch.py) to create back aadhar region type placed randomly on an image

### To toggle random text being placed on the image comment out the following part from the scripts:
```python
for cell_counter in range(random.randint(15,25)):
    while(True):
        font_random_path = calibri_font_path
        font_random = ImageFont.truetype(font_random_path, random.randint(16,32))

        input_text = rstr.xeger(r'[A-Za-z0-9]{4,15}')
        rand_w, rand_h = font_random.getsize(input_text)[0], font_random.getsize(input_text)[1]
        rand_x1 = random.randint(boundary, max_w - boundary - rand_w)
        rand_y1 = random.randint(boundary, max_h - boundary - rand_h)

        if validatePosition([rand_x1,rand_y1],[rand_w, rand_h],regions):
            regions.append([(rand_x1,rand_y1),(rand_x1+rand_w,rand_y1),(x1+rand_w,y1+rand_h),(x1,y1+rand_h)])
            # img.paste(aadhar, (rand_x1,rand_y1), aadhar.convert('RGBA'))
            d = ImageDraw.Draw(img)
            d.text((rand_x1, rand_y1), input_text, font = font_random, fill = (0,0,0))
            break
        else:
            continue
   ```

