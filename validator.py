import os
import tkinter as tk
from tkinter import ttk, filedialog, Menu
from lxml import etree
import csv
import json
from model import XMLFile


# Set schema files
SCHEMAS = json.load(open(os.environ['PIES_SCHEMAS_PATH']))




###### Set up gui theme and size ###########
root = tk.Tk()
xml_file = XMLFile()
style = ttk.Style()

BG_COLOR = "#299617"
LBL_COLOR = "#ffffff"
TXT_COLOR = "#DCDCDC"
FONT = "Helvetica 12 bold"
TITLE = "PIES Validator"
ICON = 'X:\Work\logo.ico'
w = 500
h = 300


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

message_frame = tk.Frame(root, background=LBL_COLOR)
message_frame.pack(fill="both", expand=True)

button_frame = tk.Frame(root, background=LBL_COLOR)
button_frame.pack(fill="both", expand=True)

message = tk.Label(
    message_frame,
    text="Open a file to begin.",
    background=LBL_COLOR,
)
message.pack(fill="both",  side='bottom')
report_button = ttk.Button(button_frame, command=lambda: generate_error_log(xml_file), text="Save And Open Error Report")

message.configure(wraplength=375)

filemenu = Menu(menubar, background=LBL_COLOR, tearoff=0)

filemenu.add_command(
    label="Open", command=lambda: main(xml_file))

filemenu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=filemenu)

root.config(menu=menubar)

def main(xml: XMLFile):
    loaded = set_file(xml)
    if not loaded:
        return
    has_pies = get_pies_version(xml) 
    
    if not has_pies:
        return
    validate_file(xml)

def set_file(xml: XMLFile)->bool:
    if xml.valid == True:
        report_button.pack_forget()
    xml.set_state(False)
    file = filedialog.askopenfile(filetypes=[("XML Files", "*.xml")])
    if file == None or file.name == None:
        message.config(text="Open a file to begin.")
        return False
    message.config(text= f"Validating: \n {file.name}")
    xml.set_file(file)
    return True

def define_schema(xml: XMLFile)->bool:
    try:
        xml.set_schema(SCHEMAS[xml.version])
        return True
    except Exception as error:
        xml.set_state(False)
        message.config(text=f"Schema for PIES Version {error} not found. \n Please contact a Senior or Supervisor.")
        return False


def get_pies_version(xml: XMLFile) -> bool:
    try:
        tree = etree.parse(xml.file.name)
    except etree.XMLSyntaxError as error:
        message.config(text= f"File failed validation on line: {error.lineno}. \n Error message: {error.msg}.")
        return False
    try:
        root = tree.getroot()
        pies_version = root.find(
            f"./{xml.namespace}Header/{xml.namespace}PIESVersion").text
        xml.set_version(pies_version)
    except Exception as error:
        xml.set_state(False)
        message.config(text=  f"Unable to validate file due to invalid XML structure and/or namespace.")
        return False
    return define_schema(xml)


def validate_file(xml: XMLFile) -> None:
    file_schema = etree.parse(xml.schema)
    xml_schema = etree.XMLSchema(file_schema)
    xml_file = etree.parse(xml.file.name)
    try:
        xml_schema.assertValid(xml_file)
        xml.set_state(False)
        message.config(text="Validation Complete. File has passed validation!")
        return
    except etree.DocumentInvalid:
        errors = [[error.line, error.message]
                  for error in xml_schema.error_log]
        errors.insert(0, ["Line Number", "Error Message"])
        xml.error_log = errors
        message.config(text=f"PIES failed validation. \n\n First error occurs on line: {errors[1][0]} \n Error Message: {errors[1][1]} \n \n For further details:")
        report_button.pack()
        xml.set_state(True)
        return


def generate_error_log(xml: XMLFile)-> None:
    save_path = filedialog.asksaveasfilename(
        filetypes=[("CSV Files", "*.csv")], defaultextension='.csv')
    if save_path == '':
        return
    with open(save_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(xml.error_log)
    os.startfile(save_path)
    


if __name__ == "__main__":

    root.mainloop()
