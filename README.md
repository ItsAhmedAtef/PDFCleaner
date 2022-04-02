# PDFCleaner
Python script to remove PDF metadata tags

### Overview
- Simple Python libraries, Just "sys" and "os".
- Original PDF will not be edited.
- New file will be created with unwanted chosen metadata tags.
- You can remove PDF [ Title - Producer - Author - Creator ] tags

### Usage
```py3
python3 ./PDFCleaner.py PDFNAME.pdf --all
```
### Options
- ```--all```
- ```--author```
- ```--creator```
- ```--producer```
- ```--title```
