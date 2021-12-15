import tkinter as tk
from tkinter.filedialog import askopenfile
from frequency_filtering.fft import FFT
from frequency_filtering.ifft import InverseFFT
from frequency_filtering.sampling import Sampling
from frequency_filtering.symmetry import ConjugateSymmetry
from frequency_filtering.acquire_image import AcquireImage
from PIL import Image, ImageTk
import numpy as np
import cv2

window = tk.Tk()
window.title('MRI reconstruction')
window.geometry('1000x720')
window.resizable(0,0)
window.config(bg='#dcdcdc')

left_frm = tk.Frame(window, width=280, height=710, bg='#f0f0f0')
left_frm.grid(row=0, column=0, padx=5, pady=5)
right_frm = tk.Frame(window, width=705, height=710, bg='#f0f0f0')
right_frm.grid(row=0, column=1, pady=5)

input_frm = tk.Frame(left_frm, width=270, height=210, bg='#fff')
input_frm.grid(row=0, column=0, padx=5, pady=5)
input_frm.grid_columnconfigure(0, weight=1)
input_frm.grid_propagate(0)

sampling_frm = tk.Frame(left_frm, highlightbackground='#000', highlightthickness=1)
sampling_frm.grid(row=1, column=0, padx=5, pady=(0, 5))
# sampling_frm.grid_columnconfigure(0, weight=1)
# sampling_frm.grid_propagate(0)

ac_frm = tk.Frame(left_frm)
ac_frm.grid(row=2, column=0, padx=5, pady=(0, 5))
# ac_frm.grid_columnconfigure(0, weight=1)
# ac_frm.grid_propagate(0)

fft0_frm = tk.Frame(right_frm, width=350, height=350, bg='#fff')
fft0_frm.grid(row=0, column=0, padx=(0, 5), pady=(0, 5))
fft0_frm.grid_columnconfigure(0, weight=1)
fft0_frm.grid_propagate(0)

fft1_frm = tk.Frame(right_frm, width=350, height=350, bg='#fff')
fft1_frm.grid(row=0, column=1, pady=(0, 5))
fft1_frm.grid_columnconfigure(0, weight=1)
fft1_frm.grid_propagate(0)

fft2_frm = tk.Frame(right_frm, width=350, height=350, bg='#fff')
fft2_frm.grid(row=1, column=0, padx=(0, 5))
fft2_frm.grid_columnconfigure(0, weight=1)
fft2_frm.grid_propagate(0)

fft3_frm = tk.Frame(right_frm, width=350, height=350, bg='#fff')
fft3_frm.grid(row=1, column=1)
fft3_frm.grid_columnconfigure(0, weight=1)
fft3_frm.grid_propagate(0)

file_path = ''
ac_trajectory = 0
row = 0
column = 0
half_fourier = 0

input_image = None
fft_data = None
sampling_data = None
ifft_image = None


def open_file():
    global file_path
    global input_image

    file = askopenfile(mode='r', filetypes=[('PNG Files', '*.png')])
    if file is not None:
        file_path = file.name
        input_image = cv2.imread(file_path, 0)

        array_to_image = Image.fromarray(input_image)
        array_to_image = array_to_image.resize((150, 150))
        image = ImageTk.PhotoImage(image=array_to_image)

        image_label = tk.Label(input_frm, image=image, bg='#fff')
        image_label.image = image
        image_label.grid(row=2, padx=5, pady=(0, 5))


def save_setting():
    global ac_trajectory
    global half_fourier
    global row
    global column

    ac_trajectory = v.get()
    half_fourier = s.get()
    if half_fourier == 0:
        row = int(input_row.get())
        column = int(input_col.get())


def get_fft():
    global input_image
    global fft_data
    global row
    global column

    image_name = "phantom"
    if input_image is not None:
        fft_obj = FFT(input_image, row, column)
        output = fft_obj.get_fft()
        fft_data = output

        array_to_image = Image.fromarray(output[0])
        array_to_image = array_to_image.resize((350, 350))
        image = ImageTk.PhotoImage(image=array_to_image)

        fft_image_name = 'output/' + image_name + "_kspace.jpg"
        cv2.imwrite(fft_image_name, output[0])

        image_label = tk.Label(fft0_frm, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0)


def acquire_sampling_data():
    global ac_trajectory
    global fft_data
    global sampling_data
    global half_fourier

    output = None
    image_name = "phantom"
    if fft_data is not None:
        if half_fourier == 0:
            sampling_obj = Sampling(fft_data, row, column, ac_trajectory)
            output = sampling_obj.get_sample()
        else:
            sampling_obj = ConjugateSymmetry(fft_data, half_fourier, ac_trajectory)
            output = sampling_obj.get_sample()

    if output is not None:
        sampling_data = output

        array_to_image = Image.fromarray(output[0])
        array_to_image = array_to_image.resize((350, 350))
        image = ImageTk.PhotoImage(image=array_to_image)

        sampling_image_name = 'output/' + image_name + "_sampling_kspace.jpg"
        cv2.imwrite(sampling_image_name, output[0])

        image_label = tk.Label(fft1_frm, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0)


def get_ifft():
    global sampling_data
    global ifft_image

    image_name = "phantom"
    if sampling_data is not None:
        inverse_obj = InverseFFT(sampling_data[1])
        output = inverse_obj.get_ifft()
        ifft_image = output

        array_to_image = Image.fromarray(output)
        array_to_image = array_to_image.resize((350, 350))
        image = ImageTk.PhotoImage(image=array_to_image)

        ifft_image_name = 'output/' + image_name + "_sampling_image.jpg"
        cv2.imwrite(ifft_image_name, output)

        image_label = tk.Label(fft2_frm, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0)


def reconstruct_image():
    global ac_trajectory
    global sampling_data
    global half_fourier

    output = None
    image_name = "phantom"
    if sampling_data is not None:
        reconstruct_obj = AcquireImage(sampling_data[1], half_fourier, row, column)
        output = reconstruct_obj.get_image()

    if output is not None:
        array_to_image = Image.fromarray(output)
        array_to_image = array_to_image.resize((350, 350))
        image = ImageTk.PhotoImage(image=array_to_image)

        sampling_image_name = 'output/' + image_name + "_reconstructed.jpg"
        cv2.imwrite(sampling_image_name, output)

        image_label = tk.Label(fft3_frm, image=image)
        image_label.image = image
        image_label.grid(row=0, column=0)


def accquisition():
    get_fft()
    acquire_sampling_data()
    get_ifft()
    reconstruct_image()


tk.Label(input_frm, text="Input Phantom", bg='#fff').grid(row=0, padx=5)
open_btn = tk.Button(input_frm, text='Choose File (PNG) ', command=lambda: open_file())
open_btn.grid(row=1, padx=5, pady=(0, 5))
temp_img = tk.Frame(input_frm, width=150, height=150, bg='#dcdcdc')
temp_img.grid(row=2, padx=5, pady=(0, 5))

v = tk.IntVar()
image = Image.open("img/fully_sampled.PNG")
image = image.resize((100, 100))
fully_sampled_img = ImageTk.PhotoImage(image)
image = Image.open("img/undersampled.PNG")
image = image.resize((100, 100))
undersampled_img = ImageTk.PhotoImage(image)

tk.Label(sampling_frm, text="Set Sampling Grid").grid(row=0, columnspan=2, pady=(10, 0))
R1 = tk.Radiobutton(sampling_frm, text="Fully Sampled", variable=v, value=0)
R1.grid(row=2, column=0, pady=(0, 5))
cartesian_img_label = tk.Label(sampling_frm, image=fully_sampled_img, width=100, height=100)
cartesian_img_label.image = fully_sampled_img
cartesian_img_label.grid(row=1, column=0, padx=(20, 10), pady=(10, 0))

R2 = tk.Radiobutton(sampling_frm, text="Undersampled", variable=v, value=1)
R2.grid(row=2, column=1, pady=(0, 5))
radial_img_label = tk.Label(sampling_frm, image=undersampled_img, width=100, height=100)
radial_img_label.image = undersampled_img
radial_img_label.grid(row=1, column=1, padx=(10, 20), pady=(10, 0))

s = tk.IntVar()
S0 = tk.Radiobutton(sampling_frm, text="Custom Sampling Grid", variable=s, value=0)
S0.grid(row=3, columnspan=2, pady=(5,0))
tk.Label(sampling_frm, text="# of lines ").grid(row=4, column=0, padx=10, pady=5)
input_row = tk.Entry(sampling_frm, width=15)
input_row.grid(row=4, column=1, padx=5, pady=5)
tk.Label(sampling_frm, text="# of points/line ").grid(row=5, column=0, padx=10, pady=5)
input_col = tk.Entry(sampling_frm, width=15)
input_col.grid(row=5, column=1, padx=5, pady=5)

S1 = tk.Radiobutton(sampling_frm, text="Top Half", variable=s, value=1)
S1.grid(row=6, column=0, pady=5)
S2 = tk.Radiobutton(sampling_frm, text="Bottom Half", variable=s, value=2)
S2.grid(row=6, column=1, pady=5)
S3 = tk.Radiobutton(sampling_frm, text="Right Half", variable=s, value=3)
S3.grid(row=7, column=0, pady=(0, 5))
S4 = tk.Radiobutton(sampling_frm, text="Left Half", variable=s, value=4)
S4.grid(row=7, column=1, pady=(0, 5))

save_btn = tk.Button(sampling_frm, text='Save Setting', command=lambda: save_setting())
save_btn.grid(row=8, columnspan=2 , padx=10, pady=10)

run_accquisition_btn = tk.Button(ac_frm, text='Start Accquisition', command=lambda: accquisition())
run_accquisition_btn.grid(row=0, padx=10, pady=10)

window.mainloop()
