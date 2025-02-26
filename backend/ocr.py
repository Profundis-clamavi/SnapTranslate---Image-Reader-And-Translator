import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from Translation import SeamlessTranslate
from timer import Timer





def select_language(language_type):
    all_languages = ['en','th', 'ch_tra', 'ch_sim', 'ja', 'ko', 'ar']
    print(f"Please select a {language_type} language from the following:")
    print("1. English\n2. Thai\n3. Traditional Chinese\n4. Simplified Chinese\n5. Japanese\n6. Korean\n7. Arabic \n8. all language")

    input_lang_selector = input("Enter the number of your choice: ")
    
    try:
        input_lang_selector = int(input_lang_selector)
        if input_lang_selector == 1:
            return 'en'
        elif input_lang_selector == 2:
            return 'th'
        elif input_lang_selector == 3:
            return 'ch_tra'
        elif input_lang_selector == 4:
            return 'ch_sim'
        elif input_lang_selector == 5:
            return 'ja'
        elif input_lang_selector == 6:
            return 'ko'
        elif input_lang_selector == 7:
            return 'ar','en'
        elif input_lang_selector == 8:
            return all_languages
        else:
            print("Invalid selection. Please choose a valid number from 1 to 7.")
            return None
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None


def extract_text(image_path, in_lang):
    reader = easyocr.Reader(['ar','en'], gpu=True)  # List of languages passed to Reader
    
    result = reader.readtext(image_path)
    print((result))
    return result


#---------------------------------------------------------Nathaniel------------------------------------------------------------------
def translate_text(translator, extracted_text, in_lang, out_lang):
    strings = []
    for i in extracted_text:
        print(i[1])
        strings.append(i[1])
    print(strings)
    # creating and loading the translation model
    # translator= SeamlessTranslate()
    # processed_text = translate.process_input(strings)
    output_text = translator.Translate(strings)
    # output = translate.Translate("Hi")
    
    
    return output_text

#---------------------------------------------------------Nathaniel------------------------------------------------------------------






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
            # print(cv2.getBuildInformation())
            # ft = cv2.freetype.createFreeType2()
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

if __name__ == "__main__":
    print("Loading...")
    t1=Timer()
    t1.start()
    translator= SeamlessTranslate()
    print("loading time:")
    t1.stop()
    in_lang = select_language("input language")
    out_lang = select_language("output language")
    base_path = os.path.dirname(__file__)
    

    image_path = os.path.join(base_path, input("Enter the path to the image file: "))
    
    t =Timer()
    t.start()
    extracted_text = extract_text(image_path, in_lang)

    output_text = translate_text(translator, extracted_text, in_lang, out_lang)

    listExtracted_text =[]
    # creating a list out of tuple so we can modify values
    for i in extracted_text:
        listExtracted_text.append(list(i))
    
    # inserting translated text into the bounding box array
    x = 0
    print(type(listExtracted_text))
    for i in listExtracted_text:
        i[1] = output_text[x]
        x+=1

    print("processing time")
    t.stop()
    # displaying the image with translated text
    display_text(image_path, listExtracted_text)
    print(output_text)
    for (bbox, text, prob) in extracted_text:
        print(f'Text: {text}, Probability: {prob}')
    
