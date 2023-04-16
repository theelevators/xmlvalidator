import os
import tkinter as tk
from tkinter import ttk, filedialog, Menu
from lxml import etree
import csv


# Set schema files

SCHEMAS = {
    "6.7": "D:\Projects\WORK\PIES\PIES_6_7_(rev3)_XSD_20160915.xsd",
    "7.1": "D:\Projects\WORK\PIES\PIES_7_1_r4_XSD.xsd"
}

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


menubar = Menu(root, background=LBL_COLOR, activebackground=LBL_COLOR,
               foreground=LBL_COLOR, activeforeground=LBL_COLOR, bg=LBL_COLOR)
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


def set_file(obj: dict) -> str:
    file = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    file.replace("file:/", "")

    if file == '':
        if obj["file"] != '':
            return f"File: \n {file}"
        return "Open a file to begin."

    obj["file"] = file
    filemenu.entryconfig("Errors", state="disabled")
    return f"File: \n {file}"


def open_error_log(obj: dict) -> None:
    if obj['errors'] == '':
        return
    os.startfile(obj['errors'])


def validate_file(obj: dict) -> str:
    valid = get_pies_version(obj)
    if valid != True:
        return valid
    file_schema = etree.parse(obj["schema"])
    xml_schema = etree.XMLSchema(file_schema)
    xml_file = etree.parse(obj["file"])
    file_name = obj["file"]
    file_name = file_name.replace('.xml', '').replace(
        'D:/Projects/WORK/PIES/', '')

    try:
        xml_schema.assertValid(xml_file)
        obj['validated'] = True
        return "Validation Complete. File has passed validation!"
    except etree.DocumentInvalid:
        obj['validated'] = False
        errors = [[error.line, error.message]
                  for error in xml_schema.error_log]
        errors.insert(0, ["Line Number", "Error Message"])
        with open(f'errors_{file_name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(errors)
        filemenu.entryconfig("Errors", state="normal")
        obj['errors'] = f"errors_{file_name}.csv"
        return f"File failed schema validation. \n Please review the errors in: errors_{file_name}.csv"


def get_pies_version(obj: dict) -> bool | str:
    namespace = '{http://www.autocare.org}'
    if obj['file'] == '':
        return "Please enter a valid file."
    try:
        tree = etree.parse(obj['file'])
    except etree.XMLSyntaxError as error:
        return f"File failed validation on line: {error.lineno}. \n Error message: {error.msg}."
    try:
        root = tree.getroot()
        pies = root.find(f"./{namespace}Header/{namespace}PIESVersion").text
        obj["schema"] = SCHEMAS[pies]
        return True
    except Exception as error:
        return f"Unable to validate file due to invalid XML structure and/or namespace."


message = tk.Label(
    root,
    text="Open a file to begin.",
    background=LBL_COLOR,
)
message.pack(fill="both", expand=True)
message.propagate(False)
message.configure(wraplength=375)

# Set up holder for files
obj = {"file": "", "schema": "", "validated": False, "importLog": [],
       "records": [], "prepared": False, "parsed": False, "completed": False, "errors": ""}

filemenu = Menu(menubar, background=LBL_COLOR, tearoff=0)
filemenu.add_command(
    label="Open", command=lambda: message.config(text=set_file(obj)))
filemenu.add_command(label="Errors", command=lambda: open_error_log(obj))
filemenu.entryconfig("Errors", state="disabled")
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
menubar.add_command(
    label="Validate", command=lambda: message.config(text=validate_file(obj)))

root.config(menu=menubar)

if __name__ == "__main__":

    root.mainloop()
