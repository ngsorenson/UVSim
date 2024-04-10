import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import uvsim
import re
from file_formatter import TxtFormatter

DEFAULT_PRIMARY_COLOR = '#4C721D'    # UVU GREEN 
DEFAULT_SECONDARY_COLOR = '#FFFFFF'  # UVU WHITE

# labels
ROOT_LABEL = "UVSim"
ACC_LABEL = "ACCUMULATOR: "
MEMORY_LABEL = "MEMORY CONTENTS"
OUTPUT_LABEL = "OUTPUT"
MEMORY_LABEL_UNSAVED_CHANGES = "MEMORY CONTENTS*"

def is_valid_hex_code(s):
    # Regular expression to match hexadecimal color code with '#' symbol required
    hex_regex = r'^#[a-fA-F0-9]{6}$|^#[a-fA-F0-9]{3}$'
    return bool(re.match(hex_regex, s))

class GUIHandler:
    def __init__(self, root):
        self.tab_number = 1
        self.root = root
        self.root.title(ROOT_LABEL)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_tab()
        self.set_guihandler_colors(DEFAULT_PRIMARY_COLOR, DEFAULT_SECONDARY_COLOR)

    def create_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=f"Tab {self.tab_number}")
        self.tab_number += 1
        
        tab_management_buttons = ttk.Frame(tab)
        close_button = ttk.Button(tab_management_buttons, text="X", command=lambda: self.close_tab(tab)) #close current tab
        edit_button = ttk.Button(tab_management_buttons, text="Change Tab Name", command=lambda: self.change_tab_name(tab)) #edit current tab name
        add_tab_button = ttk.Button(tab_management_buttons, text="+", command=self.create_tab) #add new tab
        edit_button.pack(side='left')
        close_button.pack(side='right')
        add_tab_button.pack(side='right')
        tab_management_buttons.pack(anchor='ne', side="top")

        # uv_sim = uvsim.UVSim(gui=True) # will create whatever the default version parameter of uvsim is
        # GUI(tab, uv_sim)
        GUI(tab)
    
    def close_tab(self, tab):
        total_tabs = self.notebook.index('end')
        if total_tabs == 1: #tab is last tab, prompt before quitting program
            if tk.messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?"):
                self.root.quit()
        else:
            self.notebook.forget(tab)

    def change_tab_name(self, tab):
        current_text = self.notebook.tab(tab, "text")
        new_name = tk.simpledialog.askstring("Edit Tab Name", f"Enter new name for this tab", initialvalue=current_text)
        if new_name:
            self.notebook.tab(tab, text=new_name)

    def set_guihandler_colors(self, color1, color2):
        style = ttk.Style()
        style.theme_use('default')
        if is_valid_hex_code(color1):
            style.configure('TNotebook', background=color1)
            style.map('TNotebook.Tab', background = [('selected', color1)])
            style.configure('TFrame', background=color1)
        if is_valid_hex_code(color2):
            style.configure('TButton', background=color2)
        return style

class GUI:
    def __init__(self, tab, version = 2):
        self.uv_sim = uvsim.UVSim(version, True)
        self.root = tab #self.root is now referencing the tab parent in the ttk notebook from GUIHandler
        # self.root.bind("<KeyPress>", self.shortcut)   # this key binding event is now handled in the key binding event for arrow keys

        # Left frame
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=5, expand=False)

        # Accumulator frame
        self.accumulator_frame = tk.Frame(self.left_frame)
        self.accumulator_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=(0, 16))

        self.accumulator_label = tk.Label(self.accumulator_frame,  text=ACC_LABEL)
        self.accumulator_label.pack(side=tk.LEFT, fill=tk.NONE) 

        self.accumulator_text = tk.Text(self.accumulator_frame, wrap="none", padx=5, height=1, width=8)
        self.accumulator_text.config(state="disabled")
        self.accumulator_text.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # Memory frame
        self.memory_frame = tk.Frame(self.left_frame, pady=5)
        self.memory_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.memory_title_label = tk.Label(self.memory_frame, text=MEMORY_LABEL)
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
        self.memory_line_text = tk.Text(self.inner_memory_frame, wrap="none", padx=5, height=self.uv_sim.program_class.MAX_PROGRAM_LENGTH+2, width=3) #related to comment a few lines below
        self.memory_line_text.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.memory_line_text.configure(state="disabled")

        self.memory_text = tk.Text(self.inner_memory_frame, wrap="none", padx=5, height=self.uv_sim.program_class.MAX_PROGRAM_LENGTH + 1) # need to show max+1 otherwise max is cut off memory_text
        
        self.memory_text.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        self.memory_text.bind("<Key>", self.is_arrow_break)
        self.memory_text.bind("<KeyRelease>", self.edit_memory)
        self.memory_text.bind("<Button-3>", self.show_menu) # right-click to show menu

        self.memory_canvas.create_window((0, 0), window=self.inner_memory_frame, anchor="nw")

        self.update_memory_text()

        # Create a menu for copy, paste, and cut functionality
        self.memory_canvas_menu = tk.Menu(root, tearoff=0)
        self.memory_canvas_menu.add_command(label="Copy", command=self.copy_text)
        self.memory_canvas_menu.add_command(label="Paste", command=self.paste_text)
        self.memory_canvas_menu.add_command(label="Cut", command=self.cut_text)

        # Output frame
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=5, expand=True)

        self.output_title_label = tk.Label(self.output_frame, text=OUTPUT_LABEL)
        self.output_title_label.pack()

        self.output_text = tk.Text(self.output_frame, wrap="char", height=10, width=40)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_text.insert(tk.END, "> ")
        self.output_text.configure(state="disabled")

        self.output_scrollbar = tk.Scrollbar(self.output_frame, command=self.output_text.yview)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text.config(yscrollcommand=self.output_scrollbar.set)

        # File buttons
        self.file_buttons_frame = tk.Frame(self.root)
        self.file_buttons_frame.pack(fill=tk.X, pady=5)

        self.load_button = tk.Button(self.file_buttons_frame, text="Load Program", command=self.load_program)
        self.load_button.pack(fill=tk.X)

        self.save_button = tk.Button(self.file_buttons_frame, text="Save Program", command=self.save_program)
        self.save_button.pack(fill=tk.X)

        # Program execution buttons
        self.execute_buttons = tk.Frame(self.root)
        self.execute_buttons.pack(fill=tk.X, pady=(0,5))

        self.run_button = tk.Button(self.execute_buttons, text="Run Program", command=self.run_program)
        self.run_button.pack(fill=tk.X)

        self.step_button = tk.Button(self.execute_buttons, text="Step Program", command=self.step_program)
        self.step_button.pack(fill=tk.X)

        self.stop_button = tk.Button(self.execute_buttons, text="Stop Program", command=self.stop_program)
        self.stop_button.pack(fill=tk.X)
        
        # Reinitialize button
        self.reinitialize_button = tk.Button(self.root, text="Reinitialize UVSim", command=self.initialize_uvsim)
        self.reinitialize_button.pack(fill=tk.X)

        # Change version button
        self.version_button = tk.Button(self.root, text="Change Version", command=self.change_version)
        self.version_button.pack(fill=tk.X)
        
        # Clear Output button
        self.clear_output_button = tk.Button(self.root, text="Clear Output", command=self.clear_output)
        self.clear_output_button.pack(fill=tk.X)

        # Change colors button
        self.change_colors_button = tk.Button(self.root, text="Change Color Scheme", command=self.open_color_popup)
        self.change_colors_button.pack(fill=tk.X)

        self.reset_colors_button = tk.Button(self.root, text="Reset to Default Colors",command=lambda: self.set_colors(DEFAULT_PRIMARY_COLOR, DEFAULT_SECONDARY_COLOR))
        self.reset_colors_button.pack(fill=tk.X)

        # SET COLORS TO THE DEFAULTS UPON STARTUP
        #self.set_colors(DEFAULT_PRIMARY_COLOR, DEFAULT_SECONDARY_COLOR) #broken by ttk notebook
    
    def get_inputs(self, entry1, entry2, popup):
            input1 = entry1.get()
            input2 = entry2.get()

            if not is_valid_hex_code(input1):
                print(f"Error: Primary color input '{input1}' was not a valid hex code. No primary color change.")
            else:
                print(f"Primary color successfully changed to '{input1}'")
            if not is_valid_hex_code(input2):
                print(f"Error: Secondary color input: '{input2}' was not a valid hex code. No secondary color change.")
            else: 
                print(f"Secondary color was successfully changed to '{input2}'")
            self.set_colors(input1, input2)
            popup.destroy()

    def open_color_popup(self):
        popup = tk.Toplevel(root)
        popup.title("Input")
        label0 = tk.Label(
            popup, 
            text="Enter a hex code value for the color you want to change. Example: #4C721D. Leave blank for no change."
        )
        label0.pack(expand=False, fill=tk.BOTH)

        label_frame = tk.Frame(popup)
        label_frame.pack(pady=10, expand=True)

        label1 = tk.Label(label_frame, text="Enter primary color hexcode:")
        label1.pack(side="left")
        entry1 = tk.Entry(label_frame)
        entry1.pack(side="left")

        label2 = tk.Label(label_frame, text="Enter secondary color hexcode:")
        label2.pack(side="left")
        entry2 = tk.Entry(label_frame)
        entry2.pack(side="right") 

        button_frame=tk.Frame(popup)
        button_frame.pack()

        submit_button = tk.Button(
            button_frame, 
            text="Submit", 
            command=lambda: self.get_inputs(entry1, entry2, popup),
        )
        submit_button.pack(side="left", padx=5, pady=5)

        cancel_button = tk.Button(
            button_frame, 
            text="Cancel", 
            command=popup.destroy,
        )
        cancel_button.pack(side="right", padx=5, pady=5)

    def set_colors(self, color1, color2): 
        # All frames are color1 or what they were before. 
        frames = [
            self.root,
            self.left_frame,
            self.inner_memory_frame,
            self.file_buttons_frame,
            self.execute_buttons, 
        ]
        # All buttons and text are color2 or what they were before. 
        bt_list = [
            self.accumulator_frame,
            self.memory_frame,
            self.output_frame,
            self.accumulator_label,
            self.accumulator_text, 
            self.memory_title_label,
            self.memory_line_text,
            self.memory_text,
            self.output_title_label,
            self.output_text, 
            self.load_button,
            self.save_button,
            self.run_button,
            self.step_button,
            self.stop_button,
            self.reinitialize_button,
            self.clear_output_button,
            self.change_colors_button,
            self.memory_canvas,
            self.reset_colors_button,
            self.execute_buttons
        ]

        #manually set the colors of the labels
        labels = [self.accumulator_label,
                  self.memory_title_label,
                  self.output_title_label
        ]

        for label in labels:
            label.config(fg='black')
 
        #manually set the colors for the text elements
        text_elements = [self.accumulator_text,
                         self.memory_line_text,
                         self.memory_text,
                         self.output_text
        ]

        for text in text_elements:
            text.config(fg='black')

        if is_valid_hex_code(color1):
            for frame in frames:    
                frame.config(bg=color1)

        if is_valid_hex_code(color2):
            for bt in bt_list:  
                bt.config(bg=color2)
    
    def change_version(self):
        version_popup = tk.Toplevel()
        version_popup.title("Change UVSim Version")
        text=tk.Label(version_popup, text="What UVSim version would you like to switch to?")
        text.pack()
        versions = ["v1 - 4 bit", "v2 - 6 bit"]
        clicked = tk.StringVar()
        if self.uv_sim.version == 1:
            clicked.set(f'v{self.uv_sim.version} - 4 bit')
        elif self.uv_sim.version == 2:
            clicked.set(f'v{self.uv_sim.version} - 6 bit')

        drop = tk.OptionMenu(version_popup, clicked, *versions ) 
        drop.pack() 

        warning=tk.Label(version_popup, text="Changing versions with a program loaded into memory will corrupt the program in memory (but not the source file)")
        warning.pack()

        confirm_button = tk.Button(version_popup, text = "Confirm", command=lambda:self.change_version_helper(clicked.get(), version_popup))
        confirm_button.pack(side="left", anchor='center')

        cancel_button = tk.Button(version_popup, text="Cancel", command=version_popup.destroy)
        cancel_button.pack(side='right', anchor='center')

    def change_version_helper(self, selected_version, version_popup):
        '''need this separate function to capture what is selected on click event'''
        match selected_version:
            case "v1 - 4 bit":
                version = 1
                
            case "v2 - 6 bit":
                version = 2

        if version is not None:
            self.uv_sim.change_version(version)
            self.update_memory_text()
            version_popup.destroy()
            
    def is_arrow_break(self, event):
        self.shortcut(event)
        if event.keysym not in ("Left", "Right", "Up", "Down"):
            return "break"
        else:
            return ""

    def _on_mousewheel(self, event):
        self.memory_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def edit_memory(self, event):
        cursor_pos = self.memory_text.index(tk.INSERT).split(".")
        cursor_pos[0] = int(cursor_pos[0])
        cursor_pos[1] = int(cursor_pos[1])
        
        if cursor_pos[0] >= self.uv_sim.memory.max + 1: #bugfix for trying to write past end of file 
            self.memory_text.mark_set("insert", f"{float(self.uv_sim.memory.max)}") #move cursor to max line
            return

        match event.keysym_num: #checks what keysym was pressed
            case 65288:     # backspace
                if self.memory_text.tag_ranges(tk.SEL): #added this to allow user to delete an entire selection instead of just one char at a time
                    self.memory_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
                else:
                    if cursor_pos[1] > 0:
                        self.memory_text.delete(f"{cursor_pos[0]}.{cursor_pos[1]-1}", f"{cursor_pos[0]}.{cursor_pos[1]}")
                        self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
                    elif self.get_memory_line(cursor_pos[0]-1) == "":
                        self.memory_text.delete(f"{cursor_pos[0]-1}.0", f"{cursor_pos[0]}.0")
                        self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
                    elif self.get_memory_line(cursor_pos[0]) == "":
                        self.memory_text.delete(f"{cursor_pos[0]}.0", f"{cursor_pos[0]+1}.0")
                        self.memory_text.mark_set("insert", f"{cursor_pos[0]-1}.{len(self.get_memory_line(cursor_pos[0]-1))}")
                        self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
                    else:
                        self.memory_text.mark_set("insert", f"{cursor_pos[0]-1}.{len(self.get_memory_line(cursor_pos[0]-1))}")
            case 65293:    # return
                if cursor_pos[0] < self.uv_sim.memory.max:
                    self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "\n")
                    self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
            case 43:   # plus
                if (event.state & 1) and (cursor_pos[1] == 0):
                    try:
                        first_char = self.get_memory_line(cursor_pos[0])[0]
                        if (first_char != "+") and (first_char != "-"):
                            self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "+")
                            self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
                    except:
                        self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "+")
                        self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
            case 45:   # minus
                if cursor_pos[1] == 0:
                    try:
                        first_char = self.get_memory_line(cursor_pos[0])[0]
                        if (first_char != "+") and (first_char != "-"):
                            self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "-")
                            self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
                    except:
                        self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", "-")
                        self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
            case _:
                # integer
                if (event.keysym_num >= 48) and (event.keysym_num <= 57):
                    try:
                        line_value = self.get_memory_line(cursor_pos[0])
                        if (len(line_value) <= self.uv_sim.program_class.MAX_LINE_LENGTH) or (((line_value[0] == "+") or (line_value[0] == "-")) and (len(line_value[1:]) < self.uv_sim.program_class.MAX_LINE_LENGTH)): #this is where we control line length from user input
                            self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", event.char)
                            self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)
                    except ValueError:
                        self.memory_text.insert(f"{cursor_pos[0]}.{cursor_pos[1]}", event.char)
                        self.memory_title_label.config(text=MEMORY_LABEL_UNSAVED_CHANGES)

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
        self.uv_sim.store_program_in_memory(self.get_gui_memory_contents(), skip_identification=True)
        self.update_memory_text()
        self.memory_title_label.config(text=MEMORY_LABEL)

    def initialize_uvsim(self):
        if self.uv_sim.is_running:
            self.output_text.configure(state="normal")
            self.output_text.insert(tk.END, "\n> ")
            self.output_text.configure(state="disabled")
        self.uv_sim = uvsim.UVSim(self.uv_sim.version, True)
        self.update_memory_text()
        self.memory_title_label.config(text=MEMORY_LABEL)

    def load_program(self):
        file_name = filedialog.askopenfilename(title="Select a program file")
        if self.uv_sim.is_running:
            self.output_text.configure(state="normal")
            self.output_text.insert(tk.END, "\n> ")
            self.output_text.configure(state="disabled")
        self.memory_title_label.config(text=MEMORY_LABEL)
        if file_name:
            self.initialize_uvsim()
            self.uv_sim.store_program_in_memory(TxtFormatter.format_file(file_name))
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
        self.memory_text.configure(height=self.uv_sim.program_class.MAX_PROGRAM_LENGTH+1)
        for address, value in enumerate(self.uv_sim.memory.memory_array):
            if value is not None:
                value_str = str(abs(value))
                line = value_str.rjust(self.uv_sim.program_class.MAX_LINE_LENGTH, "0")
                if len(line) <= self.uv_sim.program_class.MAX_LINE_LENGTH:
                    if value >= 0:
                        line = "+" + line
                    else:
                        line = "-" + line
                if address != self.uv_sim.memory.max:
                    line += "\n"
                self.memory_text.insert(tk.END, line) 

        self.memory_line_text.config(state="normal")
        self.memory_line_text.delete(1.0, tk.END)
        self.memory_line_text.tag_configure("right", justify="right")
        self.memory_line_text.configure(height=self.uv_sim.program_class.MAX_PROGRAM_LENGTH+2)
        newline = ""
        for i in range(0, self.uv_sim.program_class.MAX_PROGRAM_LENGTH):
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
        lines= self.memory_text.get("1.0", "end").split("\n")
        
        for line in lines: #fixes an issue with not being able to paste a full 100 lines into an empty window 
            if line == '':
                lines.remove(line)

        # Count how many lines will be pasted
        lines_to_paste = pasted_text.split("\n")
        total_lines = len(lines) + len(lines_to_paste)
        
        # Truncate pasted text if it exceeds the limit
        if total_lines > self.uv_sim.memory.max:
            excess_lines = total_lines - self.uv_sim.memory.max
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
    gui_handler = GUIHandler(root)
    root.mainloop()
