import cv2
import numpy as np


class FFT:
    def __init__(self, image, row, col):
        self.image = image
        self.row = row
        self.col = col

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

    def get_fft(self):
        fft = np.fft.fft2(self.image)
        fft_shift = np.fft.fftshift(fft)

        mag_fft = self.post_process_image(np.abs(fft_shift))

        return [mag_fft, fft_shift]
