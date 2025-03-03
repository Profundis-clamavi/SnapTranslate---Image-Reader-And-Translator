from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText
from typing import List, Dict, Any
import torch

class SeamlessTranslate():
    def __init__(self, lang = "none"):
        self.lang =lang
        # Load the pre-trained model and processor
        self.processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
        self.model = SeamlessM4Tv2ForTextToText.from_pretrained("facebook/seamless-m4t-v2-large").to('cuda')

    def Translate(self, input,src_lang="eng",tgt_lang="eng"):
    #     # Process the input text (Source: English, Target: Russian)
    #     translated = []
    #     for text in input:
    #         text_inputs = self.processor(text=text, src_lang = src_lang, return_tensors="pt").to('cuda')
    #         print(text_inputs)
    #         # Perform the text-to-text translation (English to Russian in this case)
    #         translated_text = self.model.generate(**text_inputs, tgt_lang=tgt_lang)[0]
    #         translated_text_decoded = self.processor.decode(translated_text.tolist(), skip_special_tokens=True)
    #         translated.append(translated_text_decoded)
    #     return translated
        # ---------------------------------------------------------------------------
        # Process the input text
        input_texts = self.process_input(input)

        # Create the batch input for processing
        text_inputs = self.processor(text=input_texts, src_lang=src_lang, return_tensors="pt", padding=True).to('cuda')

        # Perform batch translation
        translated_ids = self.model.generate(**text_inputs, tgt_lang=tgt_lang)

        # Decode each translated sentence
        translated_texts = []
        for translated_id in translated_ids:
            # Decode each sequence in the batch individually
            decoded_text = self.processor.decode(translated_id.tolist(), skip_special_tokens=True)
            translated_texts.append(decoded_text)

        return translated_texts
        
    

    def process_input(self, input) -> List[str]:
        """
        Ensure input is converted into a list of strings.
        """
        if isinstance(input, str):
            return [input]  # Single string, wrap it in a list
        elif isinstance(input, list):
            if all(isinstance(i, str) for i in input):
                return input  # List of strings, return as-is
            elif all(isinstance(i, dict) for i in input):
                # If it's a list of dictionaries, assume each dict has a key 'text'
                return [i.get('text', '') for i in input]  # Extract text from dicts
            elif all(isinstance(i, list) for i in input):
                # If it's a list of lists, flatten it to a list of strings
                return [str(sub_item) for sublist in input for sub_item in sublist]
        raise ValueError(f"Unsupported input type: {type(input)}")