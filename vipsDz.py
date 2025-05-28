import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import tkinterdnd2 as tkdnd
import webbrowser

class DzSaveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VIPS DZSaver")
        self.root.geometry("450x300")

        # Check if vips is installed
        if not self.check_vips_installed():
            self.show_install_message()
            return

        # Create a label to display messages
        self.label = tk.Label(root, text="Drag an image file to this text. You may upload additional images after this one has output dzi. You do not need to select a directory", width = 200, font=("Courier", 20), wraplength=380, justify="center")
        self.label.pack(pady=20) # pad up and down, pack instead of grid

        # Configure the drop area using tkdnd
        self.configure_drop_area()
        # Create a button to select the output directory
        self.output_dir = "dzi_output"  # Default output directory
        self.create_output_dir_button()
        self.create_default_dir_button()

    def configure_drop_area(self):
        self.root.drop_target_register(tkdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        file_paths = self.split_list(event.data)
        for file_path in file_paths:
            # Remove enclosing {} if they have them
            file_path = file_path.strip("{}")
            if os.path.isfile(file_path):
                self.execute_vips_dzsave(file_path)
            else:
                messagebox.showerror("Error", f"File not found: {file_path}")

    def split_list(self, data):
        # Split the data by newline characters (common in file paths from drag-and-drop)
        # Also remove file:// prefix
        return [path.replace("file://", "").strip("{}") for path in data.split()]

    def execute_vips_dzsave(self, file_path):
        # Define the output directory
        if not self.output_dir:
            messagebox.showwarning("Output Directory Not Set", "Please select an output directory first.")
            return

        base_name = os.path.basename(file_path).rsplit('.', 1)[0]
        output_name = os.path.join(self.output_dir, base_name)

        # Add VIPS bin directory to PATH (modify the path according to your VIPS installation)
        #############################################################
        vips_bin_path = r"C:\downloads\vips-w64\vips-dev-8.16\bin"  # Update this path to your VIPS bin directory 
        #############################################################
        env = os.environ.copy()
        env["PATH"] = vips_bin_path + ";" + env["PATH"]

        # Construct the vips dzsave command
        command = ["vips", "dzsave", file_path, output_name]

        # Run the command
        try:
            subprocess.run(command, check=True, env=env, creationflags=subprocess.CREATE_NO_WINDOW)
            messagebox.showinfo("Success", f"Processed {file_path} and saved to {output_name}.dzi")
            self.label.config(font=("Courier", 15))
            self.update_label(f"Processed {file_path} and saved to {output_name}.dzi")
            #self.root.after(3000, (self.update_label(f"You may upload additional files")))
            #self.root.after(3000, (self.update_label(f"2nd Processed {file_path} and saved to {output_name}.dzi")))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error executing vips dzsave command: {e}")
            self.update_label(f"Error processing {file_path}: {e}")

    def update_label(self, text):
        self.label.config(text=text, wraplength=380, justify="center")
    #check if vips installed using subprocess to run it before running
    def check_vips_installed(self):
        try:
            result = subprocess.run(["vips", "--version"], capture_output=True, text=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def show_install_message(self):
        message = (
            "VIPS is not installed on your system.\n\n"
            "Please visit the libvips website to download and install VIPS:\n\n"
            "<https://libvips.github.io/libvips/install.html>"
        )
        messagebox.showinfo("VIPS Not Installed", message)
        webbrowser.open("https://libvips.github.io/libvips/install.html")
        self.root.destroy()  # Close the application after showing the message
    #Output Dir Button
    def create_output_dir_button(self):
        self.select_dir_button = tk.Button(self.root, text="Select Output Directory", command=self.select_output_directory)
        self.select_dir_button.pack(padx=(90,0),side=tk.LEFT)
    #Output dir actual function
    def select_output_directory(self):
        selected_dir = filedialog.askdirectory(title="Select Output Directory")
        if selected_dir:
            self.output_dir = selected_dir
            messagebox.showinfo("Selected Directory", f"Output directory set to: {selected_dir}")
        else:
            messagebox.showwarning("No Directory Selected", "No output directory selected. Using default: 'dzi_output'")
            self.output_dir = "dzi_output"
    #Reset Button function and function that does reset of variable
    def create_default_dir_button(self):
        self.select_dir_button = tk.Button(self.root, text="Reset to Default Directory", command=self.reseter)
        self.select_dir_button.pack(side=tk.LEFT, padx=(10,0)) #gap it
    def reseter(self):
        self.output_dir = "dzi_output"
        message = ("The input directory has been reset to default")
        messagebox.showinfo("RESET", message)
        

def main():
    root = tkdnd.TkinterDnD.Tk()
    app = DzSaveApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
