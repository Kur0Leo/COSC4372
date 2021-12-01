import cv2
import numpy as np
from frequency_filtering.ifft import InverseFFT


class Filtering:
    def __init__(self, image, data, row, col):
        self.image = image
        self.data = data
        self.row = row
        self.col = col

    def acquire_data(self, i, j):
        frequency = 0;
        for m in range(i-1, i+2):
            for n in range(j-1, j+2):
                frequency += self.data[m][n]
        frequency = frequency / 9
        return frequency;

    def fully_sampled_filtering(self):
        # blurred / use filter
        return self.image

    def undersampled_filtering(self):
        shape = np.shape(self.data)
        sampling_data = np.zeros(shape, dtype=complex)
        start_row = int(round((shape[0] / 2) - (self.row / 2)))
        start_col = int(round((shape[1] / 2) - (self.col / 2)))

        for i in range(start_row, start_row + self.row):
            for j in range(start_col, start_col + self.col):
                if (self.data[i][j] == 0):
                    sampling_data[i][j] = self.acquire_data(i, j)
                else:
                    sampling_data[i][j] = self.data[i][j]

        img_obj = InverseFFT(sampling_data)
        img = img_obj.get_ifft()

        return img
