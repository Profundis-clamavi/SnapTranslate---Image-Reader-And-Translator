import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt



class EasyOcr():

    def extract_text(image_path, in_lang):
        reader = easyocr.Reader(['en'], gpu=True)  # List of languages passed to Reader
        
        result = reader.readtext(image_path)
        print((result))
        return result



    def display_text(image_path, result):
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

            rect_color = avg_color - text_color / 3.5
            rect_color = np.clip(rect_color, 0, 255)

            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (avg_color), thickness=-1)

            text_color = (255, 255, 255)

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

            rect_color = avg_color - text_color / 3.5
            rect_color = np.clip(rect_color, 0, 255)

            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (avg_color), thickness=-1)

            text_color = (255, 255, 255)

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

        return image

