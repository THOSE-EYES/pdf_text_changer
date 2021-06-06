# Simple Python PDF Text Replacer
Replace text in PDF from the command line using Python.


## Installation
The program is written using PyPDF2 library. To install run : 
```
$ pip install pypdf2
```

And then clone the repository to use the script.

## Example of use
The program can used as a standalone script like described below :
```
python replacer.py -i <pdf> -r '<JSON-object like { "data" : "replacer" }>'
```

Or it can be referenced by other scripts using import.
