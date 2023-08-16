'''I made this script to facilitate my gameplay in games of the clicker genre.
Line 96 to line 101 is for the code to work correctly, 
because I couldn't find another way to work correctly after the user pressed a key'''
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyautogui
from pynput import keyboard

class KeyConfigApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Key Configuration")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 450
        window_height = 450
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="gray10")

        self.style = ttk.Style()
        self.style.theme_create("custom_style", settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": "#1A1A1A",
                    "fieldbackground": "#1A1A1A",
                    "foreground": "white",
                    "selectforeground": "white",
                }
            },
            "TCombobox.dropdown": {
                "configure": {
                    "background": "#1A1A1A",
                    "foreground": "white",
                }
            },
            "TCombobox.Listbox": {
                "configure": {
                    "background": "#1A1A1A",
                    "foreground": "white",
                    "selectbackground": "gray",
                    "selectforeground": "white",
                }
            },
            "TCombobox.padding": {
                "configure": {
                    "padding": 6,
                }
            },
            "Vertical.TScrollbar": {
                "configure": {
                    "troughcolor": "gray",
                    "bordercolor": "gray",
                    "darkcolor": "gray",
                    "lightcolor": "gray",
                    "arrowcolor": "white",
                    "arrowbackground": "gray",
                },
                "map": {
                    "background": [("active", "gray30"), ("!active", "gray20")],
                    "troughcolor": [("active", "gray50"), ("!active", "gray")],
                    "bordercolor": [("active", "gray30"), ("!active", "gray")],
                    "darkcolor": [("active", "gray30"), ("!active", "gray")],
                    "lightcolor": [("active", "gray30"), ("!active", "gray")],
                    "arrowcolor": [("active", "white"), ("!active", "white")],
                    "arrowbackground": [("active", "gray30"), ("!active", "gray30")]
                }
            }
        })
        self.style.theme_use("custom_style")

        self.message_label = tk.Label(self.root, text="", bg="gray10", fg="white", font=("Helvetica", 14))
        self.message_label.pack(pady=20)

        self.activate_key = None
        self.deactivate_key = None
        self.active_function = False
        self.autoclick_job = None

        self.activate_button = tk.Button(self.root, text="Set key to ACTIVATE the script", command=self.set_activate_key, bg="#8B0000", fg="white", font=("Helvetica", 12))
        self.activate_button.pack(pady=10)

        self.deactivate_button = tk.Button(self.root, text="Set key to DEACTIVATE the script", command=self.set_deactivate_key, bg="#8B0000", fg="white", font=("Helvetica", 12))
        self.deactivate_button.pack(pady=10)

        self.label = tk.Label(self.root, text="Choose the click delay:", bg="gray10", fg="white", font=("Helvetica", 16))
        self.label.pack(pady=20)
        self.delay_options = [100, 200, 300, 400, 500, 1000]
        self.delay_ms = tk.IntVar(self.root)
        self.delay_ms.set(self.delay_options[0])
        self.delay_dropdown = ttk.Combobox(self.root, textvariable=self.delay_ms, values=self.delay_options)
        self.delay_dropdown.config(font=("Helvetica", 14))
        self.delay_dropdown.pack(pady=10)

        self.op = ['Click here when configuration is complete']
        self.de = tk.StringVar(self.root)
        self.de.set(self.op[0])
        self.de_drop = ttk.Combobox(self.root, textvariable=self.de, values=self.op)
        self.de_drop.config(font=("Helvetica", 14), width=35)
        self.de_drop.pack(pady=10)
      
        self.listener = None

    def on_key_press(self, key):
        try:
            pressed_key = key.char.upper()
        except AttributeError:
            return self.show_message_box('Please press a key with a character, keys like "ctrl", "shift" do not work')
        
        if pressed_key == self.activate_key:
            self.start_autoclick()
        elif pressed_key == self.deactivate_key:
            self.stop_autoclick()

    def check_key(self, event):
        pressed_key = event.keysym.upper()
        if pressed_key == self.activate_key:
            self.start_autoclick()
        elif pressed_key == self.deactivate_key:
            self.stop_autoclick()

    def start_autoclick(self):
        if not self.active_function:
            self.active_function = True
            self.message_label.config(text="Autoclick enabled", fg="white")
            self.autoclick()

    def autoclick(self):
        if self.active_function:
            delay = self.delay_ms.get()
            pyautogui.click()
            self.autoclick_job = self.root.after(delay, self.autoclick)

    def stop_autoclick(self):
        if self.autoclick_job is not None:
            self.root.after_cancel(self.autoclick_job)
            self.autoclick_job = None
        self.active_function = False
        self.message_label.config(text="Autoclick disabled", fg="white")

    def set_activate_key(self):
        self.configuring_activate = False
        self.message_label.config(text="Which key should I use to ACTIVATE the script?", fg="white")
        self.root.bind("<KeyPress>", self.listen_activate_key)

    def set_deactivate_key(self):
        self.configuring_activate = True
        self.message_label.config(text="Which key should I use to DEACTIVATE the script?", fg="white")
        self.root.bind("<KeyPress>", self.listen_deactivate_key)

    def listen_activate_key(self, event):
        pressed_key = event.keysym.upper()
        self.activate_key = pressed_key
        self.activate_button.config(text="Set key to ACTIVATE the function")
        self.show_message_box("Key to activate the script set successfully!")
        self.root.unbind("<KeyPress>")
        self.root.bind("<KeyPress>", self.check_key)

        if not self.listener:
            self.listener = keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()

    def listen_deactivate_key(self, event):
        pressed_key = event.keysym.upper()
        self.deactivate_key = pressed_key
        self.deactivate_button.config(text="Set key to DEACTIVATE the function")
        self.show_message_box("Key to deactivate the script set successfully!")
        self.root.unbind("<KeyPress>")
        self.root.bind("<KeyPress>", self.check_key)

        if not self.listener:
            self.listener = keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()

    def show_message_box(self, message):
        messagebox.showinfo("Message", message)

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KeyConfigApp()
    app.start()
