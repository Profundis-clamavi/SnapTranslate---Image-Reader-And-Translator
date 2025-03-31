import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter



class EasyOcr():

    def extract_text(image_path, in_lang):
        image = cv2.imread(image_path)
        reader = easyocr.Reader(['en'], gpu=True)  # List of languages passed to Reader as well as gpu activation for processing time
        
        result = reader.readtext(image)
        print((result)) #Allows us to see what the OCR read
        return result


    def return_image(image_path, result):
        # Load the image using OpenCV
        image = cv2.imread(image_path)
        
        # Initialize EasyOCR reader
        
        # Extract text from the image
        # result = reader.readtext(image)
        
        annotated_image = image.copy()  # Create a copy of the image for annotation
        
        # Iterate over the result of text extraction
        for detection in result:
            text = detection[1]
            bbox = detection[0]
            
            # Convert bbox to an array of pixels
            polygon = np.array(bbox, dtype=np.int32)
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [polygon], 255)
            
            # Get bounding box coordinates
            x_min = int(min(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
            x_max = int(max(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
            y_min = int(min(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
            y_max = int(max(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
            
            # Get the surrounding pixels (above, below, left, and right)
            surrounding_pixels = []
            
            # Above
            if y_min > 0:
                surrounding_pixels.append(image[y_min-1, x_min:x_max].tolist())
            
            # Below
            if y_max < image.shape[0]:
                surrounding_pixels.append(image[y_max+1, x_min:x_max].tolist())
            
            # Left
            if x_min > 0:
                surrounding_pixels.append(image[y_min:y_max, x_min-1].tolist())
            
            # Right
            if x_max < image.shape[1]:
                surrounding_pixels.append(image[y_min:y_max, x_max+1].tolist())
            
            # Flatten and average all surrounding pixels
            surrounding_pixels = [pixel for sublist in surrounding_pixels for pixel in sublist]
            background_color = np.mean(surrounding_pixels, axis=0)
            background_color = tuple(map(int, background_color))
            
            # Fill the polygon with the background color
            cv2.fillPoly(annotated_image, [polygon], color=background_color)
            
            # Convert background color to grayscale intensity for better differentiation
            def rgb_to_intensity(c):
                return 0.2989 * c[2] + 0.587 * c[1] + 0.114 * c[0]  # Using standard luminance formula
            
            background_intensity = rgb_to_intensity(background_color)
            
            # Get all pixels inside the bounding box in RGB
            text_region = cv2.bitwise_and(image, image, mask=mask)
            text_pixels_rgb = text_region[mask == 255]
            
            # Filter out background-like pixels based on intensity
            def is_similar_color(pixel, threshold=25):
                # Calculate intensity for each pixel and compare to background intensity
                pixel_intensity = rgb_to_intensity(pixel)
                return abs(pixel_intensity - background_intensity) < threshold
            
            # Convert pixels to tuples for comparison
            text_pixels_rgb = [tuple(pixel) for pixel in text_pixels_rgb]
            
            # Exclude pixels that are too similar to the background color
            text_pixels_rgb = [pixel for pixel in text_pixels_rgb if not is_similar_color(pixel)]
            
            # Find the most common colors inside the bounding box
            color_counts = Counter(tuple(pixel) for pixel in text_pixels_rgb)
            common_colors = color_counts.most_common()
            
            # Filter out common colors that are too similar to the background
            def is_different_from_background(color, threshold=25):
                return np.linalg.norm(np.array(color) - np.array(background_color)) > threshold
            
            filtered_common_colors = [color for color in common_colors if is_different_from_background(color[0])]
            
            # Get top 3 colors
            top_colors = filtered_common_colors[:3]
            
            # Sort colors based on their distance from the background color
            def color_distance(c1, c2):
                return np.linalg.norm(np.array(c1) - np.array(c2))
            
            # Sort top colors based on their difference from the background color (most different first)
            top_colors_sorted = sorted(top_colors, key=lambda x: color_distance(x[0], background_color), reverse=True)
            
            # Get color 1, color 2, and color 3 (text color is the most different)
            color_1 = top_colors_sorted[0][0] if len(top_colors_sorted) > 0 else (0, 0, 0)
            color_2 = top_colors_sorted[1][0] if len(top_colors_sorted) > 1 else (255, 255, 255)
            color_3 = top_colors_sorted[2][0] if len(top_colors_sorted) > 2 else (255, 255, 255)
            
            color_text = (int(color_1[0]), int(color_1[1]), int(color_1[2]))  # Text color set to BGR format)
            
            # Calculate the width and height of the bounding box
            box_width = x_max - x_min
            box_height = y_max - y_min
            
            # Adjust font scale so that the text fits inside the box
            font_scale = 1
            while True:
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, font_scale, 2)[0]
                if text_size[0] > box_width or text_size[1] > box_height:
                    font_scale -= 0.1
                else:
                    break
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            # Calculate the text size and position
            text_size = cv2.getTextSize(text, font, font_scale, 1)[0]
            text_x = int(x_min + (box_width - text_size[0]) / 2)  # Center the text horizontally
            text_y = int(y_min + (box_height + text_size[1]) / 2)  # Center the text vertically
            
            # Draw the text in the bounding box with the calculated font size
            cv2.putText(annotated_image, text, (text_x, text_y), font, font_scale, color_text, 2, cv2.LINE_AA)
        
       
        
        
        return annotated_image
    
    def mergeBox(image_path,result):
        image = cv2.imread(image_path)
        # get width and height of the image
        height, width = image.shape[:2] 

        # margin of error horizontaly
        horError = int(width/30)
        heightError = int(height/20)
        vertError = int(height/80)
        numOfBoxes= len(result)
        numOfBoxesMerged=0

        for i in range(len(result)-1):
            delList=[]
            # getting the bounding box from results
            bbox1 = result[i][0]
            text1= result[i][1]
            #getting the next bounding box
            try:
                bbox2 = result[i+1][0]
                text2 =result[i+1][1]
            except:
                pass
            # coordinates for box 1
            x1_min = int(min(bbox1[0][0], bbox1[1][0], bbox1[2][0], bbox1[3][0]))
            y1_min = int(min(bbox1[0][1], bbox1[1][1], bbox1[2][1], bbox1[3][1]))
            x1_max = int(max(bbox1[0][0], bbox1[1][0], bbox1[2][0], bbox1[3][0]))
            y1_max = int(max(bbox1[0][1], bbox1[1][1], bbox1[2][1], bbox1[3][1]))

            # coordinates for box 2
            x2_min = int(min(bbox2[0][0], bbox2[1][0], bbox2[2][0], bbox2[3][0]))
            y2_min = int(min(bbox2[0][1], bbox2[1][1], bbox2[2][1], bbox2[3][1]))
            x2_max = int(max(bbox2[0][0], bbox2[1][0], bbox2[2][0], bbox2[3][0]))
            y2_max = int(max(bbox2[0][1], bbox2[1][1], bbox2[2][1], bbox2[3][1]))

            # how close are the boxes horizontally
            horSpace = x2_min - x1_max
            #how close are the top of the boxes to the same vertically
            vertTopSpace = abs(y1_min -y2_min)
            vertBottomSpace = abs(y1_max-y2_max)
            # vert space between
            vertBetweenSpace = y1_max - y2_min
            # how tall are the box relatively
            simSize =abs((y1_max-y1_min)-(y2_max-y2_min))

            # check to see if the boxes are on the same line
            if vertBetweenSpace < 0 or vertBottomSpace > vertError or vertTopSpace > vertError:
                continue

            # check to see how close the boxes are
            if horSpace < horError and horSpace >-40:


                # check to see if boxes are similar height
                if simSize < heightError:
                    # adding new bounding box to array in the order top left, top right, bottom right, bottom left
                    result[i+1][0] = [[x1_min,y1_min],[x2_max,y1_min],[x2_max,y1_max],[x1_min,y1_max]]
                    result[i+1][1]= text1+" "+text2
                    # result.pop(i)
                    # marking results for deletion
                    print(f"vertBetween space: {vertBetweenSpace}, vertTop: {vertTopSpace}, vertBottom: {vertBottomSpace}, vertError: {vertError} horSpace: {horSpace}, horError: {horError}")
                    delList.append(i)
                    numOfBoxesMerged +=1
                else:
                    pass
            else:
                pass
        print(f"number of boxes to start: {numOfBoxes}")
        print(f"number of boxes merged: {numOfBoxesMerged}")
        for i in delList:
            result.pop(i)
        return result



                    

            
            









