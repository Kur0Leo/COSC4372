import cv2
import numpy as np


class GetDiff:
    def __init__(self, input_image, reconstructed_image):
        self.input_image = input_image
        self.reconstructed_image = reconstructed_image

    def get_diff(self):
        shape = np.shape(self.input_image)
        img = np.zeros(shape)

        for i in range(0, shape[0]):
            for j in range(0,shape[1]):
                img[i][j] = self.input_image[i][j] - self.reconstructed_image[i][j]

        return img
