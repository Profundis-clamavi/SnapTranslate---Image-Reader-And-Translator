import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw,Image
import os



class EasyOcr():
    def __init__(self):
        ...

    def extract_text(image_path, in_lang):
        reader = easyocr.Reader(['en'], gpu=True)  # List of languages passed to Reader as well as gpu activation for processing time
        
        result = reader.readtext(image_path)
        print((result)) #Allows us to see what the OCR read
        return result



    def display_text(image_path, result):
        image = cv2.imread(image_path) #Using cv2 to "scan" the image

        for detection in result: #Each detection is expected to have a bounding box. This section fetches them.
            bbox = detection[0]
            text = detection[1]
            x_min = int(min(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
            y_min = int(min(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
            x_max = int(max(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
            y_max = int(max(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))

            margin = 0
            #Setting a region equal to the bounding box
            region = image[max(0, y_min - margin):y_max + margin, max(0, x_min - margin):x_max + margin] 
            #Getting the average color of the bounding box
            avg_color = np.mean(region, axis=(0, 1))

            text_area = image[y_min:y_max, x_min:x_max]
            text_color = np.mean(text_area, axis=(0, 1))

            rect_color = avg_color - text_color / 3.5
            rect_color = np.clip(rect_color, 0, 255)

            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (avg_color), thickness=-1)

            text_color = (avg_color)

            box_width = x_max - x_min
            box_height = y_max - y_min

            font_scale = 1
            while True:
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, font_scale, 2)[0]
                if text_size[0] > box_width or text_size[1] > box_height:
                    font_scale -= 0.1
                else:
                    break

            text_x = x_min + (box_width - text_size[0]) // 2
            text_y = y_min + (box_height + text_size[1]) // 2
            cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, font_scale, (0, 0, 255), 1)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        plt.imshow(image_rgb)
        plt.axis('off')
        plt.show()

    def return_image(image_path, result):
        image = cv2.imread(image_path)

        for detection in result:
            bbox = detection[0]
            text = detection[1]

            x_min = int(min(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
            y_min = int(min(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
            x_max = int(max(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
            y_max = int(max(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))

            margin = 5
            region = image[max(0, y_min - margin):y_max + margin, max(0, x_min - margin):x_max + margin]
            avg_color = np.mean(region, axis=(0, 1))

            text_area = image[y_min:y_max, x_min:x_max]
            text_color = np.mean(text_area, axis=(0, 1))

            rect_color = (255,255,255)

            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), ((avg_color)), thickness=-1)

            # text_color = (255, 255, 255)

            box_width = x_max - x_min
            box_height = y_max - y_min

            font_scale = 1
            while True:
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, font_scale, 2)[0]
                if text_size[0] > box_width or text_size[1] > box_height:
                    font_scale -= 0.1
                else:
                    break

            text_x = x_min + (box_width - text_size[0]) // 2
            text_y = y_min + (box_height + text_size[1]) // 2
            # cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, font_scale * 1.5, (avg_color), 2)
            cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, font_scale, ((0,0,255)), 1)


        return image
    
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

    def get_text_size(self,text, box_width,box_height, font):
        im = Image.new('RGB', (box_width, box_height))
        draw = ImageDraw.Draw(im)
        return draw.textlength(text, font)

    def find_font_size(self, text, font, box_width, box_height, target_width_ratio):
        tested_font_size = 100
        tested_font = ImageFont.truetype(font, tested_font_size)
        observed_width, observed_height = self.get_text_size(text, box_width, box_height, tested_font)
        estimated_font_size = tested_font_size / (observed_width / box_width) * target_width_ratio
        return round(estimated_font_size)

    

    # supports utf-8 encoding
    def return_image_utf8_pil(self,image_path, result):
            image = cv2.imread(image_path)
            print("Current directory:", os.getcwd())
            fontpath = "./backend/Noto_Sans/static/NotoSans-Italic.ttf"    

            for detection in result:
                bbox = detection[0]
                text = detection[1]

                x_min = int(min(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
                y_min = int(min(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
                x_max = int(max(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
                y_max = int(max(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))

                margin = 5
                region = image[max(0, y_min - margin):y_max + margin, max(0, x_min - margin):x_max + margin]
                avg_color = np.mean(region, axis=(0, 1))

                text_area = image[y_min:y_max, x_min:x_max]
                text_color = np.mean(text_area, axis=(0, 1))

                rect_color = avg_color - text_color / 3.5
                rect_color = np.clip(rect_color, 0, 255)

                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (avg_color), thickness=-1)

                text_color = (255, 255, 255)

                box_width = x_max - x_min
                box_height = y_max - y_min

                # font_scale = 1
                # while True:
                #     text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, font_scale, 2)[0]
                #     if text_size[0] > box_width or text_size[1] > box_height:
                #         font_scale -= 0.1
                #     else:
                #         break

                # text_x = x_min + (box_width - text_size[0]) // 2
                # text_y = y_min + (box_height + text_size[1]) // 2


                
                font_size = box_height*0.9
                font = ImageFont.truetype(fontpath, font_size)
                while True:
                    text_size = font.getlength(text)
                    if text_size > box_width:
                        font_size -= 1
                        font = ImageFont.truetype(fontpath, font_size)
                    else:
                        break
                # font = ImageFont.truetype(fontpath, font_size)


                # a temporary image to find the text size
                im = Image.new('RGB', (box_width, box_height))
                draw = ImageDraw.Draw(im)

                # Get the bounding box of the text using textbbox()
                text_bbox = draw.textbbox((x_min, y_min), text, font=font)

                # Calculate the width and height of the text bounding box
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # Calculate the center position of the bounding box
                x_center = x_min + (x_max - x_min) // 2
                y_center = y_min + (y_max - y_min) // 2

                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(image_rgb)
                # img_pil = Image.fromarray(image)
                draw = ImageDraw.Draw(img_pil)
                draw.text((x_center, y_center), text, font=font, fill="red", anchor="mm")
                image = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
                # cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX, font_scale, (0, 0, 255), 1)

            return image
    
    
    

    # # supports utf-8 encoding
    # def return_image_utf8_cv(image_path, result):
    #         image = cv2.imread(image_path)

    #         for detection in result:
    #             bbox = detection[0]
    #             text = detection[1]

    #             x_min = int(min(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
    #             y_min = int(min(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))
    #             x_max = int(max(bbox[0][0], bbox[1][0], bbox[2][0], bbox[3][0]))
    #             y_max = int(max(bbox[0][1], bbox[1][1], bbox[2][1], bbox[3][1]))

    #             margin = 5
    #             region = image[max(0, y_min - margin):y_max + margin, max(0, x_min - margin):x_max + margin]
    #             avg_color = np.mean(region, axis=(0, 1))

    #             text_area = image[y_min:y_max, x_min:x_max]
    #             text_color = np.mean(text_area, axis=(0, 1))

    #             rect_color = avg_color - text_color / 3.5
    #             rect_color = np.clip(rect_color, 0, 255)

    #             cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (avg_color), thickness=-1)

    #             text_color = (255, 255, 255)

    #             box_width = x_max - x_min
    #             box_height = y_max - y_min

    #             font_scale = 1
    #             while True:
    #                 text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, font_scale, 2)[0]
    #                 if text_size[0] > box_width or text_size[1] > box_height:
    #                     font_scale -= 0.1
    #                 else:
    #                     break

    #             text_x = x_min + (box_width - text_size[0]) // 2
    #             text_y = y_min + (box_height + text_size[1]) // 2
    #             ft = cv2.freetype.createFreeType2()
    #             fontpath = "./backend/Noto_Sans/static/NotoSans-Italic.ttf"   
    #             ft.loadFontData(fontpath)
                  
                
    #             cv2.putText(image, text, (text_x, text_y), ft, font_scale, (0, 0, 255), 1)

    #         return image



                    

            
            









