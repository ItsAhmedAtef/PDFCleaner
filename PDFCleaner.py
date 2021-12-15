#!/usr/bin/env python3

###################
import sys
import os
###################

argv = sys.argv
allowed_parameters = ["--all","--title","--creator","--author","--producer"]

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
    found_first_title = False
    for line in original_file:
        ##### ##### Title ##### #####
        if ("--all" in list_arguments or "--title" in list_arguments):
            if (found_first_title == False):
                if "/Title(".encode("unicode-escape") in line:
                    found_first_title = True
                    Title = line.decode("unicode-escape").split("/Title(")[1].split(")")[0]
                    title_code = "/Title("+Title+")"
                    line = line.replace(title_code.encode(), b"/Title()")
                    print("Title: \"" + Title + "\" (deleted)")
        ##### ##### Creator ##### #####
        if ("--all" in list_arguments or "--creator" in list_arguments):
            if "/Creator(".encode("unicode-escape") in line:
                Creator = line.decode("unicode-escape").split("/Creator(")[1].split(")")[0]
                creator_code = "/Creator("+Creator+")"
                line = line.replace(creator_code.encode(), b"/Creator()")
                print("Creator: \"" + Creator + "\" (deleted)")
        ##### ##### Author ##### #####
        if ("--all" in list_arguments or "--author" in list_arguments):
            if "/Author(".encode("unicode-escape") in line:
                Author = line.decode("unicode-escape").split("/Author(")[1].split(")")[0]
                author_code = "/Author("+Author+")"
                line = line.replace(author_code.encode(), b"/Author()")
                print("Author: \"" + Author + "\" (deleted)")
        ##### ##### Producer ##### #####
        if ("--all" in list_arguments or "--producer" in list_arguments):
            if "/Producer(".encode("unicode-escape") in line:
                Producer = line.decode("unicode-escape").split("/Producer(")[1].split(")")[0]
                producer_code = "/Producer("+Producer+")"
                line = line.replace(producer_code.encode(), b"/Producer()")
                print("Producer: \"" + Producer + "\" (deleted)")
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
