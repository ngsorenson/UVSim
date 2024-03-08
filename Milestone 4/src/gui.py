import tkinter as tk
from tkinter import filedialog
import uvsim

class GUI:
    def __init__(self, root):
        self.uv_sim = uvsim.UVSim("gui")

        self.root = root
        self.root.title("UVSim")

        # Memory frame
        self.memory_frame = tk.Frame(self.root)
        self.memory_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.memory_title_label = tk.Label(self.memory_frame, text="Memory Content")
        self.memory_title_label.pack()

        self.memory_text = tk.Text(self.memory_frame, wrap="none", height=10, width=40)
        self.memory_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.memory_scrollbar = tk.Scrollbar(self.memory_frame, command=self.memory_text.yview)
        self.memory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.memory_text.config(yscrollcommand=self.memory_scrollbar.set)

        self.update_memory_text()

        # Output frame
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.output_title_label = tk.Label(self.output_frame, text="Output")
        self.output_title_label.pack()

        self.output_field = tk.Text(self.output_frame, wrap="none", height=10, width=40)
        self.output_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.output_scrollbar = tk.Scrollbar(self.output_frame, command=self.output_field.yview)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_field.config(yscrollcommand=self.output_scrollbar.set)

        # Load, Run, and Reinitialize buttons
        self.load_button = tk.Button(self.root, text="Load Program", command=self.load_program)
        self.load_button.pack()

        self.run_button = tk.Button(self.root, text="Run Program", command=self.run_program)
        self.run_button.pack()

        # refresh_button = tk.Button(self.root, text="Refresh Memory", command=self.update_memory_text)
        # refresh_button.pack()

        self.reinitialize_button = tk.Button(self.root, text="Reinitialize UVSim", command=self.initialize_uvsim)
        self.reinitialize_button.pack()


    def initialize_uvsim(self):
        self.uv_sim = uvsim.UVSim("gui")
        self.update_memory_text()

    def load_program(self):
        file_name = filedialog.askopenfilename(title="Select a program file")
        if file_name:
            self.uv_sim.store_program_in_memory(file_name)
            self.memory_text.delete(1.0, tk.END)  # Clear previous content
            with open(file_name, "r") as file:
                lines = file.readlines()
                for line in lines:
                    self.memory_text.insert(tk.END, line)
                self.memory_text.insert(tk.END, "\nProgram loaded from {}\n".format(file_name))

            # Resize the text window to fit the content
            self.memory_text.config(width=max(40, len(max(lines, key=len))))

    def run_program(self):
        try:
            self.uv_sim.run_program()
            for output in self.uv_sim.outputs:
                self.output_field.insert(tk.END, "\nOutput: {}\n".format(output))
        except EOFError:
            self.output_field.insert(tk.END, "End of program.\n")
        except Exception as e:
            self.output_field.insert(tk.END, f"Error: {str(e)}\n")

    def update_memory_text(self):
        # Clear existing text field
        self.memory_text.delete(1.0, tk.END)

        # Display memory
        self.memory_text.insert(tk.END, f"Accumulator: {self.uv_sim.accumulator}\n")
        for address, value in enumerate(self.uv_sim.memory.memory_array):
            self.memory_text.insert(tk.END, f"{address}: {value}\n")

if __name__ == "__main__":
    root = tk.Tk()
    uv_sim_gui = GUI(root)
    root.mainloop()
