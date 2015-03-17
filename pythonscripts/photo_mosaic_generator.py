#!/usr/bin/env python
# photo mosaic generator

import sys
import os.path
import Image
import glob
from pymos.core import build_mosaic


filelist= glob.glob("/home/ferran/DCIM/Camera/*.jpg")
thumbnail_size = (100, 100)

# Loop through all provided arguments
for i in range(1, len(filelist)):
    try:
        # Attempt to open an image file
        filepath = filelist[i]
        image = Image.open(filepath)
    except IOError, e:
        # Report error, and then skip to the next argument
        print "Problem opening", filepath, ":", e
        continue

    # Resize the image
    image = image.resize(thumbnail_size, Image.ANTIALIAS)
    
    # Split our original filename into name and extension
    (name, extension) = os.path.splitext(filepath)
    
    # Save the thumbnail as "(original_name)_thumb.jpg"
    image.save('/home/ferran/mosaic/'+name+'.jpg')

build_mosaic(
	input_path="orignal_image.jpg",
	output_path="output_mosaic.png",
	collection_path="/home/ferran/mosaic/",
	zoom=4,
	thumb_size=50,
	fuzz=20,
	new_colormap=False
)
