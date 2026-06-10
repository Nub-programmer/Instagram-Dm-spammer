import tkinter as tk
from tkinter import ttk
import threading
from automation import start_automation

stop_event = threading.Event()

def launch_gui():
    root = tk.Tk()
    root.title("Instabot Spammer Control Dashboard")
    root.geometry("600x670")
    root.configure(bg="#121212")
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#121212", foreground="#FFFFFF", font=("Helvetica", 10, "bold"))
    style.configure("TButton", background="#1DB954", foreground="#FFFFFF", font=("Helvetica", 10, "bold"), borderwidth=0)
    style.map("TButton", background=[("active", "#1aa34a")], foreground=[("disabled", "#777777")])
    style.configure("Stop.TButton", background="#E11D48", foreground="#FFFFFF")
    style.map("Stop.TButton", background=[("active", "#be123c")])

    title_lbl = tk.Label(root, text="INSTABOT SPAMMER SYSTEM", bg="#121212", fg="#1DB954", font=("Helvetica", 16, "bold"))
    title_lbl.pack(pady=20)

    fields = ["Username", "Password", "Chat URL", "Message", "Interval (seconds)"]
    entries = {}
    
    frame = tk.Frame(root, bg="#121212")
    frame.pack(fill="x", padx=40)
    
    for field in fields:
        lbl = ttk.Label(frame, text=field + ":")
        lbl.pack(pady=4, anchor="w")
        
        if field == "Password":
            entry = tk.Entry(frame, show="*", bg="#1E1E1E", fg="#FFFFFF", insertbackground="#FFFFFF", bd=0, relief="flat", font=("Helvetica", 11))
        else:
            entry = tk.Entry(frame, bg="#1E1E1E", fg="#FFFFFF", insertbackground="#FFFFFF", bd=0, relief="flat", font=("Helvetica", 11))
            
        entry.pack(fill="x", ipady=6, pady=2)
        entries[field] = entry
        
    entries["Interval (seconds)"].insert(0, "30")
    
    log_box = tk.Text(root, height=12, bg="#1E1E1E", fg="#00FF66", insertbackground="#FFFFFF", font=("Courier", 10), bd=0, highlightthickness=1, highlightbackground="#2A2A2A")
    log_box.pack(fill="both", padx=40, pady=20, expand=True)
    
    def append_log(text):
        log_box.config(state="normal")
        log_box.insert(tk.END, text + "\n")
        log_box.see(tk.END)
        log_box.config(state="disabled")

    def on_start():
        stop_event.clear()
        btn_start.config(state="disabled")
        btn_stop.config(state="normal")
        
        username = entries["Username"].get()
        password = entries["Password"].get()
        chat_url = entries["Chat URL"].get()
        message = entries["Message"].get()
        try:
            interval = float(entries["Interval (seconds)"].get())
        except ValueError:
            interval = 30.0
        
        def runtime_wrapper():
            start_automation(username, password, chat_url, message, interval, stop_event, append_log)
            btn_start.config(state="normal")
            btn_stop.config(state="disabled")
            
        t = threading.Thread(target=runtime_wrapper, daemon=True)
        t.start()
        append_log("[SYSTEM] Active deployment initialization requested...")

    def on_stop():
        stop_event.set()
        append_log("[SYSTEM] Halt flag activated! Signaling browser window closure...")
        btn_stop.config(state="disabled")

    btn_frame = tk.Frame(root, bg="#121212")
    btn_frame.pack(pady=10)

    btn_start = ttk.Button(btn_frame, text="LAUNCH RUNTIME", command=on_start, width=20)
    btn_start.grid(row=0, column=0, padx=12, ipady=5)

    btn_stop = ttk.Button(btn_frame, text="STOP SPAMMER", style="Stop.TButton", command=on_stop, width=20)
    btn_stop.grid(row=0, column=1, padx=12, ipady=5)
    btn_stop.config(state="disabled")
    
    root.mainloop()
