import traceback

from flask import Flask, jsonify, request
#from Annoy import get_similar_images
from flask_cors import CORS
from annoy_indexes_test import similar_images_from_url

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

@app.route('/api/images', methods=['GET', 'POST'])
def images():
    if request.method == 'GET':
        image_urls = [
            "https://static.zara.net/photos///2024/V/0/3/p/5767/521/712/2/w/2048/5767521712_3_1_1.jpg?ts=1707751046435",
            "https://static.zara.net/photos///2024/V/0/1/p/5862/059/811/2/w/2048/5862059811_3_1_1.jpg?ts=1707511076020",
            "https://static.zara.net/photos///2024/V/0/1/p/6147/105/427/2/w/2048/6147105427_3_1_1.jpg?ts=1710507096429",
            "https://static.zara.net/photos///2024/V/0/1/p/2513/750/500/2/w/2048/2513750500_3_1_1.jpg?ts=1706866499269",
            "https://static.zara.net/photos///2024/V/0/2/p/0840/465/444/2/w/2048/0840465444_3_1_1.jpg?ts=1712655394433",
            "https://static.zara.net/photos///2024/V/0/3/p/4442/660/712/2/w/2048/4442660712_3_1_1.jpg?ts=1705317447332",
            "https://static.zara.net/photos///2024/V/1/3/p/4546/330/010/2/w/2048/4546330010_3_1_1.jpg?ts=1708438825678",
            "https://static.zara.net/photos///2023/I/1/3/p/1251/230/800/2/w/2048/1251230800_3_1_1.jpg?ts=1697466806411",
            "https://static.zara.net/photos///2023/I/0/2/p/4767/488/723/2/w/2048/4767488723_3_1_1.jpg?ts=1685607087434",
            "https://static.zara.net/photos///2023/I/0/3/p/6887/602/250/2/w/2048/6887602250_3_1_1.jpg?ts=1689860680377"
        ]



        return jsonify({'image_urls': image_urls}), 200

    elif request.method == 'POST':
        try:
            # Obtener la URL de la imagen de la solicitud POST
            image_url = request.json.get('imageUrl')
            print(request.json)
            # Imprimir la URL de la imagen en el servidor Flask
            print("Received image URL:", image_url)

            # Llamada algoritmo para obtener data set imagenes similares
            try:
                urls = similar_images_from_url(image_url)
            except Exception as e:
                traceback.print_exc()
                return jsonify({'error': str(e)}), 404
            return jsonify(urls[1:]), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)