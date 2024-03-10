import tkinter as tk
from tkinter import filedialog
import uvsim

class GUI:
    def __init__(self, root):
        self.uv_sim = uvsim.UVSim("gui")

        self.root = root
        self.root.title("UVSim")
        self.root.bind("<KeyRelease>", self.shortcut)

        # Left frame
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5, expand=False)
        
        # Accumulator frame
        self.accumulator_frame = tk.Frame(self.left_frame)
        self.accumulator_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=(0, 16))

        self.accumulator_label = tk.Label(self.accumulator_frame, text="Accumulator: ")
        self.accumulator_label.pack(side=tk.LEFT, fill=tk.NONE)

        self.accumulator_text = tk.Text(self.accumulator_frame, wrap="none", padx=5, height=1, width=6)
        self.accumulator_text.config(state="disabled")
        self.accumulator_text.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # Memory frame
        self.memory_frame = tk.Frame(self.left_frame, pady=5,)
        self.memory_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.memory_title_label = tk.Label(self.memory_frame, text="Memory Contents")
        self.memory_title_label.pack()

        self.memory_canvas = tk.Canvas(self.memory_frame, width=40)
        self.memory_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.memory_scrollbar = tk.Scrollbar(self.memory_frame, orient=tk.VERTICAL, command=self.memory_canvas.yview)
        self.memory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.memory_canvas.configure(yscrollcommand=self.memory_scrollbar.set)
        self.memory_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.memory_canvas.bind("<Configure>", lambda e: self.memory_canvas.configure(scrollregion=self.memory_canvas.bbox("all")))

        self.inner_memory_frame = tk.Frame(self.memory_canvas)

        #Line Numbers
        self.memory_line_text = tk.Text(self.inner_memory_frame, wrap="none", padx=5, height=100, width=3)
        self.memory_line_text.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.memory_line_text.configure(state="disabled")

        self.memory_text = tk.Text(self.inner_memory_frame, wrap="none", padx=5, height=100)
        self.memory_text.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.memory_text.bind("<Key>", self.is_arrow_break)
        self.memory_text.bind("<KeyRelease>", self.edit_memory)

        self.memory_canvas.create_window((0, 0), window=self.inner_memory_frame, anchor="nw")

        self.update_memory_text()

        # Output frame
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.output_title_label = tk.Label(self.output_frame, text="Output")
        self.output_title_label.pack()

        self.output_field = tk.Text(self.output_frame, wrap="char", height=10, width=40)
        self.output_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_field.insert(tk.END, "> ")
        self.output_field.configure(state="disabled")

        self.output_scrollbar = tk.Scrollbar(self.output_frame, command=self.output_field.yview)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_field.config(yscrollcommand=self.output_scrollbar.set)

        # Buttons
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(padx=5, pady=10)

        # File buttons
        self.file_buttons_frame = tk.Frame(self.buttons_frame)
        self.file_buttons_frame.pack(fill=tk.X, pady=(0, 8))

        self.load_button = tk.Button(self.file_buttons_frame, text="Load Program", command=self.load_program)
        self.load_button.pack(fill=tk.X)

        self.save_button = tk.Button(self.file_buttons_frame, text="Save Program", command=self.save_program)
        self.save_button.pack(fill=tk.X)

        # Program execution buttons
        self.execute_buttons = tk.Frame(self.buttons_frame)
        self.execute_buttons.pack(pady=(0, 3))

        self.run_button = tk.Button(self.execute_buttons, text="Run Program", command=self.run_program)
        self.run_button.pack(fill=tk.X)

        self.step_button = tk.Button(self.execute_buttons, text="Step Program", command=self.step_program)
        self.step_button.pack(fill=tk.X)

        self.step_button = tk.Button(self.execute_buttons, text="Stop Program", command=self.stop_program)
        self.step_button.pack(fill=tk.X)

        # Reinitialize button
        self.reinitialize_button = tk.Button(self.root, text="Reinitialize UVSim", command=self.initialize_uvsim)
        self.reinitialize_button.pack(fill=tk.X)

    def is_arrow_break(self, event):
        if (event.keycode < 37) or (event.keycode > 40):
            return "break"
        else:
            return ""

    def _on_mousewheel(self, event):
        self.memory_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def edit_memory(self, event):
        cursor_pos = self.memory_text.index(tk.INSERT).split(".")
        cursor_pos[0] = int(cursor_pos[0])
        cursor_pos[1] = int(cursor_pos[1])
        match event.keycode:
            case 8:     # backspace
                if cursor_pos[1] > 0:
                    self.memory_text.delete(f"{cursor_pos[0]}.{cursor_pos[1]-1}", f"{cursor_pos[0]}.{cursor_pos[1]}")
                    self.memory_title_label.config(text="Memory Contents*")
                elif self.get_memory_line(cursor_pos[0]-1) == "":
                    self.memory_text.delete(f"{cursor_pos[0]-1}.0", f"{cursor_pos[0]}.0")
                    self.memory_title_label.config(text="Memory Contents*")
                elif self.get_memory_line(cursor_pos[0]) == "":
                    self.memory_text.delete(f"{cursor_pos[0]}.0", f"{cursor_pos[0]+1}.0")
                    self.memory_text.mark_set("insert", f"{cursor_pos[0]-1}.{len(self.get_memory_line(cursor_pos[0]-1))}")
                    self.memory_title_label.config(text="Memory Contents*")
                else:
                    self.memory_text.mark_set("insert", f"{cursor_pos[0]-1}.{len(self.get_memory_line(cursor_pos[0]-1))}")
            case 13:    # enter
                if cursor_pos[0] < self.uv_sim.memory.max:
                    self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "\n")
                    self.memory_title_label.config(text="Memory Contents*")
            case 187:   # plus
                if (event.state == 9) and (cursor_pos[1] == 0):
                    try:
                        first_char = self.get_memory_line(cursor_pos[0])[0]
                        if (first_char != "+") and (first_char != "-"):
                            self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "+")
                            self.memory_title_label.config(text="Memory Contents*")
                    except:
                        self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "+")
                        self.memory_title_label.config(text="Memory Contents*")
            case 189:   # minus
                if cursor_pos[1] == 0:
                    try:
                        first_char = self.get_memory_line(cursor_pos[0])[0]
                        if (first_char != "+") and (first_char != "-"):
                            self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "-")
                            self.memory_title_label.config(text="Memory Contents*")
                    except:
                        self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "-")
                        self.memory_title_label.config(text="Memory Contents*")
            case _:
                # integer
                if (event.keycode >= 48) and (event.keycode <= 57):
                    try:
                        line_value = int(self.get_memory_line(cursor_pos[0]))
                        if abs(line_value) < 10**4:
                            self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", event.char)
                            self.memory_title_label.config(text="Memory Contents*")
                    except ValueError:
                        self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", event.char)
                        self.memory_title_label.config(text="Memory Contents*")
                else:
                    self.shortcut(event)

    def shortcut(self, event):
        match event.keycode:
            case 83:
                if event.state == 12:
                    self.save_gui_memory_text()

    def get_gui_memory_contents(self):
        return self.memory_text.get("1.0", "end-1c").split("\n")[:self.uv_sim.memory.max-1]
    
    def get_memory_line(self, line):
        return self.memory_text.get(f"{line}.0", f"{line+1}.0")[:-1]
    
    def save_gui_memory_text(self):
        if self.uv_sim.is_running:
            self.output_field.configure(state="normal")
            self.output_field.insert(tk.END, "\n> ")
            self.output_field.configure(state="disabled")
        self.uv_sim.store_program_in_memory(self.get_gui_memory_contents())
        self.update_memory_text()
        self.memory_title_label.config(text="Memory Contents")

    def initialize_uvsim(self):
        if self.uv_sim.is_running:
            self.output_field.configure(state="normal")
            self.output_field.insert(tk.END, "\n> ")
            self.output_field.configure(state="disabled")
        self.uv_sim = uvsim.UVSim("gui")
        self.update_memory_text()
        self.memory_title_label.config(text="Memory Contents")

    def load_program(self):
        file_name = filedialog.askopenfilename(title="Select a program file")
        if self.uv_sim.is_running:
            self.output_field.configure(state="normal")
            self.output_field.insert(tk.END, "\n> ")
            self.output_field.configure(state="disabled")
        self.memory_title_label.config(text="Memory Contents")
        if file_name:
            self.uv_sim.store_program_in_memory(file_name)
            self.update_memory_text()
            self.output_field.configure(state="normal")
            self.output_field.insert(tk.END, "File loaded successfully.\n> ")
            self.output_field.configure(state="disabled")
    
    def save_program(self):
        self.save_gui_memory_text()
        file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
        if file is None:
            return
        program = self.get_gui_memory_contents()
        output = ""
        for line in program:
            if (len(line) > 0):
                if int(line) < 10**4:
                    output += line + "\n"
                else:
                    break
            else:
                output += "\n"
        file.write(output[:-1])
        file.close()
        self.output_field.configure(state="normal")
        self.output_field.insert(tk.END, "File saved successfully.\n> ")
        self.output_field.configure(state="disabled")

    def step_program(self):
        self.output_field.configure(state="normal")
        try:
            if not self.uv_sim.is_running:
                self.output_field.insert(tk.END, "Running program:")
                self.save_gui_memory_text()
            self.uv_sim.step_program()
            if self.uv_sim.output is not None:
                self.output_field.insert(tk.END, f"\n{self.uv_sim.output}")
                self.uv_sim.output = None
            if not self.uv_sim.is_running:
                self.output_field.insert(tk.END, "\n> ")
        # except EOFError:
        #     self.output_field.insert(tk.END, "\nEnd of program.\n> ")
        except Exception as e:
            self.output_field.insert(tk.END, f"\nError: {str(e)}\n> ")
        self.update_memory_text()
        self.output_field.configure(state="disabled")

    def run_program(self):
        self.step_program()
        while self.uv_sim.is_running:
            self.step_program()
    
    def stop_program(self):
        self.uv_sim.is_running = False
        self.output_field.configure(state="normal")
        self.output_field.insert(tk.END, "\n> ")
        self.output_field.configure(state="disabled")
        self.update_memory_text()

    def update_memory_text(self):
        # Clear existing text field
        self.memory_text.delete(1.0, tk.END)

        # Display memory
        self.accumulator_text.config(state="normal")
        self.accumulator_text.delete(1.0, tk.END)
        self.accumulator_text.insert(tk.END, self.uv_sim.accumulator)
        self.accumulator_text.config(state="disabled")
        for address, value in enumerate(self.uv_sim.memory.memory_array):
            if address == 0:
                newline = ""
            else:
                newline = "\n"
            if value is not None:
                self.memory_text.insert(tk.END, f"{newline}{value}")
            elif address == 99:
                self.memory_text.insert(tk.END, "")
            else:
                self.memory_text.insert(tk.END, "\n")
        
        self.memory_line_text.config(state="normal")
        self.memory_line_text.delete(1.0, tk.END)
        self.memory_line_text.tag_configure("right", justify="right")
        newline = ""
        for i in range(0, self.uv_sim.memory.max):
            if self.uv_sim.is_running and (self.uv_sim.program_counter == i):
                if i < 10:
                    self.memory_line_text.insert(tk.END, f"{newline}> {i}")
                else:
                    self.memory_line_text.insert(tk.END, f"{newline}>{i}")
            else:
                self.memory_line_text.insert(tk.END, f"{newline}{i}")
            newline = "\n"
        self.memory_line_text.tag_add("right", 1.0, tk.END)
        self.memory_line_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(width=800, height=400)
    uv_sim_gui = GUI(root)
    root.mainloop()
