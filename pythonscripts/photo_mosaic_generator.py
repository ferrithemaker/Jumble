#!/usr/bin/env python
# photo mosaic generator

import sys
import os.path
import Image
import glob
from pymos.core import build_mosaic


filelist= glob.glob("/home/ferran/nexus5-last/DCIM/Camera/*.jpg")
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
    (file_path, extension) = os.path.splitext(filepath)
    file_path_split=file_path.split('/')
    print 'Converting /home/ferran/mosaic/'+file_path_split[len(file_path_split)-1]+'.jpg'
    
    # Save the thumbnail as "(original_name)_thumb.jpg"
    image.save('/home/ferran/mosaic/'+file_path_split[len(file_path_split)-1]+'.jpg')
print "Building photo mosaic..."
build_mosaic(
	input_path="rpi.jpg",
	output_path="rpi_mosaic.png",
	collection_path="/home/ferran/mosaic/",
	zoom=4,
	thumb_size=50,
	fuzz=20,
	new_colormap=False
)
