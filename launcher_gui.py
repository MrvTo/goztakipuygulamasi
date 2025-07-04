import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
import subprocess
import threading
import os
import sys
from tkinter import messagebox
from PIL import Image, ImageTk

base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, 'logo.png')

app = tb.Window(themename="superhero")
app.title("Göz Takip Uygulaması")
app.geometry("1024x480")
app.resizable(False, False)

g_process = None
vj_process = None
log_visible = False

# Logo yükleme
try:
    img = Image.open(logo_path)
    img = img.resize((469, 135))
    img_tk = ImageTk.PhotoImage(img)
    logo_label = tb.Label(app, image=img_tk)
    logo_label.image = img_tk
    logo_label.place(x=10, y=10)
except Exception as e:
    print(f"Logo yüklenemedi: {e}")

# Log alanı
log_frame = tb.Frame(app)

log_text_eye = ScrolledText(log_frame, height=10, width=48, autohide=True, bootstyle="dark")
log_text_eye.grid(row=0, column=0, padx=5, pady=5)
eye_label = tb.Label(log_frame, text="👁 Eye Tracking Log", bootstyle="secondary")
eye_label.grid(row=1, column=0)

log_text_vjoy = ScrolledText(log_frame, height=10, width=48, autohide=True, bootstyle="dark")
log_text_vjoy.grid(row=0, column=1, padx=5, pady=5)
vjoy_label = tb.Label(log_frame, text="🎮 vJoy Log", bootstyle="secondary")
vjoy_label.grid(row=1, column=1)

# logda çıkacak herhangi bi hatayı renklendirme
log_text_eye.tag_config("error", foreground="red")
log_text_vjoy.tag_config("error", foreground="red")

def log_eye(message):
    if "error" in message.lower():
        log_text_eye.insert("end", message + "\n", "error")
    else:
        log_text_eye.insert("end", message + "\n")
    log_text_eye.see("end")

def log_vjoy(message):
    if "error" in message.lower():
        log_text_vjoy.insert("end", message + "\n", "error")
    else:
        log_text_vjoy.insert("end", message + "\n")
    log_text_vjoy.see("end")

def toggle_log_visibility():
    global log_visible
    if log_visible:
        log_frame.place_forget()
        btn_toggle_log.config(text="Ayrıntıları Göster")
    else:
        log_frame.place(x=200, y=270)
        btn_toggle_log.config(text="Ayrıntıları Gizle")
    log_visible = not log_visible

def read_gonderici_output():
    for line in g_process.stdout:
        if line.strip():
            app.after(0, log_eye, line.strip())

def read_vjoy_output():
    for line in vj_process.stdout:
        if line.strip():
            app.after(0, log_vjoy, line.strip())

def start_eyetracking():
    global g_process
    if g_process is not None:
        messagebox.showinfo("Bilgi", "Eye Tracking zaten çalışıyor.")
        return
    gonderici_path = os.path.join(base_dir, 'gonderici.py')
    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    g_process = subprocess.Popen(
        ['python', gonderici_path],
        cwd=base_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=creationflags
    )
    btn_eye.config(state="disabled", text="Başlatıldı ✔️")
    threading.Thread(target=read_gonderici_output, daemon=True).start()

def start_vjoy():
    global vj_process
    if vj_process is not None:
        messagebox.showinfo("Bilgi", "vJoy zaten çalışıyor.")
        return
    vjoy_path = os.path.join(base_dir, 'vjoy_kontrol.py')
    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    vj_process = subprocess.Popen(
        ['python', vjoy_path],
        cwd=base_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=creationflags
    )
    btn_vjoy.config(state="disabled", text="Başlatıldı ✔️")
    threading.Thread(target=read_vjoy_output, daemon=True).start()

def clear_logs():
    log_text_eye.delete('1.0', 'end')
    log_text_vjoy.delete('1.0', 'end')

def on_close():
    if g_process:
        g_process.terminate()
    if vj_process:
        vj_process.terminate()
    app.destroy()

# Butonlar
btn_eye = tb.Button(app, text="👁 Eye Tracking Başlat", width=25, bootstyle="success", command=start_eyetracking)
btn_eye.place(x=50, y=150)
btn_eye.tooltip = "Göz takip sürecini başlatır"

btn_vjoy = tb.Button(app, text="🎮 vJoy Başlat", width=25, bootstyle="info", command=start_vjoy)
btn_vjoy.place(x=50, y=190)
btn_vjoy.tooltip = "vJoy kontrol sürecini başlatır"

btn_toggle_log = tb.Button(app, text="Ayrıntıları Göster", width=20, bootstyle="secondary", command=toggle_log_visibility)
btn_toggle_log.place(x=850, y=430)

btn_clear_logs = tb.Button(app, text="Logu Temizle", width=20, bootstyle="warning", command=clear_logs)
btn_clear_logs.place(x=720, y=430)

app.protocol("WM_DELETE_WINDOW", on_close)

app.mainloop()
