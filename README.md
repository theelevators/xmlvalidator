# PIES XML Validator

This is a simple xml validator use to validate PIES files using the XSD provided by the Auto Care Association.

App has a single window that provides a message and a menu bar.
Menu bar allows to open an XML file or to exit program.
Once a file has been opened, the validation process will being. 
The process starts by attempting to parse the loaded file. If the file is able to be parsed, the program will attempt to get and set the PIES Version.
This will allow the program to open the json file with the xsd locations and find the appropriate schema based on the PIES version.
When the program is able to get the schema, it will then do a file validation against the loaded schema.

![example_1](https://user-images.githubusercontent.com/121846740/232383218-a4099f32-482d-4073-b89d-3b080550579f.png)
![example_2](https://user-images.githubusercontent.com/121846740/232383220-ebc9c8eb-c168-4767-b7c0-b514a47121b7.png)


If any errors are generated while validating against the schema, a message will appear to the user.
This message will contain a small detail about what caused the file to fail validation as well as the line where it happened.
Another option will be granted to generate and save a csv file with all the errors found within the file.

![example_4](https://user-images.githubusercontent.com/121846740/232383222-49dffa00-3850-4181-beec-a2275b6a16d5.png)
![example_5](https://user-images.githubusercontent.com/121846740/232383223-d75a4434-1ee7-4aff-b870-ca4c35ba5885.png)

If the csv file is saved and generated, the program will automatically open the csv file.
The file contains 2 columns, first column contains the file lines where the error is occurring. 
Second column contains the error message generated.

![example_6](https://user-images.githubusercontent.com/121846740/232383224-ea95ce32-e4c2-48a2-8963-e15ceb239a22.png)


