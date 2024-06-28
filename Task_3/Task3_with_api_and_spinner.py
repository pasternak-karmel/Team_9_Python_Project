import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import requests
import threading
import time
from io import BytesIO

# Définir le token API et l'URL du modèle
API_TOKEN = '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'
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# En-têtes de la requête
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Fonction pour envoyer la requête à l'API et obtenir l'image
def generate_image(prompt, result_label, spinner_label, retries=2, delay=10):
    data = {
        "inputs": prompt
    }

    while retries > 0:
        try:
            # Envoyer la requête POST à l'API
            response = requests.post(API_URL, headers=headers, json=data)

            if response.status_code == 200:
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                image = image.resize((500, 500))
                image_tk = ImageTk.PhotoImage(image)
                result_label.config(image=image_tk)
                result_label.image = image_tk  
                spinner_label.stop_animation = True
                spinner_label.config(image='')  
                messagebox.showinfo("Succès", "Image générée avec succès!")

                return
            elif response.status_code == 503:
                raise Exception("Service Indisponible (503)")
            else:
                raise Exception(f"Erreur de génération d'image : {response.status_code}")

        except Exception as e:
            retries -= 1
            if retries > 0:
                messagebox.showwarning("Erreur", f"{str(e)}. Réessai dans {delay} secondes...")
                time.sleep(delay)
            else:
                spinner_label.stop_animation = True
                spinner_label.config(image='')  
                messagebox.showerror("Erreur", f"Échec de la génération d'image après plusieurs tentatives : {str(e)}")               
                return

# Fonction pour démarrer la génération d'image
def start_generation(prompt, result_label, spinner_label):
    spinner_label.stop_animation = False
    threading.Thread(target=generate_image, args=(prompt, result_label, spinner_label)).start()
    animate_spinner(spinner_label)

# Fonction pour animer le spinner
def animate_spinner(spinner_label):
    frames = ImageSequence.Iterator(Image.open('spinner.webp'))
    frames = [ImageTk.PhotoImage(frame.resize((40,40))) for frame in frames]

    def update_frame(frame_index):
        if not spinner_label.stop_animation:
            spinner_label.config(image=frames[frame_index])
            spinner_label.image = frames[frame_index]  
            frame_index = (frame_index + 1) % len(frames)
            spinner_label.after(100, update_frame, frame_index)

    update_frame(0)

# Création de l'interface Tkinter
root = tk.Tk()
root.geometry("700x650")
root.resizable(False, False)
root.title("Génération d'image")

prompt_label = tk.Label(root, text="Entrez votre prompt:")
prompt_label.place(x=45, y=15)

prompt_entry = tk.Entry(root, width=50)
prompt_entry.place(x=200, y=10, height=25)

spinner_label = tk.Label(root)
spinner_label.place(x=450, y=45)

result_label = tk.Label(root)
result_label.place(x=100, y=90)

generate_button = tk.Button(root, text="Générer l'image", command=lambda: start_generation(prompt_entry.get(), result_label, spinner_label))
generate_button.place(x=150, y=50)

root.mainloop()
