import tkinter as tk
import json
import threading
import itertools
import time
from tkinter import filedialog, scrolledtext, messagebox

from pipelineDescriptionCreator import create_pipeline_description
from pipelineDesignCreator import create_design2

# === GLOBAL STATE ===
spinner_running = False

# === GUI SETUP ===
root = tk.Tk()
root.title("Apache Hop Pipeline Creator")
root.geometry("1000x740")

# === Output Directory Selection ===
def browse_directory():
    path = filedialog.askdirectory()
    if path:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, path)

tk.Label(root, text="Pipelines Output Directory:").pack(anchor="w", padx=10, pady=(10, 0))
dir_frame = tk.Frame(root)
dir_frame.pack(fill="x", padx=10)
dir_entry = tk.Entry(dir_frame)
dir_entry.pack(side="left", fill="x", expand=True)
tk.Button(dir_frame, text="Browse", command=browse_directory).pack(side="right")

# === Pipeline Name Entry ===
tk.Label(root, text="Pipeline Name:").pack(anchor="w", padx=10, pady=(10, 0))
pipeline_name_entry = tk.Entry(root)
pipeline_name_entry.pack(fill="x", padx=10)

# === Prompt Input ===
tk.Label(root, text="Enter What You Want:").pack(anchor="w", padx=10, pady=(10, 0))
prompt_text = scrolledtext.ScrolledText(root, height=5)
prompt_text.pack(fill="both", expand=False, padx=10)

# === Response Output ===
tk.Label(root, text="Pipeline Design Description:").pack(anchor="w", padx=10, pady=(10, 0))
response_text = scrolledtext.ScrolledText(root, height=10)
response_text.pack(fill="both", expand=True, padx=10)

# === Editable Used Plugins ===
tk.Label(root, text="Used Plugins (comma-separated):").pack(anchor="w", padx=10, pady=(10, 0))
plugins_text = scrolledtext.ScrolledText(root, height=3)
plugins_text.pack(fill="both", expand=False, padx=10)

# === Spinner Label ===
spinner_label = tk.Label(root, text="", font=("Arial", 24))
spinner_label.pack(pady=(5, 10))

# === Spinner Functions ===
def start_spinner():
    global spinner_running
    spinner_running = True
    threading.Thread(target=spin, daemon=True).start()

def stop_spinner():
    global spinner_running
    spinner_running = False
    spinner_label.config(text="")

def spin():
    for frame in itertools.cycle(["⏳", "🔄", "🔃"]):
        if not spinner_running:
            break
        spinner_label.config(text=frame)
        time.sleep(0.2)

# === BACKEND UTILS ===
def strip_code_fences(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()
    if text.endswith("```"):
        text = text[:-len("```")].strip()
    return text

# === Task Threads ===
def generate_prompt_thread(prompt):
    try:
        design = create_pipeline_description(prompt)
        design = strip_code_fences(design)
        data = json.loads(design)

        description = data['description']
        used_plugins = data['used_plugins']

        def update_ui():
            response_text.delete("1.0", tk.END)
            response_text.insert(tk.END, description)
            plugins_text.delete("1.0", tk.END)
            plugins_text.insert(tk.END, ", ".join(used_plugins))
            stop_spinner()

        root.after(0, update_ui)

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", str(e)))
        root.after(0, stop_spinner)

def submit_pipeline_thread(prompt, final_answer, used_plugins, output_dir, pipeline_name):
    try:
        create_design2(prompt, output_dir, final_answer, used_plugins, pipeline_name)
        print("Final Answer Submitted:", final_answer)
        print("Output Directory:", output_dir)
        print("Pipeline Name:", pipeline_name)
        print("Used Plugins:", used_plugins)

        root.after(0, lambda: messagebox.showinfo("Submitted", f"Pipeline '{pipeline_name}' submitted successfully."))
        root.after(0, stop_spinner)

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", str(e)))
        root.after(0, stop_spinner)

# === Generate Button Logic ===
def handle_prompt():
    prompt = prompt_text.get("1.0", tk.END).strip()
    if not prompt:
        messagebox.showerror("Error", "Prompt cannot be empty.")
        return
    start_spinner()
    threading.Thread(target=generate_prompt_thread, args=(prompt,), daemon=True).start()

tk.Button(root, text="Generate Pipeline Design Description", command=handle_prompt).pack(pady=10)

# === Submit Button Logic ===
def handle_submit():
    global used_plugins

    prompt = prompt_text.get("1.0", tk.END).strip()
    final_answer = response_text.get("1.0", tk.END).strip()
    output_dir = dir_entry.get().strip()
    pipeline_name = pipeline_name_entry.get().strip()
    plugins_input = plugins_text.get("1.0", tk.END).strip()

    if not final_answer:
        messagebox.showerror("Error", "Answer cannot be empty.")
        return
    if not output_dir:
        messagebox.showerror("Error", "Please select an output directory.")
        return
    if not pipeline_name:
        messagebox.showerror("Error", "Please enter a pipeline name.")
        return

    # Convert comma-separated plugin string to list
    used_plugins = [item.strip() for item in plugins_input.split(",") if item.strip()]

    start_spinner()
    threading.Thread(target=submit_pipeline_thread, args=(prompt, final_answer, used_plugins, output_dir, pipeline_name), daemon=True).start()

tk.Button(root, text="Create Pipeline XML", command=handle_submit).pack(pady=(0, 20))

# === Run App ===
root.mainloop()
