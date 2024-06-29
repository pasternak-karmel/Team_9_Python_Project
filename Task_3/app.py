import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import torch
import threading
import subprocess
import sys
from diffusers import StableDiffusionPipeline
from accelerate import Accelerator
import requests
import time
from io import BytesIO
import os

folder_path = 'image/'


def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import numpy as np
except ImportError:
    install("numpy<2.0.0")
    import numpy as np

model_id = "hf-internal-testing/tiny-stable-diffusion-torch"
accelerator = Accelerator()
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
pipe = pipe.to(accelerator.device)

API_TOKEN = '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'
model_id1 = "dreamlike-art/dreamlike-photoreal-2.0"
API_URL = "https://api-inference.huggingface.co/models/" + model_id1

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}


class SpinnerLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop_animation = True
        self.frames = [ImageTk.PhotoImage(frame.resize((40, 40))) for frame in
                       ImageSequence.Iterator(Image.open('spinner.webp'))]

    def start(self):
        self.stop_animation = False
        self._animate(0)

    def stop(self):
        self.stop_animation = True

    def _animate(self, frame_index):
        if not self.stop_animation:
            self.config(image=self.frames[frame_index])
            self.image = self.frames[frame_index]
            frame_index = (frame_index + 1) % len(self.frames)
            self.after(100, self._animate, frame_index)


root = tk.Tk()
root.geometry('800x700')
root.title('Team 9 - Image Generator')
root.resizable(height=True, width=True)


# Function to generate image using Stable Diffusion
def generate_stable_diffusion(text):
    with torch.autocast("cuda"):
        generated_image = pipe(text).images[0]
        return generated_image


def generate_api_image(prompt, retries=2, delay=10):
    data = {"inputs": prompt}
    while retries > 0:
        try:
            response = requests.post(API_URL, headers=headers, json=data)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                return image
            elif response.status_code == 503:
                raise Exception("Service Unavailable (503)")
            else:
                raise Exception(f"Image generation error: {response.status_code}")
        except Exception as e:
            retries -= 1
            if retries > 0:
                messagebox.showwarning("Error", f"{str(e)}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise e


def generate_image():
    image_label.config(image='', text="Generating new image...")
    description = description_entry.get()
    generate_button.config(state=tk.DISABLED)
    spinner.start()
    threading.Thread(target=lambda: process_image_generation(description)).start()


# Function to process image generation and display the result
def process_image_generation(prompt):
    try:
        if use_stable_diffusion.get():
            generated_image = generate_stable_diffusion(prompt)
        else:
            generated_image = generate_api_image(prompt)
        display_generated_image(generated_image)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate image: {str(e)}")
        spinner.stop()
        generate_button.config(state=tk.NORMAL)


def display_generated_image(generated_image):
    folder_path = 'image/'
    spinner.stop()
    generated_image = generated_image.resize((400, 400))
    img_tk = ImageTk.PhotoImage(generated_image)
    image_label.config(image=img_tk, text='')
    image_filename = description_entry.get().strip()
    if not image_filename:
        image_filename = "generated_image"

    if not folder_path.endswith('/'):
        folder_path += '/'

    ensure_folder_exists(folder_path)

    image_path = folder_path + image_filename + ".png"
    generated_image.save(image_path)
    # generated_image.save(f"{description_entry.get()}.png")
    image_label.image = img_tk
    generate_button.config(state=tk.NORMAL)


description_label = ttk.Label(root, text="Description:")
description_label.grid(row=0, column=0, padx=10, pady=10)

description_entry = ttk.Entry(root, width=40)
description_entry.grid(row=0, column=1, padx=10, pady=10)

use_stable_diffusion = tk.BooleanVar(value=True)
stable_diffusion_radio = ttk.Radiobutton(root, text="Use Stable Diffusion", variable=use_stable_diffusion, value=True)
api_radio = ttk.Radiobutton(root, text="Use API", variable=use_stable_diffusion, value=False)
stable_diffusion_radio.grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)
api_radio.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)

generate_button = ttk.Button(root, text="Generate Image", command=generate_image)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

spinner = SpinnerLabel(root)
spinner.grid(row=2, column=2, padx=10, pady=10)

image_label = ttk.Label(root, text="Image will be displayed here", width=50, relief="solid")
image_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
