import json
import struct
import tkinter as tk
from io import BytesIO
from tkinter.filedialog import askopenfilename, asksaveasfilename


class GUI:
    FILETYPES = [("Mugbem Files", "*.osas"), ("All Files", "*.*")]
    FILETYPES_SAVE = [("Mugbem Files", "*.osas"), ("Decoded Mugbem JSON", "*.json"), ("All Files", "*.*")]

    TITLE = "Mugbem Sniffer"
    STRUCT_FORMAT = '<qfd'

    class Functions:
        def __init__(self, gui: 'GUI'):
            self.gui = gui
            self.opened_file = None

        def open_file(self):
            """Open a file for editing."""
            filepath = askopenfilename(filetypes=GUI.FILETYPES)
            if not filepath:
                return
            self.gui.txt_edit.delete("1.0", tk.END)
            with open(filepath, mode="rb") as input_file:
                text = input_file.read()

            _block_size = int(struct.calcsize(GUI.STRUCT_FORMAT))

            result = [
                list(struct.unpack(GUI.STRUCT_FORMAT, text[i:i+_block_size]))
                for i in range(0, len(text), _block_size)
            ]
            result_json = json.dumps(result, indent=4)
            self.opened_file = filepath
            self.gui.data = result_json
            self.gui.txt_edit.insert(tk.END, result_json)
            self.gui.window.title(f"{GUI.TITLE} - {filepath}")

        def save_file(self):
            """Save the current file as a new file."""
            filepath = asksaveasfilename(filetypes=GUI.FILETYPES_SAVE)
            if not filepath:
                return
            with open(filepath, mode="wb") as output_file:

                text = self.gui.txt_edit.get("1.0", tk.END).encode('utf-8')
                if filepath[-4:] == 'osas':
                    res = BytesIO()
                    q = json.loads(text)
                    for item in q:
                        res.write(struct.pack(GUI.STRUCT_FORMAT, *item))
                    text = res.getvalue()
                output_file.write(text)
            self.gui.window.title(f"{GUI.TITLE} - {filepath}")

    def __init__(self):
        self.window = tk.Tk()
        self.window.title(GUI.TITLE)
        self.window.rowconfigure(0, minsize=800, weight=1)
        self.window.columnconfigure(1, minsize=800, weight=1)
        self.txt_edit = tk.Text(self.window)
        self.frm_buttons = tk.Frame(self.window, relief=tk.RAISED, bd=2)
        self.functions = GUI.Functions(self)
        self.btn_open = tk.Button(self.frm_buttons, text="Open", command=self.functions.open_file)
        self.btn_save = tk.Button(self.frm_buttons, text="Save As...", command=self.functions.save_file)

    def show(self):
        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5)
        self.frm_buttons.grid(row=0, column=0, sticky="ns")
        self.txt_edit.grid(row=0, column=1, sticky="nsew")
        return self.window.mainloop()
