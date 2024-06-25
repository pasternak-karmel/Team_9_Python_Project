# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk
# from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
# import torch
# import threading
#
# model_id = "stabilityai/stable-diffusion-2"
# scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
# pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float16)
# pipe = pipe.to("cuda")
#
# def generate_image():
#     description = description_entry.get()
#     spinner.start()
#     threading.Thread(target=lambda: generate_and_display_image(description)).start()
#
# def generate_and_display_image(text):
#     with torch.autocast("cuda"):
#         image = pipe(text).images[0]
#     root.after(0, lambda: stop_spinner(image))
#
# def stop_spinner(image):
#     spinner.stop()
#     image = image.resize((400, 200))
#     img_tk = ImageTk.PhotoImage(image)
#     image_label.config(image=img_tk)
#     image_label.image = img_tk
#
# root = tk.Tk()
# root.title("Tkinter Application UI")
#
# description_label = tk.Label(root, text="Description:")
# description_label.grid(row=0, column=0, padx=10, pady=10)
#
# description_entry = tk.Entry(root, width=40)
# description_entry.grid(row=0, column=1, padx=10, pady=10)
#
# generate_button = tk.Button(root, text="Generate Image", command=generate_image)
# generate_button.grid(row=1, column=1, pady=10)
#
# spinner = ttk.Progressbar(root, mode='indeterminate')
# spinner.grid(row=1, column=2, padx=10, pady=10)
#
# image_label = tk.Label(root, text="Image Display Area", width=50, height=10, relief="solid")
# image_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
#
# root.mainloop()


import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from diffusers import StableDiffusionPipeline
# from transformers import pipeline
import torch
import threading
import subprocess
import sys
from accelerate import Accelerator

import matplotlib.pyplot as plt


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import numpy as np
except ImportError:
    install("numpy<2.0.0")
    import numpy as np

# model_id = "dreamlike-art/dreamlike-photoreal-2.0"
model_id = "hf-internal-testing/tiny-stable-diffusion-torch"
accelerator = Accelerator()
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
pipe = pipe.to(accelerator.device)

# prompt = "photo, a church in the middle of a field of crops, bright cinematic lighting, gopro, fisheye lens"
# image = pipe(prompt).images[0]
#
# image.save("./result.jpg")

root = tk.Tk()
root.geometry('600x600')
root.title('Team 9')
root.resizable(height=True, width=True)


def karmel():
    image.config(image='', text="Generating new image...")
    description = description_entry.get()
    spinner.start()
    threading.Thread(target=lambda: generate(description)).start()


def generate(text):
    # with torch.autocast(accelerator.device):
    with torch.autocast("cuda"):
        celui = pipe(text).images[0]
        plt.imshow(celui)
        plt.axis('off')
    root.after(0, lambda: stop_spinner(celui))


def stop_spinner(image):
    spinner.stop()
    image = image.resize((400, 400))
    img_tk = ImageTk.PhotoImage(image)
    image.config(image=img_tk, text='')
    # image.save("/image/"+description_entry.get()+".png")
    image.save(f"{description_entry.get()}.png")
    image.image = img_tk


description_label = tk.Label(root, text="Description:")
description_label.grid(row=0, column=0, padx=10, pady=10)

description_entry = tk.Entry(root, width=40)
description_entry.grid(row=0, column=1, padx=10, pady=10)

generate_button = tk.Button(root, text="Generate Image", command=karmel)
generate_button.grid(row=1, column=1, pady=10)

spinner = ttk.Progressbar(root, mode='indeterminate')
spinner.grid(row=1, column=2, padx=10, pady=10)

image = ttk.Label(root, text="gonna display here", width=50, relief="solid")
image.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
