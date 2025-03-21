from flask import Flask, request, jsonify
from flask_cors import CORS
from Main import api
from Translation import SeamlessTranslate
import os

app = Flask(__name__)
app.translator = SeamlessTranslate()
CORS(app, supports_credentials=True)

# backend endpoint for our whole program
@app.route("/api", methods=["POST"])
def process():
    #get the language selections from the form that was submitted
    input_language = request.form.get('inputLanguage')
    output_language = request.form.get('outputLanguage')

    #check if there was an image, if not return error
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"})
        
    image_file = request.files['image']
    temp_path = "temp_upload.jpg"
    image_file.save(temp_path)

    
    #call backend endpoint with data
    output_image = api(temp_path, input_language, output_language,app.translator)
    import cv2

    #convert output image to format to be returned to UI
    _, buffer = cv2.imencode('.jpg', output_image)
    image_bytes = buffer.tobytes()

    import base64
    encoded_img = base64.b64encode(image_bytes).decode('utf-8')

    result = {
        "message": "Translation successful",
        "inputLanguage": input_language,
        "outputLanguage": output_language,
        "fileName": image_file.filename,
        "translatedImage": f"data:image/jpeg;base64,{encoded_img}"
        }
    #returns data to frontend, with new image: translatedImage
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000)
