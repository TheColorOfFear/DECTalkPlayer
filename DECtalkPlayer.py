import sys
import os
import subprocess
import time
import atexit

details = True
debug = False

def exit_handler():
    try:
        for i in range(len(process_list)):
            process_list[i].kill()
    except:
        if details:
            print("error closing DECtalk windows")

if details:
    print("DECtalk Player v1.21 || 26 Jul 2023\n")

#choose config file name
conf_name = "index.cfg"
if len(sys.argv) >= 2:
    conf_name = sys.argv[1]
if details:
    print("loading from file \"" + conf_name + "\"...")

try:
    conf = open(conf_name, "r")
    relpath =  os.path.dirname(conf.name)
    if relpath != "":
        relpath += "/"
    if debug and details:
        print("file \"" + conf.name + "\" is in the relative directory \"" + relpath + "\"")
    config = conf.readlines()
    conf.close()
    length = (float(config[0]))
    
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
    if debug and details:
        print(startingLine)
    
    command_list = []
    try:
        for i in range(len(config) - startingLine):
            command_list.append([config[i+startingLine][0:8].strip(), (relpath + config[i+startingLine][9:].strip())])
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
                    if details:
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
                    if details:
                        print(command_list[i][1] + " - couldn't open \"" + command_list[i][0] + "\" window")
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
    if details:
        print("couldn't load \"" + conf_name + "\"")
if details:
    print("\nexiting program...")
