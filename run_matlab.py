import os
import matlab.engine
import concurrent.futures
import subprocess
import sys
import re
import time

# Start a MATLAB engine
eng = matlab.engine.start_matlab()

# Define the path to the directory containing the images
image_dir = 'frames_original'

# Get a list of all the filenames in the image directory
filenames = os.listdir(image_dir)

# Remove duplicates by converting the list to a set
filenames = list(set(filenames))

def extract_number(filename):
    # Use regular expression to find the numerical part of the filename
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None

def process_image(filename):
    # Check that the file is a .jpg file
    number = extract_number(filename)
    if number is not None and filename.endswith('.jpg') and filename not in os.listdir("frames_output") and number % 24 == int(sys.argv[1]):
        # Call the MATLAB function and pass the filename
        result = eng.expand(filename, nargout=0)
        print(f"{number} just processed an image")

# Use a ThreadPoolExecutor to run the expand function in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_image, filenames)
    
print("Finished images.")

