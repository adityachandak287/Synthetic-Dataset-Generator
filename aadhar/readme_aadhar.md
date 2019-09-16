Synthetic Aadhaar Data Generation
=================================

### Run the following scripts to create different small regions found in Aadhaar Cards:
```cmd
python generate_aadhar_big.py
python generate_aadhar_electronic.py
python generate_aadhar_med.py
python generate_aadhar_small.py
```
### Run the following scripts to create synthetic Aadhaar Card dataset:
* [generate_aadhar.py](generate_aadhar.py) to generate Aadhar structured images with the following types of Aadhar placed on the image:
   * [Big](generate_aadhar_big.py) / [Electronic](generate_aadhar_electronic.py)
   * [Medium](generate_aadhar_med.py) (Bottom)
   * [Small](generate_aadhar_small.py) (Back)

* [generate_aadhar_types.py](generate_aadhar_types.py) to create images containing only one of the aadhar region types

* [generate_random_mixed.py](generate_random_mixed.py) to create images with randomly selected aadhar region types placed randomly

* [generate_back_patch.py](generate_back_patch.py) to create back aadhar region type placed randomly on an image

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
