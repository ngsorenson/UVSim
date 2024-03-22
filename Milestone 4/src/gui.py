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
        self.memory_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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

        self.memory_text = tk.Text(self.inner_memory_frame, wrap="none", padx=5, height=101) #need to show 101 otherwise 100th line was getting cut off in memory_text
        self.memory_text.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.memory_text.bind("<Key>", self.is_arrow_break)
        self.memory_text.bind("<KeyRelease>", self.edit_memory)
        self.memory_text.bind("<Button-3>", self.show_menu) #right-click to show menu

        self.memory_canvas.create_window((0, 0), window=self.inner_memory_frame, anchor="nw")

        self.update_memory_text()

        # Create a menu for copy, paste, and cut functionality
        self.memory_canvas_menu = tk.Menu(root, tearoff=0)
        self.memory_canvas_menu.add_command(label="Copy", command=self.copy_text)
        self.memory_canvas_menu.add_command(label="Paste", command=self.paste_text)
        self.memory_canvas_menu.add_command(label="Cut", command=self.cut_text)

        # Output frame
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.output_title_label = tk.Label(self.output_frame, text="Output")
        self.output_title_label.pack()

        self.output_text = tk.Text(self.output_frame, wrap="char", height=10, width=40)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_text.insert(tk.END, "> ")
        self.output_text.configure(state="disabled")

        self.output_scrollbar = tk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text.config(yscrollcommand=self.output_scrollbar.set)

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
        
        #Clear Output button
        self.clear_output_button = tk.Button(self.root, text="Clear Output", command=self.clear_output)
        self.clear_output_button.pack(fill=tk.X)

    def is_arrow_break(self, event):
        if (event.keysym_num < 37) or (event.keysym_num > 40):
            return "break"
        else:
            return ""

    def _on_mousewheel(self, event):
        self.memory_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def edit_memory(self, event):
        cursor_pos = self.memory_text.index(tk.INSERT).split(".")
        cursor_pos[0] = int(cursor_pos[0])
        cursor_pos[1] = int(cursor_pos[1])
        
        if cursor_pos[0] >= 101: #bugfix for trying to write past end of file 
            self.memory_text.mark_set("insert", "100.0") #move cursor to line 100
            return

        match event.keysym_num: #checks what keysym was pressed
            case 65288:     # backspace
                if self.memory_text.tag_ranges(tk.SEL): #added this to allow user to delete an entire selection instead of just one char at a time
                    self.memory_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    self.memory_title_label.config(text="Memory Contents*")
                else:
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
            case 65293:    # return
                if cursor_pos[0] < self.uv_sim.memory.max:
                    self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "\n")
                    self.memory_title_label.config(text="Memory Contents*")
            case 43:   # plus
                if (event.state == 1) and (cursor_pos[1] == 0):
                    try:
                        first_char = self.get_memory_line(cursor_pos[0])[0]
                        if (first_char != "+") and (first_char != "-"):
                            self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "+")
                            self.memory_title_label.config(text="Memory Contents*")
                    except:
                        self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "+")
                        self.memory_title_label.config(text="Memory Contents*")
            case 45:   # minus
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
                if (event.keysym_num >= 48) and (event.keysym_num <= 57):
                    try:
                        line_value = int(self.get_memory_line(cursor_pos[0]))
                        if abs(line_value) < 10**4:
                            self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", event.char)
                            self.memory_title_label.config(text="Memory Contents*")
                    except ValueError:
                        self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", event.char)
                        self.memory_title_label.config(text="Memory Contents*")

    def shortcut(self, event):
        if event.state & 4:
            match event.keysym_num:
                case 99: #c
                    self.copy_text()
                case 115: #s
                    self.save_gui_memory_text()
                case 118: #v
                    self.paste_text()
                case 120: #x
                    self.cut_text()

    def get_gui_memory_contents(self):
        return self.memory_text.get("1.0", "end-1c").split("\n")[:self.uv_sim.memory.max-1]
    
    def get_memory_line(self, line):
        return self.memory_text.get(f"{line}.0", f"{line+1}.0")[:-1]
    
    def save_gui_memory_text(self):
        if self.uv_sim.is_running:
            self.output_text.configure(state="normal")
            self.output_text.insert(tk.END, "\n> ")
            self.output_text.configure(state="disabled")
        self.uv_sim.store_program_in_memory(self.get_gui_memory_contents())
        self.update_memory_text()
        self.memory_title_label.config(text="Memory Contents")

    def initialize_uvsim(self):
        if self.uv_sim.is_running:
            self.output_text.configure(state="normal")
            self.output_text.insert(tk.END, "\n> ")
            self.output_text.configure(state="disabled")
        self.uv_sim = uvsim.UVSim("gui")
        self.update_memory_text()
        self.memory_title_label.config(text="Memory Contents")

    def load_program(self):
        file_name = filedialog.askopenfilename(title="Select a program file")
        if self.uv_sim.is_running:
            self.output_text.configure(state="normal")
            self.output_text.insert(tk.END, "\n> ")
            self.output_text.configure(state="disabled")
        self.memory_title_label.config(text="Memory Contents")
        if file_name:
            self.uv_sim.store_program_in_memory(file_name)
            self.update_memory_text()
            self.output_text.configure(state="normal")
            self.output_text.insert(tk.END, f"File loaded successfully from {file_name}.\n> ")
            self.output_text.configure(state="disabled")
    
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
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, f"File saved successfully to {file.name}.\n> ")
        self.output_text.configure(state="disabled")

    def step_program(self):
        self.output_text.configure(state="normal")
        try:
            if not self.uv_sim.is_running:
                self.output_text.insert(tk.END, "Running program:")
                self.save_gui_memory_text()
            self.uv_sim.step_program()
            if self.uv_sim.output is not None:
                self.output_text.insert(tk.END, f"\n{self.uv_sim.output}")
                self.uv_sim.output = None
            if not self.uv_sim.is_running:
                self.output_text.insert(tk.END, "\n> ")
        # except EOFError:
        #     self.output_text.insert(tk.END, "\nEnd of program.\n> ")
        except Exception as e:
            self.output_text.insert(tk.END, f"\nError: {str(e)}\n> ")
        self.update_memory_text()
        self.output_text.configure(state="disabled")

    def run_program(self):
        self.step_program()
        while self.uv_sim.is_running:
            self.step_program()
    
    def stop_program(self):
        self.uv_sim.is_running = False
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, "\n> ")
        self.output_text.configure(state="disabled")
        self.update_memory_text()

    def update_memory_text(self):
        # Clear existing text field
        self.memory_text.delete(1.0, tk.END)

        # Display memory
        self.accumulator_text.config(state="normal")
        self.accumulator_text.delete(1.0, tk.END)
        self.accumulator_text.insert(tk.END, self.uv_sim.accumulator)
        self.accumulator_text.config(state="disabled")
        for address, value in enumerate(self.uv_sim.memory.memory_array): #i don't remember why i changed this
            if value is not None:
                if address == 99:
                    self.memory_text.insert(tk.END, value)
                else: 
                    self.memory_text.insert(tk.END, f"{value}\n") 

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

    def clear_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")
    
    def show_menu(self, event):
        self.memory_canvas_menu.post(event.x_root, event.y_root)
    
    def copy_text(self):
        try:
            selected_text = self.memory_text.get(tk.SEL_FIRST, tk.SEL_LAST) #exception would be thrown here if nothing selected
            self.root.clipboard_clear() #so this line wouldn't execute meaning we don't lose clipboard
            self.root.clipboard_append(selected_text)
        except: 
            pass

    def paste_text(self):
        pasted_text = self.root.clipboard_get()
        try:
            self.memory_text.delete(tk.SEL_FIRST, tk.SEL_LAST)  # Delete selected text if any
        except:
            pass
        
        #find how many lines we currently have
        lines= self.memory_text.get("1.0", "end").strip().split("\n")
        
        for line in lines: #fixes an issue with not being able to paste a full 100 lines into an empty window 
            if line == '':
                lines.remove(line)

        # Count how many lines will be pasted
        lines_to_paste = pasted_text.split("\n")
        total_lines = len(lines) + len(lines_to_paste)
        
        # Truncate pasted text if it exceeds the limit
        if total_lines > 100:
            excess_lines = total_lines - 100
            lines_to_paste = lines_to_paste[:-excess_lines]

        for line in lines_to_paste:
            self.memory_text.insert(tk.INSERT, line + "\n")

    def cut_text(self):
        try:
            selected_text = self.memory_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
            self.memory_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except: #do nothing if no selection exists
            pass

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(width=800, height=400)
    uv_sim_gui = GUI(root)
    root.mainloop()
