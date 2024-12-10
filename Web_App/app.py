from flask import *
import os
from werkzeug.utils import secure_filename
from keras.models import load_model
import numpy as np
from PIL import Image

app = Flask(__name__)

# Classes of traffic signs
classes = { 0:'Speed limit (20km/h)',
            1:'Speed limit (30km/h)',
            2:'Speed limit (50km/h)',
            3:'Speed limit (60km/h)',
            4:'Speed limit (70km/h)',
            5:'Speed limit (80km/h)',
            6:'End of speed limit (80km/h)',
            7:'Speed limit (100km/h)',
            8:'Speed limit (120km/h)',
            9:'No passing',
            10:'No passing veh over 3.5 tons',
            11:'Right-of-way at intersection',
            12:'Priority road',
            13:'Yield',
            14:'Stop',
            15:'No vehicles',
            16:'Vehicle > 3.5 tons prohibited',
            17:'No entry',
            18:'General caution',
            19:'Dangerous curve left',
            20:'Dangerous curve right',
            21:'Double curve',
            22:'Bumpy road',
            23:'Slippery road',
            24:'Road narrows on the right',
            25:'Road work',
            26:'Traffic signals',
            27:'Pedestrians',
            28:'Children crossing',
            29:'Bicycles crossing',
            30:'Beware of ice/snow',
            31:'Wild animals crossing',
            32:'End speed + passing limits',
            33:'Turn right ahead',
            34:'Turn left ahead',
            35:'Ahead only',
            36:'Go straight or right',
            37:'Go straight or left',
            38:'Keep right',
            39:'Keep left',
            40:'Roundabout mandatory',
            41:'End of no passing',
            42:'End no passing vehicle > 3.5 tons'}

def image_processing(img):
    model = load_model('./model/TSR.h5')
    data = []
    image = Image.open(img)
    image = image.resize((30, 30))  # Assuming the model was trained with this input size
    data.append(np.array(image))
    X_test = np.array(data)
    
    # Predict the class index with the updated method
    Y_pred = np.argmax(model.predict(X_test), axis=-1)
    return Y_pred


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded!"}), 400
    
    f = request.files['file']
    file_path = secure_filename(f.filename)
    f.save(file_path)
    
    try:
        result = image_processing(file_path)
        response = {"result": f"Predicted Traffic🚦Sign is: {classes[int(result[0])]}"}
    finally:
        os.remove(file_path)  # Ensure the file is removed even if there's an error.
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)