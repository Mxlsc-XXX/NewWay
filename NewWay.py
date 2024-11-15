import customtkinter as ctk
from PIL import Image, ImageTk
import os
import subprocess

def load_gif(filename, size):
    img = Image.open(filename)
    frames = []
    for _ in range(img.n_frames):
        img.seek(_)
        frame = img.copy().convert("RGBA").resize(size, Image.LANCZOS)
        frames.append(ImageTk.PhotoImage(frame))
    return frames

def animate_gif(label, frames, delay=100):
    def update_frame(frame_index):
        label.configure(image=frames[frame_index])
        frame_index = (frame_index + 1) % len(frames)
        label.after(delay, update_frame, frame_index)

    update_frame(0)

def setup_interface():
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")  

    root = ctk.CTk()
    root.title("NewWay Optimizer")
    root.geometry("850x430")
    root.resizable(False, False)
    return root

def create_background(root):
    background_image = Image.open("bg.jpg")  
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    background_image = background_image.resize((screen_width, screen_height), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)

    canvas = ctk.CTkCanvas(root, width=screen_width, height=screen_height)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=background_photo)

    canvas.background_photo = background_photo
    return canvas

def create_text_frame(canvas):
    frame1 = ctk.CTkFrame(master=canvas, width=150, height=430, fg_color="#9900cc", border_color="white", border_width=2, corner_radius=0)
    frame1.pack()
    frame1.pack_propagate(False)
    frame1.place(x=0, y=0)

    text = "🅝🅔🅦🅦🅐🅨"
    for char in text:
        label = ctk.CTkLabel(frame1, text=char, text_color="white", font=("Arial", 40))
        label.pack(pady=5)

    return frame1

def create_buttons(pad, output):
    commands = [
        ("Limpar memória ram", "ram.cmd"),
        ("Limpar cache", "cache.cmd"),
        ("Otimizar processos", "proc.cmd"),
        ("Otimizar CPU", "cpu.cmd"),
        ("Desativa transparência", "trans.cmd"),
        ("Desativa prefetch", "pref.cmd"),
        ("Desativa impressão", "impress.cmd"),
        ("Desativa recentes", "recent.cmd")
    ]

    for i, (text, cmd) in enumerate(commands):
        button = ctk.CTkButton(master=pad, text=text, bg_color="transparent", fg_color="pink",
                                command=lambda cmd=cmd: execute_command(cmd, output), text_color="black",
                                corner_radius=0, border_color="white", border_width=2,
                                border_spacing=1, hover_color="#df80ff")
        button.place(x=25 if i % 2 == 0 else 235, y=25 + (i // 2) * 50)


def execute_command(cmd, output):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        output.configure(state="normal")  
        output.insert("end", f"Comando: {cmd}\nSaída:\n{result.stdout}\nErros:\n{result.stderr}\n")
        output.configure(state="disabled")  
    except Exception as e:
        output.configure(state="normal")
        output.insert("end", f"Erro ao executar {cmd}: {str(e)}\n")
        output.configure(state="disabled")

def create_image_buttons(frame1):
    git_path = "git.jpg"
    git = Image.open(git_path)
    image = git.resize((40, 40), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    buttons_info = [
        ("", "github.cmd", photo, 25, 380),
        ("$", "donate.cmd", None, 85, 380)
    ]

    for text, cmd, img, x, y in buttons_info:
        button = ctk.CTkButton(master=frame1, text=text, image=img, bg_color="transparent", 
                                fg_color="#df80ff", command=lambda cmd=cmd: os.system(cmd), 
                                text_color="black", corner_radius=0, border_color="white", 
                                border_width=2, border_spacing=1, hover_color="purple", 
                                width=40 if text else 20, height=40 if text else 20)
        button.place(x=x, y=y)

def main():
    root = setup_interface()
    canvas = create_background(root)
    frame1 = create_text_frame(canvas)

    pad_width = 400
    pad_height = 300
    pad = ctk.CTkFrame(master=root, width=pad_width, height=pad_height, fg_color="transparent", border_width=0, corner_radius=0)
    pad.pack_propagate(False)
    pad.place(x=225, y=65)

    gif_path = os.path.join("sky.gif")
    gif_frames = load_gif(gif_path, (pad_width, pad_height))
    label_background = ctk.CTkLabel(pad, image=gif_frames[0], width=pad_width, height=pad_height, text="")
    label_background.place(relx=0, rely=0, anchor='nw')
    animate_gif(label_background, gif_frames)

    output = ctk.CTkTextbox(master=canvas, width=150, height=430, corner_radius=0, border_color="white", border_width=2, fg_color="black")
    output.configure(state="disabled")
    output.place(x=700)

    create_buttons(pad, output)
    create_image_buttons(frame1)

    root.mainloop()

if __name__ == "__main__":
    main()