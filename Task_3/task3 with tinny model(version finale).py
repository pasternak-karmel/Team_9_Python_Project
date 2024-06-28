from tkinter import *
from tkinter import ttk
import threading
from diffusers import StableDiffusionPipeline

# Initialiser le pipeline Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch")


# Configuration de la fenêtre principale
fenetre = Tk()
fenetre.geometry('500x500')
fenetre.title('Team 9')
fenetre['bg'] = '#1f2937'  
fenetre.resizable(height=False, width=False)

recent_request = []

def generator_function():
    prompt = user_request.get()
    image = pipe(prompt).images[0]
    image_path = str(prompt) + ".png"
    image.save(image_path)
    photo = PhotoImage(file=image_path)
    # Mettre à jour le label de l'image avec la nouvelle image
    image_label.config(image=photo)
    image_label.image = photo
    progress_bar.stop()
    progress_bar.pack_forget()

def start_loading():
    progress_bar.start(10)
    # Utiliser un thread pour charger l'image
    threading.Thread(target=generator_function).start()

label = Label(fenetre, text="Image Generator", bg="#374151", fg="white")
label.place(x="150", y="5")
description = Label(fenetre, text="Description", bg="#374151", fg="white")
description.place(y="100")
user_request = StringVar()
entre = Entry(fenetre, fg="black", textvariable=user_request, bg="#d1d5db")
entre.place(x="150", y="100")
lancer = Button(fenetre, text="Lancer", bg="#10b981", fg="white", command=start_loading) 
lancer.place(x="252", y="100")

# _barre de progression
progress_bar = ttk.Progressbar(fenetre, orient='horizontal', length=90, mode='indeterminate')
progress_bar.place(x="150", y="30")

# Affichage de l'image
image_label = Label(fenetre, bg="#d1d5db")
image_label.place(x="150", y="150")
quit_but = Button(fenetre, text="Quitter", bg="#ef4444", fg="white", command=fenetre.quit)
quit_but.place(x="352")
fenetre.mainloop()
