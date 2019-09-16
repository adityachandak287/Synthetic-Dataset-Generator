# Synthetic Data Generation CLI
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
