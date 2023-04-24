from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

from utils.image_modifier import create_modified_image
from utils.gallery import get_image_filenames, get_image

app = Flask(__name__)
CORS(app)

@app.route('/images', methods=['GET'])
def show_images():
    directory = './outputs'  # replace with your directory path
    images = get_image_filenames(directory)
    return jsonify(images)

@app.route('/images/<image_id>', methods=['GET'])
def get_image_endpoint(image_id):
    image_path = get_image(image_id)
    if image_path:
        return send_file(image_path, mimetype='image/png', as_attachment=True)
    else:
        return "Image not found", 404

@app.route('/modify-image', methods=['POST'])
def modify_image():
    # Get the cloudlet name from the request body
    cloudlet_name = request.json['cloudlet_name']

    # Create the modified image
    create_modified_image(cloudlet_name)

    # Return the modified image as a file download
    return send_file(f'outputs/{cloudlet_name}.png', mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)