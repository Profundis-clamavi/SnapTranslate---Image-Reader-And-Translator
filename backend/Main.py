import cv2
import os
from Translation import SeamlessTranslate
from ocr import EasyOcr
from timer import Timer
import cProfile, pstats
import datetime



def select_language(language_type):
    all_languages = ['en', 'th', 'ch_tra', 'ch_sim', 'ja', 'ko', 'ar']
    print(f"Please select a {language_type} language from the following:")
    print("1. English\n2. Thai\n3. Traditional Chinese\n4. Simplified Chinese\n5. Japanese\n6. Korean\n7. Arabic")

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
            return 'ar'
        else:
            print("Invalid selection. Please choose a valid number from 1 to 7.")
            return None
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None
    

def translate_text(translator, extracted_text, in_lang, out_lang):
    strings = []
    for i in extracted_text:
        print(i[1])
        strings.append(i[1])
    print(strings)
    # creating and loading the translation model
    # translator= SeamlessTranslate()
    # processed_text = translate.process_input(strings)
    output_text = translator.Translate(strings, src_lang=in_lang, tgt_lang=out_lang)
    # output = translate.Translate("Hi")
    
    
    return output_text


def local():
    in_lang = select_language("input language")
    out_lang = select_language("output language")
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, input("Enter the path to the image file: "))
    print("Loading...")
    t1=Timer()
    t1.start()
    translator= SeamlessTranslate()
    print("loading time:")
    t1.stop()
    
    t =Timer()
    t.start()
    extracted_text = EasyOcr.extract_text(image_path, in_lang)

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
    EasyOcr.display_text(image_path, listExtracted_text)
    print(output_text)
    for (bbox, text, prob) in extracted_text:
        print(f'Text: {text}, Probability: {prob}')

def api(image_path, in_lang, out_lang, translator):
    # directory where we store images
    # base_path = os.path.dirname(__file__)
    # translator = SeamlessTranslate()
    t1=Timer()
    t1.start()
    extracted_text = EasyOcr.extract_text(image_path, in_lang)
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

        # displaying the image with translated text
    # EasyOcr.display_text(image_path, listExtracted_text)
    # print(output_text)
    # for (bbox, text, prob) in extracted_text:
    #         print(f'Text: {text}, Probability: {prob}')
    # saving the image to directory
    img = EasyOcr.return_image(image_path, listExtracted_text)
    # might need this to save but i think we can get away without
    # filename = 'savedImage.jpg'
    # cv2.imwrite(filename, img)
    # print("After saving image:")  
    # print(os.listdir(directory))

    # print('Successfully saved')
    t1.stop()
    return img


# a function to test the processing.
def test():
    in_lang = "eng"
    out_lang = "fra"
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "Test16.png")
    print("Loading...")
    t1=Timer()
    t1.start()
    translator= SeamlessTranslate()
    print("loading time:")
    t1.stop()
    
    t2 =Timer()
    t2.start()
    extracted_text = EasyOcr.extract_text(image_path, in_lang)
    print("Extracting time:")
    t2.stop()

    t3 = Timer()
    t3.start()
    output_text = translate_text(translator, extracted_text, in_lang, out_lang)
    print("Translating Time:")
    t3.stop()
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
    
    # displaying the image with translated text
    # EasyOcr.display_text(image_path, listExtracted_text)
    # print(output_text)
    # for (bbox, text, prob) in extracted_text:
    #     print(f'Text: {text}, Probability: {prob}')




def profiler():
    # Create profiler instance
    profiler = cProfile.Profile()
    
    # Start profiling
    profiler.enable()
    
    # Run the function to be profiled
    test()
    
    # Stop profiling
    profiler.disable()

    # Ensure the directory for the profile results exists
    output_dir = 'Profiles'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a timestamp to append to the filename to avoid overwriting
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f'profile_results_{timestamp}.pstat')

    # Create the stats object, sort by cumulative time, and strip the directories
    stats = pstats.Stats(profiler).sort_stats('cumtime').strip_dirs()

    # Save the stats to a file with the timestamp in the filename
    stats.dump_stats(filename)

    print(f"Profile results saved to: {filename}")

# uncomment to run profiler
# profiler()



