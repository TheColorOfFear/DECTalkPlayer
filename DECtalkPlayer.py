import sys
import os
import subprocess
import time
import atexit

#configuration#
CFG_ver = 1.0
show_metadata = True
details = True
details_error = True
if details:
    details_error = True
debug = True

def exit_handler():
    try:
        for i in range(len(process_list)):
            process_list[i].kill()
    except:
        if debug:
            raise
        if details_error:
            print("error closing DECtalk windows")

def read_metadata():
    print("")
    if version == 0.0:
        for i in range(len(config)):
            if config[i].strip() == "!FILES!":
                break
            else:
                print(config[i].strip())
    else:
        metadata_temp = 0
        for i in range(len(config)):
            if config[i+1].strip() == "!FILES!":
                break
            elif metadata_temp == 1:
                print(config[i+1].strip())
            elif config[i+1].strip() == "!META!":
                metadata_temp = 1



if details:
    print("DECtalk Player PR v1.1.0 || 06 Aug 2023\n")

#choose config file name
conf_name = ""
if len(sys.argv) >= 2:
    conf_name = sys.argv[1]
else:
    conf_name = input("Path to config file : ")
if details:
    print("loading from file \"" + conf_name + "\"...")

try:
    conf = open(conf_name, "r")
    relpath =  os.path.dirname(conf.name)
    if relpath != "":
        relpath += "/"
    if debug and (details):
        print("file \"" + conf.name + "\" is in the relative directory \"" + relpath + "\"")
    config = conf.readlines()
    conf.close()
    length = (float(config[0]))
    
    try:
        version = (float(config[1]))
        #if cfg version is newer than the CFG_ver, alert user.
        if version > CFG_ver:
            if details_error:
                print("CFG version newer than supported. It may not work with your version of DtP")
    except:
        version = 0.0
        if details_error:
            print("ERROR : No version for CFG file. It may not work with your version of DtP.")
    if debug:
        print("cfg version", version, "\nmax cfg version", CFG_ver)
    
    #find where the files start
    startingLine = 0
    for i in range(len(config)):
        if config[i].strip() == "!FILES!":
            break
        else:
            startingLine += 1
    startingLine += 1
    if startingLine >= len(config):
        startingLine = 1
    if debug and (details):
        print(startingLine)
    
    command_list = []
    try:
        if version == 0.0:
            for i in range(len(config) - startingLine):
                command_list.append([config[i+startingLine][0:8].strip(), (relpath + config[i+startingLine][9:].strip()).replace("\\","/")])
            if details:
                print("file names and dependencies:")
            i = 0
            for i_fake in range(len(command_list)):
                if debug and details:
                    print(i_fake, i, len(command_list))
                if i < len(command_list):
                    if details:
                        print(command_list[i][1] + " - " + command_list[i][0])
                    try:
                        path_check = open(command_list[i][1], "r")
                        path_check.close()
                        i += 1
                    except:
                        if details_error:
                            print("file \"" + command_list[i][1] + "\" not found")
                        command_list.pop(i)
        try:
            #run/stop speak_us.exe with all the files
            process_list = []
            atexit.register(exit_handler)
            for i in range(len(command_list)):
                try:
                    process_list.append(subprocess.Popen(command_list[i], start_new_session=True, shell=False))
                except:
                    if debug:
                        raise
                    if details_error:
                        print(command_list[i][1] + " - couldn't open \"" + command_list[i][0] + "\" window")
            
            if (startingLine != 1) and show_metadata:
                read_metadata()
            time.sleep(length)
        except:
            if debug:
                raise
    except:
        if debug:
            raise
except:
    if debug:
        raise
    if details_error:
        print("couldn't load \"" + conf_name + "\"")
if details:
    print("\nexiting program...")
