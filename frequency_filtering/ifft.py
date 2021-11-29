import cv2
import numpy as np


class InverseFFT:
    def __init__(self, image):
        self.image = image

    def get_ifft(self):
        inverse_shift = np.fft.ifftshift(self.image)
        inverse_fft = np.fft.ifft2(inverse_shift)

        img = np.abs(inverse_fft)

        return img
