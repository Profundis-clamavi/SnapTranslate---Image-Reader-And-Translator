import os
from backend.Translation import SeamlessTranslate
from backend.ocr import EasyOcr
from backend.timer import Timer
import cProfile, pstats
import datetime




    

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
    if (len(listExtracted_text)>0):
        for i in listExtracted_text:
                i[1] = output_text[x]
                x+=1


    if len(listExtracted_text) > 1:
        listExtracted_text=EasyOcr.mergeBox(image_path,listExtracted_text)
    # img = EasyOcr.return_image(image_path, listExtracted_text)
    ocr = EasyOcr()
    img = ocr.return_image(image_path, listExtracted_text)
    # img = EasyOcr.return_image_utf8_cv(image_path, listExtracted_text)
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
    print(output_text)
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
    



def testOcr():
    in_lang = "eng"
    out_lang = "fra"
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "Test8.jpg")
    print("Loading...")
    
    t2 =Timer()
    t2.start()
    extracted_text = EasyOcr.extract_text(image_path, in_lang)
    print("Extracting time:")
    t2.stop()

    # print(output_text)
    listExtracted_text =[]
    # creating a list out of tuple so we can modify values
    for i in extracted_text:
        listExtracted_text.append(list(i))

    for (bbox, text, prob) in extracted_text:
        print(f'Text: {text}, Probability: {prob}, Bounding box: top left:{bbox[0]}, top right:{bbox[1]}, bottom right:{bbox[2]}, bottom left{bbox[3]}')
    
    # displaying the image with translated text
    listExtracted_text=EasyOcr.mergeBox(image_path,listExtracted_text)
    EasyOcr.display_text(image_path, listExtracted_text)
    # print(output_text)
    




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


if __name__=="main":
    testOcr()

