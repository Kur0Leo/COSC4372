import cv2
import numpy as np


class ConjugateSymmetry:
    def __init__(self, data, half_fourier, trajectory):
        self.mag_data = data[0]
        self.data = data[1]
        self.half_fourier = half_fourier
        self.trajectory = trajectory

    def phase_symmetry(self):
        shape = np.shape(self.data)
        mag_sampling_data = np.zeros(shape)
        sampling_data = np.zeros(shape, dtype=complex)

        if self.half_fourier == 1:
            if self.trajectory == 0:
                for i in range(0, shape[0] // 2):
                    for j in range(0, shape[1]):
                        mag_sampling_data[i][j] = self.mag_data[i][j]
                        sampling_data[i][j] = self.data[i][j]

                return [mag_sampling_data, sampling_data]
            else:
                for i in range(0, shape[0] // 2, 2):
                    for j in range(0, shape[1]):
                        mag_sampling_data[i][j] = self.mag_data[i][j]
                        sampling_data[i][j] = self.data[i][j]

                return [mag_sampling_data, sampling_data]
        else:
            if self.trajectory == 0:
                for i in range(shape[0] // 2, shape[0]):
                    for j in range(0, shape[1]):
                        mag_sampling_data[i][j] = self.mag_data[i][j]
                        sampling_data[i][j] = self.data[i][j]

                return [mag_sampling_data, sampling_data]
            else:
                for i in range(shape[0] // 2, shape[0], 2):
                    for j in range(0, shape[1]):
                        mag_sampling_data[i][j] = self.mag_data[i][j]
                        sampling_data[i][j] = self.data[i][j]

                return [mag_sampling_data, sampling_data]

    def read_symmetry(self):
        shape = np.shape(self.data)
        mag_sampling_data = np.zeros(shape)
        sampling_data = np.zeros(shape, dtype=complex)

        if self.half_fourier == 3:
            if self.trajectory == 1:
                for i in range(0, shape[0]):
                    for j in range(0, shape[1] // 2):
                        mag_sampling_data[i][j] = self.mag_data[i][j]
                        sampling_data[i][j] = self.data[i][j]

                return [mag_sampling_data, sampling_data]
            else:
                for i in range(0, shape[0]):
                    for j in range(0, shape[1] // 2, 2):
                        mag_sampling_data[i][j] = self.mag_data[i][j]
                        sampling_data[i][j] = self.data[i][j]

                return [mag_sampling_data, sampling_data]
        else:
            if self.trajectory == 1:
                for i in range(0, shape[0]):
                    for j in range(shape[1] // 2, shape[1]):
                        mag_sampling_data[i][j] = self.mag_data[i][j]
                        sampling_data[i][j] = self.data[i][j]

                return [mag_sampling_data, sampling_data]
            else:
                for i in range(0, shape[0]):
                    for j in range(shape[1] // 2, shape[1], 2):
                        mag_sampling_data[i][j] = self.mag_data[i][j]
                        sampling_data[i][j] = self.data[i][j]

                return [mag_sampling_data, sampling_data]

    def get_sample(self):
        if self.half_fourier == 1 or self.half_fourier == 2:
            return self.phase_symmetry()
        else:
            return self.read_symmetry()
