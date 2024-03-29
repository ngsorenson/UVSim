import tkinter as tk
from tkinter import filedialog, Toplevel
import uvsim

class GUI:
    def __init__(self, root):
        self.uv_sim = uvsim.UVSim("gui")

        self.root = root
        self.root.title("UVSim")

        self.title_label = tk.Label(self.root, text="Log")
        self.title_label.pack()

        self.io_frame = tk.Frame(self.root)
        self.io_frame.pack(expand=True, fill=tk.BOTH)

        self.io_field = tk.Text(self.io_frame, wrap="none", height=10, width=40)
        self.io_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.io_frame, command=self.io_field.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.io_field.config(yscrollcommand=self.scrollbar.set)

        self.load_button = tk.Button(self.root, text="Load Program", command=self.load_program)
        self.load_button.pack()

        self.run_button = tk.Button(self.root, text="Run Program", command=self.run_program)
        self.run_button.pack()

        self.memory_button = tk.Button(self.root, text="Show Memory", command=self.show_memory)
        self.memory_button.pack()
        
        self.reinitialize_button = tk.Button(self.root, text="Reinitialize UVSim", command=self.initialize_uvsim)
        self.reinitialize_button.pack()

    def initialize_uvsim(self):
        self.uv_sim = uvsim.UVSim("gui")

    def load_program(self):
        file_name = filedialog.askopenfilename(title="Select a program file")
        if file_name:
            self.uv_sim.store_program_in_memory(file_name)
            self.io_field.delete(1.0, tk.END)  # Clear previous content
            with open(file_name, "r") as file:
                lines = file.readlines()
                for line in lines:
                    self.io_field.insert(tk.END, line)
                self.io_field.insert(tk.END, "\nProgram loaded from {}\n".format(file_name))

            # Resize the text window to fit the content
            self.io_field.config(width=max(40, len(max(lines, key=len))))

    def run_program(self):
        try:
            self.uv_sim.outputs = [] #clear outputs between each run
            self.uv_sim.run_program()
            for output in self.uv_sim.outputs:
                self.io_field.insert(tk.END, "\nOutput: {}\n".format(output))
        except EOFError:
            self.io_field.insert(tk.END, "End of program.\n")
        except Exception as e:
            self.io_field.insert(tk.END, f"Error: {str(e)}\n")

    def show_memory(self):
        memory_window = Toplevel(self.root)
        memory_window.title("Memory Contents")

        memory_text = tk.Text(memory_window, wrap="none", height=10, width=40)
        memory_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        memory_scrollbar = tk.Scrollbar(memory_window, command=memory_text.yview)
        memory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        memory_text.config(yscrollcommand=memory_scrollbar.set)

        # Display memory contents in the new window
        self.update_memory_text(memory_text)

        # Refresh button
        refresh_button = tk.Button(memory_window, text="Refresh Memory", command=lambda: self.update_memory_text(memory_text))
        refresh_button.pack()

    def update_memory_text(self, memory_text):
        # Clear existing text field
        memory_text.delete(1.0, tk.END)

        # Display memory
        memory_text.insert(tk.END, f"Accumulator: {self.uv_sim.accumulator}\n")
        for address, value in enumerate(self.uv_sim.memory.memory_array):
            memory_text.insert(tk.END, f"{address}: {value}\n")

if __name__ == "__main__":
    root = tk.Tk()
    uv_sim_gui = GUI(root)
    root.mainloop()
