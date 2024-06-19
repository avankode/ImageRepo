from flask import Flask, request, jsonify
from skimage import io, img_as_float
import brisque
import requests
from io import BytesIO

app = Flask(__name__)

# Initialize BRISQUE model globally
brisque_model = brisque.BRISQUE()

def compute_brisque_score(image):
    score = brisque_model.score(image)
    return score

@app.route('/evaluate', methods=['GET'])
def evaluate_image():
    try:
        image_url = request.args.get('imageUrl')
        if not image_url:
            return jsonify({"error": "Missing 'imageUrl' in request"}), 400
        
        # Fetch image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error if the fetch fails

        # Read image from response content
        image = io.imread(BytesIO(response.content))
        image = img_as_float(image)
        
        # Compute BRISQUE score
        score = compute_brisque_score(image)
        quality = "High" if score < 30 else "Low"
        
        return jsonify({"score": score, "quality": quality})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching image from URL: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
