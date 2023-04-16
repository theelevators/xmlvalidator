import tkinter as tk
from tkinter import ttk, filedialog
from lxml import etree


## Set schema files
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


def set_schema(obj: dict) -> str:

    schema = filedialog.askopenfilename(filetypes=[("Schema Files", "*.xsd")])
    schema.replace("file:/", "")
    obj["schema"] = schema

    return f"Selected Schema: {schema}"

def set_file(obj: dict) -> str:
    file = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    file.replace("file:/", "")
    obj["file"] = file

    return f"Selected File: {file}"

def validate_file(obj: dict) -> str:
    if obj['file'] == '' or obj['schema'] == '':
        return "Please enter a valid file and schema."
    file_schema = etree.parse(obj["schema"])
    schema = etree.XMLSchema(file_schema)
    parser = etree.XMLParser(schema=schema)
    try:
        etree.parse(obj["file"], parser)
        obj['validated'] = True
        return "Validation Complete. File has passed validation!"
    except etree.DocumentInvalid:
        errors = ''
        for error in schema.error_log:
            errors += "  Line {}: {}".format(error.line, error.message)
        obj['validated'] = False
        return errors
    except etree.XMLSyntaxError as e:
        obj['validated'] = False
        return e.msg



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
schema_button = tk.Button(
    button_frame,
    text="Load XSD",
    command=lambda: message.config(text=set_schema(obj)),
    height=3,
    width=14,
    background=TXT_COLOR,
)
schema_button.pack(side="top")
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