#!/usr/bin/env python3

###################
import sys
import os
###################

# for CMD colored output
os.system("color")

def red(string):
    return  "\x1b[31m" + string + "\x1b[0m"

def yellow(string):
    return  "\x1b[33m" + string + "\x1b[0m"

def green(string):
    return  "\x1b[32m" + string + "\x1b[0m"

def blue(string):
    return  "\x1b[34m" + string + "\x1b[0m"

argv = sys.argv
allowed_parameters = ["--all","--title","--creator","--author","--producer"]

def handle_replace(binary_keyword, line):
    # ex: b"/Author" in this binary line
    if binary_keyword in line:
        splited = line.split(binary_keyword)[1]
        
        keyword_content = bytearray()
        keyword_code = binary_keyword
        index = 0
        opened = False
        closed = False
        escaped = False
        for i in splited:
            if ( opened and closed==False ):
                if ( splited[index:].startswith(b")") ):
                    if ( not escaped ):
                        closed=True
                    else:
                        keyword_content.append(i)
                else:
                    keyword_content.append(i)
                
                if (escaped):
                    escaped=False
                else:
                    if ( splited[index:].startswith(b"\\") ):
                        escaped=True
            elif ( opened==False and closed==False ):
                if (splited[index:].startswith(b"(")):
                    opened=True
                else:
                    keyword_code += b" "
            index +=1
        
        keyword_code += b"(" + keyword_content + b")"
        line =  line.replace( keyword_code, binary_keyword + b"()" )
        keyword_content = keyword_content.decode(encoding="utf-8", errors="ignore")
        print( blue(binary_keyword.decode()[1:]) + ": \"" + keyword_content + "\" " + red("(deleted)"))
        return line

def clean( file, list_arguments ):
    file_path, filename = os.path.split(file)
    new_name = os.path.splitext(filename)[0] + "_cleaned.pdf"
    new_path_name = os.path.join(file_path, new_name)
    try:
        original_file = open( file, "rb")
    except:
        sys.exit(red("Error: Couldn't read \"" + file + "\" file!"))
    try:
        new_file = open( new_path_name, "wb")
        print(green("Output saved in ") + new_path_name)
    except:
        original_file.close()
        if file_path:
            print(file_path)
            sys.exit(red("Error: Directory " + file_path + " is not writable!"))
        else:
            sys.exit(red("Error: The current directory is not writable!"))
    ##############################
    title_not_found = True
    creator_not_found = True
    author_not_found = True
    producer_not_found = True
    for line in original_file:
        ##### ##### Title ##### #####
        if (("--all" in list_arguments or "--title" in list_arguments) and title_not_found):
            check = handle_replace(b"/Title", line)
            if (check != None):
                line = check
                title_not_found = False
        ##### ##### Creator ##### #####
        if (("--all" in list_arguments or "--creator" in list_arguments) and creator_not_found):
            check = handle_replace(b"/Creator", line)
            if (check != None):
                line = check
                creator_not_found = False
        ##### ##### Author ##### #####
        if (("--all" in list_arguments or "--author" in list_arguments) and author_not_found):
            check = handle_replace(b"/Author", line)
            if (check != None):
                line = check
                author_not_found = False
        ##### ##### Producer ##### #####
        if (("--all" in list_arguments or "--producer" in list_arguments) and producer_not_found):
            check = handle_replace(b"/Producer", line)
            if (check != None):
                line = check
                producer_not_found = False
        new_file.write(line)
    ##############################
    original_file.close()
    new_file.close()
    sys.exit(green("Finished"))

def detect_argv(file):
    del argv[1] # remove this the bigger index first
    del argv[0]
    hold_list_arguments = []
    if ( argv ):
        for parameter in argv:
            if (parameter in allowed_parameters):
                hold_list_arguments.append(parameter)
            else:
                print(yellow("Warning: Unknown argument \"" + parameter + "\""))
    clean(file, hold_list_arguments)

if ( len(argv) > 1 ):
    file = argv[1]
    if ( os.path.exists(file) and os.path.isfile(file) ):
        if (os.path.splitext(file)[1] != ".pdf"):
            # bad extension
            sys.exit(red("Error: \"" + file + "\" is not a PDF file!"))
        detect_argv(file)
    else:
        sys.exit(red("Error: Couldn't read \"" + file + "\" file!"))
else:
    sys.exit(red("Error: No arguments provided!"))
