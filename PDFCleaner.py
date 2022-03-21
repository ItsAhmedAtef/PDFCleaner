#!/usr/bin/env python3

###################
import sys
import os
###################

argv = sys.argv
allowed_parameters = ["--all","--title","--creator","--author","--producer"]

def handle_replace(binary_keyword, line):
    # ex: b"/Author" in this binary line
    if binary_keyword in line:
        # split the line
        keyword_split = str(line).split(binary_keyword.decode())
        # check if the complete code is in the same line, avoid out of range errors
        if ( (len(keyword_split) > 0) and (len(keyword_split[1].split("(")) > 0) and (len(keyword_split[1].split("(")[1].split(")")) > 0) ):
            # cuted string content value
            keyword_content = keyword_split[1].split("(")[1].split(")")[0]
            keyword_code = binary_keyword + line.split(binary_keyword)[1].split(b")")[0] + b")"
            line =  line.replace( keyword_code, binary_keyword + b"()" )
            print( binary_keyword.decode()[1:] + ": \"" + keyword_content + "\" (deleted)")
            return line

def clean( file, list_arguments ):
    file_path, filename = os.path.split(file)
    new_name = os.path.splitext(filename)[0] + "_cleaned.pdf"
    new_path_name = os.path.join(file_path, new_name)
    try:
        original_file = open( file, "rb")
    except:
        sys.exit("Error: Couldn't read \"" + file + "\" file!")
    try:
        new_file = open( new_path_name, "wb")
        print("Created new file " + new_name)
    except:
        original_file.close()
        sys.exit("Error: directory " + file_path + " is not writable!")
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
    sys.exit("Finished")

def detect_argv(file):
    del argv[1] # remove this the bigger index first
    del argv[0]
    if ( argv ):
        hold_list_arguments = []
        for parameter in argv:
            if (parameter in allowed_parameters):
                hold_list_arguments.append(parameter)
            else:
                print("Warning: Unknown argument \"" + parameter + "\"")
        if ("--all" in hold_list_arguments):
            # if --all is provided ? then no need to anything else
            hold_list_arguments = ["--all"]
        clean(file, hold_list_arguments)
    else:
        clean(file, ["--all"])

if ( len(argv) > 1 ):
    file = argv[1]
    if ( os.path.exists(file) and os.path.isfile(file) ):
        if (os.path.splitext(file)[1] != ".pdf"):
            # bad extension
            sys.exit("Error: \"" + file + "\" is not a PDF file!")
        detect_argv(file)
    else:
        sys.exit("Error: Couldn't read \"" + file + "\" file!")
else:
    sys.exit("Error: No arguments provided!")
