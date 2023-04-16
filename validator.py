import os
import tkinter as tk
from tkinter import ttk, filedialog, Menu
from lxml import etree
import csv
import json
from model import XMLFile


# Set schema files
schema_files = open(r"X:\Work\xmlvalidator\schemas.json")
SCHEMAS = json.load(schema_files)

###### Set up gui theme and size ###########
root = tk.Tk()

style = ttk.Style()

BG_COLOR = "#299617"
LBL_COLOR = "#ffffff"
TXT_COLOR = "#DCDCDC"
FONT = "Helvetica 12 bold"
TITLE = "PIES Validator"
ICON = 'X:\Work\logo.ico'
w = 400
h = 250


menubar = Menu(root)
root.resizable(False, False)

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)


root.title(TITLE)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.config(bg=BG_COLOR)
root.iconbitmap(ICON)

style.configure("TLabelframe", background=LBL_COLOR)
style.configure(
    "TLabelframe.Label", font=FONT, background=LBL_COLOR, color=BG_COLOR
)

xml_file = XMLFile()

message = tk.Label(
    root,
    text="Open a file to begin.",
    background=LBL_COLOR,
)
message.pack(fill="both", expand=True)
message.propagate(False)
message.configure(wraplength=375)

filemenu = Menu(menubar, background=LBL_COLOR, tearoff=0)
filemenu.add_command(
    label="Open", command=lambda: message.config(text=set_file(xml_file)))

filemenu.add_command(
    label="Validate", command=lambda: message.config(text=validate_file(xml_file)))
filemenu.add_command(
    label="Errors", command=lambda: generate_error_log(xml_file))
filemenu.entryconfig("Errors", state="disabled")
filemenu.entryconfig("Validate", state="disabled")
filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)


def set_file(xml: XMLFile) -> str:
    file = filedialog.askopenfile(filetypes=[("XML Files", "*.xml")])
    if file.name == None:
        if xml.file == None:
            return "Open a file to begin."
        return f"Current File: \n {xml.file.name}"
    xml.set_file(file)
    filemenu.entryconfig("Errors", state="disabled")
    filemenu.entryconfig("Validate", state="normal")
    return f"Current File: \n {xml.file.name}"


def define_schema(xml: XMLFile):
    try:
        xml.set_schema(SCHEMAS[xml.version])
        print(xml.schema)
        return True
    except Exception as error:
        return f"Schema for PIES Version {error} not found. \n Please contact a Senior or Supervisor."


def get_pies_version(xml: XMLFile) -> bool | str:
    if xml == None:
        return "Please enter a valid file."
    try:
        tree = etree.parse(xml.file.name)
    except etree.XMLSyntaxError as error:
        return f"File failed validation on line: {error.lineno}. \n Error message: {error.msg}."
    try:
        root = tree.getroot()
        pies_version = root.find(
            f"./{xml.namespace}Header/{xml.namespace}PIESVersion").text
        xml.set_version(pies_version)
    except Exception as error:
        return f"Unable to validate file due to invalid XML structure and/or namespace."

    return define_schema(xml)


def validate_file(xml: XMLFile) -> str:
    valid = get_pies_version(xml)
    if valid != True:
        return valid
    file_schema = etree.parse(xml.schema)
    xml_schema = etree.XMLSchema(file_schema)
    xml_file = etree.parse(xml.file.name)
    try:
        xml_schema.assertValid(xml_file)
        xml.set_state(True)
        return "Validation Complete. File has passed validation!"
    except etree.DocumentInvalid:
        xml.set_state(False)
        errors = [[error.line, error.message]
                  for error in xml_schema.error_log]
        errors.insert(0, ["Line Number", "Error Message"])
        xml.error_log = errors
        filemenu.entryconfig("Errors", state="normal")
        return f"File failed schema validation. \n Generate report to review errors."


def generate_error_log(xml: XMLFile):
    save_path = filedialog.asksaveasfilename(
        filetypes=[("CSV Files", "*.csv")], defaultextension='.csv')
    if save_path == '':
        return
    save_path = f"{save_path}.csv"
    with open(save_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(xml.error_log)
    os.startfile(save_path)


root.config(menu=menubar)

if __name__ == "__main__":

    root.mainloop()
