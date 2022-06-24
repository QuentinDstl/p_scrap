from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("300x200")
window.configure(bg = "#FFFEFC")


canvas = Canvas(
    window,
    bg = "#FFFEFC",
    height = 200,
    width = 300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    75.0,
    100.0,
    image=image_image_1
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=171.0,
    y=97.0,
    width=109.0,
    height=20.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=170.0,
    y=68.0,
    width=113.0,
    height=20.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=170.0,
    y=20.0,
    width=110.0,
    height=40.0
)

canvas.create_text(
    14.0,
    8.0,
    anchor="nw",
    text="How to use it ?",
    fill="#FFFEFC",
    font=("Lato Bold", 15 * -1)
)

canvas.create_text(
    14.0,
    65.0,
    anchor="nw",
    text="Go to a webpage",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_text(
    14.0,
    119.0,
    anchor="nw",
    text="template exist it",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_text(
    14.0,
    137.0,
    anchor="nw",
    text="will be save, else",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_text(
    14.0,
    155.0,
    anchor="nw",
    text="add yourself a new",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_text(
    14.0,
    173.0,
    anchor="nw",
    text="one",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_text(
    14.0,
    29.0,
    anchor="nw",
    text="Go to the new",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_text(
    14.0,
    47.0,
    anchor="nw",
    text="opened browser",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_text(
    14.0,
    83.0,
    anchor="nw",
    text="and click on save",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_text(
    14.0,
    101.0,
    anchor="nw",
    text="Data, if a related",
    fill="#FFFEFC",
    font=("Lato", 15 * -1)
)

canvas.create_rectangle(
    160.0,
    130.0,
    290.0,
    190.0,
    fill="#D9D9D9",
    outline="")
window.resizable(False, False)
window.mainloop()
