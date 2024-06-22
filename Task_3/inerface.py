
from tkinter import *

from diffusers import StableDiffusionPipeline
pipe =StableDiffusionPipeline.from_pretrained("hf-internal-testing/tiny-stable-diffusion-torch")
fenetre=Tk()
fenetre.geometry('400x400')
fenetre.title('Team 9')
fenetre['bg']='blue'
fenetre.resizable(height=False,width=False)


def generator_function():
    prompt=user_request.get()
    print(str(prompt))
    prompt = "a photo of an astronaut riding a horse on mars"
    image = pipe(prompt).images[0]
    image.save("astronaut_rides_horse.png")


label=Label(fenetre,text="Image Generator",bg="white")
label.place(x="150",y="5")
description=Label(fenetre,text="Description",bg="white")
description.place(y="100")
user_request=StringVar()
entre=Entry(fenetre,fg="black",textvariable=user_request)
entre.place(x="150",y="100")
lancer=Button(text="Lancer",bg="green",command=generator_function)
lancer.place(x="252",y="100")
quit_but=Button(text="Quitter",bg="red",command=fenetre.quit)
quit_but.place(x="352")
fenetre.mainloop()
