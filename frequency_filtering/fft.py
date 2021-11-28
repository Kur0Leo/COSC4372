import cv2
import numpy as np


class Filtering:
    def __init__(self, image):
        self.image = image

    def post_process_image(self, image):
        log = np.log(image)
        shape = np.shape(log)
        fsimage = np.zeros(shape, dtype=np.uint8)

        min = log[0][0]
        max = log[0][0]

        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                if log[i][j] < min:
                    min = log[i][j]
                if log[i][j] > max:
                    max = log[i][j]

        p = 255 / (max - min)
        l = (0 - min) * p

        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                fsimage[i][j] = p * log[i][j] + l

        return fsimage

    def filter(self):
        fft = np.fft.fft2(self.image)
        fft_shift = np.fft.fftshift(fft)

        mag_dft = self.post_process_image(np.abs(fft_shift))

        return mag_dft
