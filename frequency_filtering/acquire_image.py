import cv2
import numpy as np
from frequency_filtering.ifft import InverseFFT


class AcquireImage:
    def __init__(self, data, half_fourier, row, column):
        self.data = data
        self.half_fourier = half_fourier
        self.row = row
        self.column = column

    def acquire_missing_data(self, position):
        shape = np.shape(self.data)
        if position == "top":
            for i in range(0, shape[0] // 2):
                for j in range(0, shape[1] // 2):
                    self.data[shape[0] - i - 1][shape[1] - j - 1] = np.conj(self.data[i][j])
            for i in range(0, shape[0] // 2):
                for j in range(shape[1] - 1, shape[1] // 2, -1):
                    self.data[shape[0] - i - 1][shape[1] - j - 1] = np.conj(self.data[i][j])
        elif position == "bottom":
            for i in range(shape[0] - 1, shape[0] // 2, -1):
                for j in range(0, shape[1] // 2):
                    self.data[shape[0] - i - 1][shape[1] - j - 1] = np.conj(self.data[i][j])
            for i in range(shape[0] - 1, shape[0] // 2, -1):
                for j in range(shape[1] - 1, shape[1] // 2, -1):
                    self.data[shape[0] - i - 1][shape[1] - j - 1] = np.conj(self.data[i][j])
        elif position == "right":
            for i in range(0, shape[0] // 2):
                for j in range(0, shape[1] // 2):
                    self.data[shape[0] - i - 1][shape[1] - j - 1] = np.conj(self.data[i][j])
            for i in range(shape[0] - 1, shape[0] // 2, -1):
                for j in range(0, shape[1] // 2):
                    self.data[shape[0] - i - 1][shape[1] - j - 1] = np.conj(self.data[i][j])
        elif position == "left":
            for i in range(0, shape[0] // 2):
                for j in range(shape[1] - 1, shape[1] // 2, -1):
                    self.data[shape[0] - i - 1][shape[1] - j - 1] = np.conj(self.data[i][j])
            for i in range(shape[0] - 1, shape[0] // 2, -1):
                for j in range(shape[1] - 1, shape[1] // 2, -1):
                    self.data[shape[0] - i - 1][shape[1] - j - 1] = np.conj(self.data[i][j])
        img_obj = InverseFFT(self.data)
        img = img_obj.get_ifft()
        return img

    def get_image(self):
        if self.half_fourier == 0:
            return self.acquire_missing_data("grid")

        elif self.half_fourier == 1:
            return self.acquire_missing_data("top")

        elif self.half_fourier == 2:
            return self.acquire_missing_data("bottom")

        elif self.half_fourier == 3:
            return self.acquire_missing_data("right")

        elif self.half_fourier == 4:
            return self.acquire_missing_data("left")
