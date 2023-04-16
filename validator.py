import tkinter as tk
from tkinter import ttk, filedialog
from lxml import etree


## Set schema files

SCHEMAS = {
    "6.7": "D:\Projects\WORK\PIES\PIES_6_7_(rev3)_XSD_20160915.xsd",
    "7.1": "D:\Projects\WORK\PIES\PIES_7_1_r4_XSD.xsd"
}


###### Set up gui theme and size ###########
root = tk.Tk()

style = ttk.Style()

BG_COLOR = "#299617"
LBL_COLOR = "#D3D3D3"
TXT_COLOR = "#DCDCDC"
FONT = "Helvetica 12 bold"
TITLE = "XML Validator"


w = 600
h = 400

root.resizable(False, False)

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()



x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

root.title(TITLE)
root.geometry("%dx%d+%d+%d" % (w, h, x, y))
root.config(bg=BG_COLOR)

style.configure("TLabelframe", background=LBL_COLOR)
style.configure(
    "TLabelframe.Label", font=FONT, background=LBL_COLOR, color=BG_COLOR
)

def set_file(obj: dict) -> str:
    file = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    file.replace("file:/", "")
    obj["file"] = file
    return f"Selected File: {file}"

def validate_file(obj: dict) -> str:
    valid = get_pies_version(obj)
    if valid != True:
        return valid
    file_schema = etree.parse(obj["schema"])
    xml_schema = etree.XMLSchema(file_schema)
    xml_file = etree.parse(obj["file"])
    try:
        xml_schema.assertValid(xml_file)
        obj['validated'] = True
        return "Validation Complete. File has passed validation!"
    except etree.DocumentInvalid:
        obj['validated'] = False
        for error in xml_schema.error_log:
            print("  Line {}: {}".format(error.line, error.message))
   
def get_pies_version(obj: dict)-> bool|str:
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

message_frame = ttk.Labelframe(root, text="Validation Message")
message_frame.pack(fill="both", expand=True, side="left")
message_frame.propagate(False)

message = tk.Label(
    message_frame,
    text="Make A Selection To Start Validation.",
    background=LBL_COLOR,
)
message.pack(fill="both", expand=True)
message.propagate(False)
message.configure(wraplength=375)

# Set up holder for files
obj = {"file": "", "schema": "", "validated": False, "importLog": [],
        "records": [], "prepared": False, "parsed": False, "completed": False}

button_frame = tk.Frame(root, background=LBL_COLOR)
button_frame.pack(fill="y", side="right")
file_button = tk.Button(
    button_frame,
    text="Load XML",
    command=lambda: message.config(text=set_file(obj)),
    height=3,
    width=14,
    background=TXT_COLOR,
)
file_button.pack(side="top")
validation_button = tk.Button(
    button_frame,
    text="Validate XML",
    command=lambda: message.config(text=validate_file(obj)),
    height=3,
    width=14,
    background=TXT_COLOR,
)
validation_button.pack(side="top")


if __name__ == "__main__":
    

   root.mainloop()