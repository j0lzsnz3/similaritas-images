from flask import Flask, json, Response, request
import os
import cv2
import numpy as np
import glob
import base64
from PIL import Image
from result import Result

app = Flask(__name__, static_url_path="/image", static_folder="results")


@app.route('/api/compare/image', methods=['POST'])
def compare_image():
    result_of_compare = []

    encode_image = request.form['image_encode']
    image_file = save_image(encode_image)

    image_to_upload = cv2.imread(image_file)

    folder_name = "similar"
    file_names = save_file_name(folder_name)
    image_list = save_image_numpy(folder_name + '/*.png')

    if image_list.size <= 0:
        print('original image is empty')
    else:
        for i in range(image_list.size):
            print(i)
            image_to_compare = cv2.resize(image_to_upload, (700, 500))
            convert_color = cv2.cvtColor(image_list.__getitem__(i), cv2.COLOR_BGR2RGB)
            original = cv2.resize(convert_color, (700, 500))

            # Check if 2 images are equals
            if image_to_compare.shape == original.shape:
                print('the images have same size and channels')
                difference = cv2.subtract(original, image_to_compare)
                b, g, r = cv2.split(difference)

                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    print('the images are completly Equal')
                else:
                    print('the images are not Equal')

            # 2) Check for similarities between the 2 images
            sift = cv2.xfeatures2d.SIFT_create(nfeatures=15)
            kp_1, desc_1 = sift.detectAndCompute(original, None)
            kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

            index_params = dict(algorithm=0, trees=5)
            search_params = dict()
            flann = cv2.FlannBasedMatcher(index_params, search_params)

            matches = flann.knnMatch(desc_1, desc_2, k=2)

            good_points = []
            for m, n in matches:
                if m.distance < 0.89 * n.distance:
                    good_points.append(m)

            # Define how similar they are
            if len(kp_1) <= len(kp_2):
                number_keypoints = len(kp_1)
            else:
                number_keypoints = len(kp_2)

            good_match = len(
                good_points) / number_keypoints * 100

            image_result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)
            image_result_name = "result_w_" + file_names.__getitem__(i)
            path = 'results/'
            cv2.imwrite(path + image_result_name, image_result)

            # Insert all result into Result class
            result = Result(file_names.__getitem__(i), good_match, "image/" + image_result_name)
            result_of_compare.append(result)

        response = {
            'response': {
                'image_to_compare': image_file,
                'result': [e.toJSON() for e in result_of_compare]
            }
        }

        resp = Response(json.dumps(response), status=200, mimetype='application/json')
        resp.headers['Link'] = 'http://127.0.0.1:5000'
        return resp


def save_file_name(folder_image):
    # Save filename into Array
    file_names = []
    for root, dirs, files in os.walk(folder_image):
        for filename in files:
            if filename.endswith(".png"):
                file_names.append(filename)
    return file_names


def save_image_numpy(folder_type):
    # Save image file into Numpy Array
    image_ori_loc = glob.glob(folder_type)
    image_list = np.array([np.array(Image.open(f_name)) for f_name in image_ori_loc])

    return image_list


def save_image(encode_image):
    img_data = base64.b64decode(encode_image)
    filename = 'image_to_compare.png'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(img_data)

    return filename


if __name__ == '__main__':
    app.run(host='0.0.0.0')
