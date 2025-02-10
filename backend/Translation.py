from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText

# Load the pre-trained model and processor
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2ForTextToText.from_pretrained("facebook/seamless-m4t-v2-large")

# Example text input (English text to translate to Russian)
text_to_translate = "Hello, my dog is cute"

# Process the input text (Source: English, Target: Russian)
text_inputs = processor(text=text_to_translate, src_lang="eng", return_tensors="pt")

# Perform the text-to-text translation (English to Russian in this case)
translated_text = model.generate(**text_inputs, tgt_lang="rus")[0]
translated_text_decoded = processor.decode(translated_text, skip_special_tokens=True)

# Print the original and translated text
print(f"Original: {text_to_translate}")
print(f"Translated: {translated_text_decoded}")