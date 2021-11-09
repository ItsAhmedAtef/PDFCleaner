#!/usr/bin/env python3

###################
import sys
import os
###################

argv = sys.argv

original_file = open( argv[1], "rb" )

file_name = os.path.splitext(argv[1])[0]

file_extension = os.path.splitext(argv[1])[1]

new_name = file_name + "-cleaned" + file_extension

cleaned_file = open( new_name, "wb" )

found_title = True

found_dc_creator = False

for line in original_file:

   ##################################################################
   if "/Title(".encode('ascii') in line and found_title :
       Title = str(line).partition("/Title(")[2].split(')')[0]
       if "\\\\".encode('ascii') in Title.encode("ascii"):
           Title = Title.encode("ascii").decode('unicode-escape')
       print( "Title : \033[31m", Title, "\033[0m" )
       found_title = False
       if "--all" in argv or "--title" in argv:
           replace = "/Title(" + Title + ")"
           line = line.replace(replace.encode("ascii"), b"/Title()")
           print("\033[41mDeleted\033[0m")
   ##################################################################
   if "/Author(".encode('ascii') in line:
       Author = str(line).partition("/Author(")[2].split(')')[0]
       if "\\\\".encode('ascii') in Author.encode("ascii"):
           Author = Author.encode("ascii").decode('unicode-escape')
       print( "Author : \033[31m", Author, "\033[0m" )
       if "--all" in argv or "--author" in argv:
           replace = "/Author(" + Author + ")"
           line = line.replace(replace.encode("ascii"), b"/Author()")
           print("\033[41mDeleted\033[0m")
   ##################################################################
   if "/Creator(".encode('ascii') in line:
       Creator = str(line).partition("/Creator(")[2].split(')')[0]
       if "\\\\".encode('ascii') in Creator.encode("ascii"):
           Creator = Creator.encode("ascii").decode('unicode-escape')
       print( "Creator : \033[31m", Creator, "\033[0m" )
       if "--all" in argv or "--creator" in argv:
           replace = "/Creator(" + Creator + ")"
           line = line.replace(replace.encode("ascii"), b"/Creator()")
           print("\033[41mDeleted\033[0m")
   ##################################################################
   if "</dc:creator>".encode('ascii') in line:
       found_dc_creator = False
   if found_dc_creator:
       if "<rdf:li>".encode('ascii') in line:
           if "</rdf:li>".encode('ascii') in line:
               Creator = str(line).partition("<rdf:li>")[2].split('</rdf:li>')[0]
               print( "DC Creator : \033[31m", Creator, "\033[0m" )
               if "--all" in argv or "--creator" in argv:
                   replace = "<rdf:li>" + Creator + "</rdf:li>"
                   line = line.replace(replace.encode("ascii"), b"<rdf:li></rdf:li>")
                   print("\033[41mDeleted\033[0m")
   if "<dc:creator>".encode('ascii') in line:
       if "<rdf:li>".encode('ascii') in line:
           Creator = str(line).partition("<rdf:li>")[2].split('</rdf:li>')[0]
           print( "DC Creator : \033[31m", Creator, "\033[0m" )
           if "--all" in argv or "--creator" in argv:
               replace = "<rdf:li>" + Creator + "</rdf:li>"
               line = line.replace(replace.encode("ascii"), b"<rdf:li></rdf:li>")
               print("\033[41mDeleted\033[0m")
       elif "<dc:creator>\r\n".encode('ascii') in line:
           found_dc_creator = True
   ##################################################################
   if "/Producer(".encode('ascii') in line:
       Producer = str(line).partition("/Producer(")[2].split(')')[0]
       if False in Producer.encode("ascii"):
           Producer = Producer.encode("ascii").decode('unicode-escape')
       print( "Producer : \033[31m", Producer, "\033[0m" )
       if "--all" in argv or "--producer" in argv:
           replace = "/Producer(" + Producer + ")"
           line = line.replace(replace.encode("ascii"), b"/Producer()")
           print("\033[41mDeleted\033[0m")
   ##################################################################
   if "<pdf:Producer>".encode('ascii') in line:
       Producer = str(line).partition("<pdf:Producer>")[2].split('</pdf:Producer>')[0]
       if "\\\\".encode('ascii') in Producer.encode("ascii"):
           Producer = Producer.encode("ascii").decode('unicode-escape')
       print( "XML Producer : \033[31m", Producer, "\033[0m" )
       if "--all" in argv or "--producer" in argv:
           replace = "<pdf:Producer>" + Producer + "</pdf:Producer>"
           line = line.replace(replace.encode("ascii"), b"<pdf:Producer></pdf:Producer>")
           print("\033[41mDeleted\033[0m")
   ##################################################################
   if "/Keywords(".encode('ascii') in line:
       Keywords = str(line).partition("/Keywords(")[2].split(')')[0]
       if "\\\\".encode('ascii') in Keywords.encode("ascii"):
           Keywords = Keywords.encode("ascii").decode('unicode-escape')
       print( "Keywords : \033[31m", Keywords, "\033[0m" )
       if "--all" in argv or "--keywords" in argv:
           replace = "/Keywords(" + Keywords + ")"
           line = line.replace(replace.encode("ascii"), b"/Keywords()")
           print("\033[41mDeleted\033[0m")
   ##################################################################

   cleaned_file.write(line)

print("\033[32mA clean copy created without deleted Tags : \033[0m" + new_name)

original_file.close()
cleaned_file.close()
