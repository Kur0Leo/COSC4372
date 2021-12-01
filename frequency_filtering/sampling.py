import cv2
import numpy as np


class Sampling:
    def __init__(self, data, row, col, trajectory):
        self.mag_data = data[0]
        self.data = data[1]
        self.row = row
        self.col = col
        self.trajectory = trajectory

    def get_fully_sampled(self):
        shape = np.shape(self.data)
        mag_sampling_data = np.zeros(shape)
        sampling_data = np.zeros(shape, dtype=complex)
        start_row = int(round((shape[0]/2) - (self.row/2)))
        start_col = int(round((shape[1]/2) - (self.col/2)))

        for i in range(start_row, start_row+self.row):
            for j in range(start_col, start_col+self.col):
                mag_sampling_data[i][j] = self.mag_data[i][j]
                sampling_data[i][j] = self.data[i][j]

        return [mag_sampling_data, sampling_data]

    def get_undersampled(self):
        shape = np.shape(self.data)
        mag_sampling_data = np.zeros(shape)
        sampling_data = np.zeros(shape, dtype=complex)
        start_row = int(round((shape[0] / 2) - (self.row / 2)))
        start_col = int(round((shape[1] / 2) - (self.col / 2)))

        for i in range(start_row, start_row + self.row, 2):
            for j in range(start_col, start_col + self.col):
                mag_sampling_data[i][j] = self.mag_data[i][j]
                sampling_data[i][j] = self.data[i][j]

        return [mag_sampling_data, sampling_data]

    def get_sample(self):
        if self.trajectory == 0:
            return self.get_fully_sampled()
        else:
            return self.get_undersampled()
