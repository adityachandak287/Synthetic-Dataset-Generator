import os
import glob
import sys

root_dir = os.getcwd()
resources_dir = os.path.join(root_dir, "resources")
scripts_dir = os.path.join(root_dir, "scripts")

scripts_info = [{
    "generate_text.py": "Generate images with text placed randomly with random fonts. YOLO format annotation files created."
},
    {
    "generate_form.py": "Generate images with text placed in a structured form-like format. YOLO format annotation files created."
},
    {
    "generate_qr.py": "Generate images with text placed in a structured form-like format with QR codes randomly placed. Can be used to train model to ignore QR codes. YOLO format annotation files created for text, not QR code."
},
    {
    "orientation_dataset.py": "Accepts images and generates images with 1 or 2 images rotated randomly. YOLO format annotation files created."
}, ]

while(True):
    print("Choose from the following:")
    index = 0
    for script in scripts_info:
        for s_name, s_info in script.items():
            index += 1
            print(str(index) + ". \033[1;31;93m" + s_name + "\033[0m")
            print(s_info)
    print(str(5) + ". \033[1;31;93mExit\033[0m")
    choice = int(input("Enter choice - "))

    num_of_images = int(input("\033[1;31;95mNumber of images - \033[0m"))

    default = input("Use default paths? [y/n] - ").lower()

    if default == "n":
	    if choice == 5:
	    	break
	    fonts_dir = ""
	    qr_dir = ""
	    image_input = ""

	    

	    if choice in [1, 2, 3]:
	    	fonts_dir = input("\033[1;31;95mFonts directory - \033[0m")
	    output_root = input("\033[1;31;95mRoot output directory - \033[0m")
	    if choice == 3:
	    	qr_dir = input("\033[1;31;95mQR Codes directory - \033[0m")
	    if choice == 4:
	    	image_input = input("\033[1;31;95mImage Input directory - \033[0m")

	    script_name = list(scripts_info[choice - 1].keys())[0]
	    print("*"*10)
	    # arguments = " ".join([num_of_images, fonts_dir, output_root, qr_dir, image_input])
	    os.chdir("scripts")
	    os.system("python %s %s %s %s %s %s" % (script_name, str(num_of_images),fonts_dir ,output_root, qr_dir, image_input))
	    os.chdir(os.pardir)
    elif default == "y":
    	image_input = ""
    	if choice == 4:
    		image_input = input("\033[1;31;95mImage Input directory - \033[0m")	

    	script_name = list(scripts_info[choice - 1].keys())[0]
    	print("*"*10)
    	# arguments = " ".join([num_of_images, image_input])
    	os.chdir("scripts")
    	os.system("python %s %s %s" % (script_name, str(num_of_images), image_input))
    	os.chdir(os.pardir)
	# else:
	# 	print("Invalid input.")
	
		
