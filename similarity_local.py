from flask import Flask
from flask import json
from flask import Response
import os
import cv2
import numpy as np
import glob
from PIL import Image

image_to_upload = cv2.imread("similar/path.png")

# Save filename into Array
file_names = []
for root, dirs, files in os.walk("similar"):
    for filename in files:
        if filename.endswith(".png"):
                file_names.append(filename)

# Save image file into Numpy Array
image_ori_loc = glob.glob('similar/*.png')
image_list = np.array([np.array(Image.open(f_name)) for f_name in image_ori_loc])

if image_list.size <= 0:
    print('compared image is empty')
else:
    for i in range(image_list.size):
        print(i)
        image_to_compare = cv2.resize(image_to_upload, (700, 450))
        convert_color = cv2.cvtColor(image_list.__getitem__(1), cv2.COLOR_BGR2RGB)
        original = cv2.resize(convert_color, (700, 450))

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
        sift = cv2.xfeatures2d.SIFT_create(nfeatures=10)
        kp_1, desc_1 = sift.detectAndCompute(original, None)
        kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)

        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(desc_1, desc_2, k=2)

        good_points = []
        for m, n in matches:
            if m.distance < 0.8 * n.distance:
                good_points.append(m)

        # Define how similar they are
        if len(kp_1) <= len(kp_2):
            number_keypoints = len(kp_1)
        else:
            number_keypoints = len(kp_2)

        print("Keypoints COMP Image: " + str(len(kp_2)))
        print("Keypoints of " + file_names.__getitem__(1) + " : " + str(len(kp_1)))
        print("GOOD Matches:", len(good_points))
        print("How good it's the match: ", len(
                good_points) / number_keypoints * 100)

        result = cv2.drawMatches(original, kp_1, image_to_compare, kp_2, good_points, None)

        cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))
        cv2.imwrite("feature_matching.jpg", result)

        cv2.imshow("Original", cv2.resize(original, None, fx=0.4, fy=0.4))
        cv2.imshow("Duplicate", cv2.resize(image_to_compare, None, fx=0.4, fy=0.4))
        cv2.waitKey(0)
        cv2.destroyAllWindows()