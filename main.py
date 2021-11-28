import tkinter as tk
from tkinter.filedialog import askopenfile
from frequency_filtering.fft import Filtering
from PIL import Image, ImageTk
import numpy as np
import cv2

window = tk.Tk()
window.title('MRI reconstruction')
window.geometry('1280x720')
window.config(bg='#dcdcdc')

left_frm = tk.Frame(window, width=280, height=710, bg='#f0f0f0')
left_frm.grid(row=0, column=0, padx=5, pady=5)
right_frm = tk.Frame(window, width=985, height=710, bg='#f0f0f0')
right_frm.grid(row=0, column=1, pady=5)

input_frm = tk.Frame(left_frm, width=270, height=260, bg='#fff')
input_frm.grid(row=0, column=0, padx=5, pady=5)
input_frm.grid_columnconfigure(0, weight=1)
input_frm.grid_propagate(0)

sampling_frm = tk.Frame(left_frm, highlightbackground='#000', highlightthickness=1)
sampling_frm.grid(row=1, column=0, padx=5, pady=(0, 5))
sampling_frm.grid_columnconfigure(0, weight=1)
#sampling_frm.grid_propagate(0)

ac_frm = tk.Frame(left_frm, bg='#fff')
ac_frm.grid(row=2, column=0, padx=5, pady=(0, 5))
ac_frm.grid_columnconfigure(0, weight=1)
#ac_frm.grid_propagate(0)

fft0_frm = tk.Frame(right_frm, width=490, height=350, bg='#fff')
fft0_frm.grid(row=0, column=0, padx=(0, 5), pady=(0, 5))
fft0_frm.grid_columnconfigure(0, weight=1)
fft0_frm.grid_propagate(0)

fft1_frm = tk.Frame(right_frm, width=490, height=350, bg='#fff')
fft1_frm.grid(row=0, column=1, pady=(0, 5))

fft2_frm = tk.Frame(right_frm, width=490, height=350, bg='#fff')
fft2_frm.grid(row=1, column=0, padx=(0, 5))

fft3_frm = tk.Frame(right_frm, width=490, height=350, bg='#fff')
fft3_frm.grid(row=1, column=1)

file_path = ''


def open_file():
    global file_path
    file = askopenfile(mode='r', filetypes=[('PNG Files', '*.png')])
    if file is not None:
        file_path = file.name
        input_image = cv2.imread(file_path, 0)

        array_to_image = Image.fromarray(input_image)
        array_to_image = array_to_image.resize((200, 200))
        image = ImageTk.PhotoImage(image=array_to_image)

        image_label = tk.Label(input_frm, image=image, bg='#fff')
        image_label.image = image
        image_label.grid(row=2, padx=5, pady=(0, 5))


def process():
    global file_path
    image_name = "phantom"
    input_image = cv2.imread(file_path, 0)
    if input_image is not None:
        filter_obj = Filtering(input_image)
        output = filter_obj.filter()

        array_to_image = Image.fromarray(output)
        array_to_image = array_to_image.resize((350, 350))
        image = ImageTk.PhotoImage(image=array_to_image)

        # Write output file
        output_dir = 'output/'

        output_image_name = output_dir + image_name + "_dft.jpg"
        cv2.imwrite(output_image_name, output)

        image_label = tk.Label(fft0_frm, image=image)
        image_label.image = image
        image_label.grid()

    else:
        null_label = tk.Label(left_frm, text='No file selected.')
        null_label.grid(row=3, columnspan=2)


tk.Label(input_frm, text="Input Phantom", bg='#fff').grid(row=0, padx=5)
open_btn = tk.Button(input_frm, text='Choose File (PNG) ', command=lambda: open_file())
open_btn.grid(row=1, padx=5, pady=(0, 5))
temp_img = tk.Frame(input_frm, width=200, height=200, bg='#dcdcdc')
temp_img.grid(row=2, padx=5, pady=(0, 5))

ac_trajectory = tk.IntVar()
image = Image.open("img/cartesian.PNG")
image = image.resize((100, 100))
cartesian_img = ImageTk.PhotoImage(image)
image = Image.open("img/radial.PNG")
image = image.resize((100, 100))
radial_img = ImageTk.PhotoImage(image)

tk.Label(sampling_frm, text="Select Trajectory").grid(row=0, columnspan=2, pady=(10, 0))
R1 = tk.Radiobutton(sampling_frm, text="Cartesian", variable=ac_trajectory, value=1)
R1.grid(row=2, column=0, pady=(0, 5))
cartesian_img_label = tk.Label(sampling_frm, image=cartesian_img, width=100, height=100)
cartesian_img_label.image = cartesian_img
cartesian_img_label.grid(row=1, column=0, padx=(20, 10), pady=(10, 0))

R2 = tk.Radiobutton(sampling_frm, text="Radial", variable=ac_trajectory, value=2)
R2.grid(row=2, column=1, pady=(0, 5))
radial_img_label = tk.Label(sampling_frm, image=radial_img, width=100, height=100)
radial_img_label.image = radial_img
radial_img_label.grid(row=1, column=1, padx=(10, 20), pady=(10, 0))

run_fft_btn = tk.Button(ac_frm, text='Get FFT', command=lambda: process())
run_fft_btn.grid(row=0, padx=10, pady=10)

window.mainloop()