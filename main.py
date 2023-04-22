import numpy as np

from PIL import Image


def rgb_to_yiq(image_path):
    # Open image
    image = Image.open(image_path)

    # Convert image to numpy array
    image_array = np.asarray(image, np.float64)

    height, width, channel = image_array.shape

    # Calculate YIQ values
    for ly in range(0, height):
        for lx in range(0, width):

            r = image_array.item(ly, lx, 0)
            g = image_array.item(ly, lx, 1)
            b = image_array.item(ly, lx, 2)

            y = (0.299*r) + (0.587*g) + (0.114*b)

            i = (0.596*r) - (0.274*g) - (0.322*b)

            q = (0.211*r) - (0.523*g) + (0.312*b)

            image_array.itemset((ly, lx, 0), y)
            image_array.itemset((ly, lx, 1), i)
            image_array.itemset((ly, lx, 2), q)

    return image_array


def yiq_to_rgb(image_array):
    height, width, channel = image_array.shape

    # Calculate RGB values
    for ly in range(0, height):
        for lx in range(0, width):

            y = image_array.item(ly, lx, 0)
            i = image_array.item(ly, lx, 1)
            q = image_array.item(ly, lx, 2)

            r = y + (0.956*i) + (0.621*q)

            g = y - (0.272*i) - (0.647*q)

            b = y - (1.105*i) + (1.702*q)

            image_array.itemset((ly, lx, 0), r)
            image_array.itemset((ly, lx, 1), g)
            image_array.itemset((ly, lx, 2), b)

    rgb_image = Image.fromarray(np.uint8(image_array))
    return rgb_image

def negative_rgb(image_path): 
   
    # Convert image to numpy array
    image = np.asarray(Image.open(image_path))
    image_array = image.copy()

    height, width, channel = image_array.shape

    # Calculate YIQ values
    for ly in range(0, height):
        for lx in range(0, width):

            r = image_array.item(ly, lx, 0)
            g = image_array.item(ly, lx, 1)
            b = image_array.item(ly, lx, 2)

            Nr = 255 - r

            Ng = 255 - g

            Nb = 255 - b

            image_array.itemset((ly, lx, 0), Nr)
            image_array.itemset((ly, lx, 1), Ng)
            image_array.itemset((ly, lx, 2), Nb)
    
    rgb_image = Image.fromarray(image_array)
    return rgb_image

def negative_yiq(image_path): 
    # Open image
    image = Image.open(image_path)

    # Convert image to numpy array
    image_array = np.asarray(image, np.float64)

    height, width, channel = image_array.shape

    # Calculate YIQ values
    for ly in range(0, height):
        for lx in range(0, width):

            r = image_array.item(ly, lx, 0)
            g = image_array.item(ly, lx, 1)
            b = image_array.item(ly, lx, 2)

            y = (0.299*r) + (0.587*g) + (0.114*b)
            y = 255 - y

            i = (0.596*r) - (0.274*g) - (0.322*b)

            q = (0.211*r) - (0.523*g) + (0.312*b)

            image_array.itemset((ly, lx, 0), y)
            image_array.itemset((ly, lx, 1), i)
            image_array.itemset((ly, lx, 2), q)

    return image_array

def median_filter(image_path, filter_dimensions):
    #Image openning
    image = Image.open(image_path)

    image = image.resize((1500, 1000))    # Apply a resize for bigger images

    # Image convert to Array
    img_array = np.asarray(image, np.float64)

    # Image to apply the result
    filtered_image = Image.new(image.mode, image.size)

    # Image and filter dimensions
    height, width, channel = img_array.shape
    filter_half_width = filter_dimensions[1] // 2
    filter_half_height = filter_dimensions[0] // 2

    # Go through all the pixels of the image
    for y in range(height):
        for x in range(width):
            # Create a list of neighbors for each color
            r = []
            g = []
            b = []
            for i in range(-filter_half_height, filter_half_height+1): # Go through height neighbors
                for j in range(-filter_half_width, filter_half_width+1): # Go through widhth neighbors
                    # Get coordinates
                    widthNeighbor = x + j
                    heightNeighbor = y + i

                    # Make zero extension if a neighbor has a negative value or if it's bigger than the image
                    if widthNeighbor < 0 or widthNeighbor >= width or heightNeighbor < 0 or heightNeighbor >= height:
                        r.append(0)
                        g.append(0)
                        b.append(0)
                    # If the pixel is in the image, add the pixel value to the list of neighbors
                    else:
                        r.append(img_array[heightNeighbor, widthNeighbor, 0])
                        g.append(img_array[heightNeighbor, widthNeighbor, 1])
                        b.append(img_array[heightNeighbor, widthNeighbor, 2])

            # Calculate the median for each color
            median_value_r = int(np.median(r))
            median_value_g = int(np.median(g))
            median_value_b = int(np.median(b))

            # Aply the new values to the pixel
            filtered_image.putpixel((x, y), (median_value_r, median_value_g, median_value_b))

    return filtered_image


image_file = "DancingInWater.jpg"

# Transform RGB to YIQ
yiq_array = rgb_to_yiq(image_file)

# Convert YIQ to RGB
rgb_image = yiq_to_rgb(yiq_array)

rgb_image.save('rgb_' + image_file)

# Convert Negative RGB
negative_image_rgb = negative_rgb(image_file)

negative_image_rgb.save('negative_rgb_'+ image_file)

# Convert Negative YIQ

negative_image_yiq_array = negative_yiq(image_file)
negative_y = yiq_to_rgb(negative_image_yiq_array)


negative_y.save('negative_yiq_'+ image_file)


# Apply median filter

m = 3
n = 3
filtered_image = median_filter(image_file, (m, n))
filtered_image.save('median_filter_' + image_file)

