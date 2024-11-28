from flask import Flask, request, jsonify
from flask_cors import CORS

import PIL
import PIL.Image

import tensorflow as tf

print("TensorFlow version:", tf.__version__)

from tensorflow.keras.models import load_model
#from tensorflow.preprocessing.image import load_img, img_to_array

from tensorflow.keras.utils import img_to_array, load_img

import os

# Configurações básicas
app = Flask(__name__)
CORS(app)

# Diretório para salvar imagens
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Carregar o modelo de classificação
MODEL_PATH = 'flask_api/model/my_flower_model_2.keras'  # Atualize o caminho para seu modelo
model = load_model(MODEL_PATH, compile=False)

# Lista das espécies de flores
CLASSES = ['Rose', 'Tulip', 'Daisy', 'Dandelion', 'Sunflower']  # Atualize conforme seu modelo

@app.route('/classify', methods=['POST'])
def classify_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Salvar a imagem
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Preprocessar a imagem
    image = load_img(file_path, target_size=(224, 224))  # Ajuste o tamanho conforme o modelo
    image_array = img_to_array(image)
    image_array = image_array / 255.0  # Normalizar
    image_array = image_array.reshape((1, *image_array.shape))

    # Fazer a predição
    predictions = model.predict(image_array)
    predicted_class = CLASSES[predictions.argmax()]

    return jsonify({'class': predicted_class, 'confidence': float(predictions.max())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
