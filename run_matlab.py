import os
import sys
import re
import concurrent.futures
import matlab.engine

# Start the MATLAB engine
eng = matlab.engine.start_matlab()

IMAGE_DIR = 'frames_original'
OUTPUT_DIR = 'frames_output'

# Ensure frames_output directory exists
if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# Get list of filenames (remove duplicates by converting to a set)
filenames = os.listdir(IMAGE_DIR)
filenames = list(set(filenames))


def extract_number(filename):
    """
    Extract the numerical part of a filename using regex.
    Returns an integer or None if not found.
    """
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else None


def process_image(filename, remainder):
    """
    Process a single image by calling the MATLAB 'expand' function.
    Only process the file if it ends with '.jpg', is not already in OUTPUT_DIR,
    and its frame number matches the remainder criteria.
    """
    number = extract_number(filename)
    if (
        number is not None
        and filename.endswith('.jpg')
        and filename not in os.listdir(OUTPUT_DIR)
        and number % 16 == remainder
    ):
        # Call the MATLAB expand function
        eng.expand(filename, nargout=0)
        processed_count = len(os.listdir(OUTPUT_DIR))
        total_count = len(os.listdir(IMAGE_DIR))
        print(f"Processed image {filename} (frame {number})")
        print(f"{processed_count} / {total_count} images processed")


if __name__ == "__main__":
    # Expecting an argument that indicates the remainder (0..15)
    if len(sys.argv) < 2:
        print("Usage: python3 run_matlab.py <remainder>")
        sys.exit(1)

    remainder_value = int(sys.argv[1])

    # Process images in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_image, f, remainder_value)
            for f in filenames
        ]

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)
    print("Finished processing images.")
