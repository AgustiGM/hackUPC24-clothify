from flask import Flask, jsonify, request
#from Annoy import get_similar_images
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and methods

@app.route('/')
def home():
    return "Welcome to the Image Similarity API! Use /api/images to get similar images."

"""@app.route('/api/images', methods=['POST'])
def images():
    try:
        # Obtener la imagen y la URL de la solicitud
        image_file = request.files['image']
        image_url = request.form['image_url']

        # Guardar la imagen en el servidor
        image_path = 'query_image.jpg'
        image_file.save(image_path)

        print("URL de la imagen:", image_url)
        print("Ruta de la imagen guardada:", image_path)
        # Llamar a la función get_similar_images con la imagen y la URL
        #similar_images = get_similar_images(image_path, image_url)

        return jsonify({'message': 'URL y imagen guardadas en el servidor'}), 200
        #return jsonify(similar_images), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
"""

@app.route('/api/images', methods=['POST'])
def images():
    try:
        # Obtener la URL de la imagen de la solicitud POST
        image_url = request.json.get('imageUrl')

        # Imprimir la URL de la imagen en el servidor Flask
        print("Received image URL:", image_url)

        # Llamada algoritmo para obtener data set imagenes similares

        return "Image URL received successfully", 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)