import sys
import subprocess
import time
import atexit

def exit_handler():
    try:
        for i in range(len(process_list)):
            process_list[i].kill()
    except:
        print("error closing DECtalk windows")

print("DECtalk Player v1.1 || 26 Jul 2023\n")

details = True
debug = True

#choose config file name
conf_name = "index.cfg"
if len(sys.argv) >= 2:
    conf_name = sys.argv[1]
if details:
    print("loading from file \"" + conf_name + "\"...")

try:
    conf = open(conf_name, "r")
    config = conf.readlines()
    conf.close()
    length = (float(config[0]))
    command_list = []
    try:
        for i in range(len(config) - 1):
            command_list.append([config[i+1][0:8].strip(), config[i+1][9:].strip()])
        if details:
            print("file names and dependancies:")
            i = 0
            for i_fake in range(len(command_list)):
                if debug:
                    print(i_fake, i, len(command_list))
                if i < len(command_list):
                    print(command_list[i][1] + " - " + command_list[i][0])
                    try:
                        path_check = open(command_list[i][1], "r")
                        path_check.close()
                        i += 1
                    except:
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
    print("couldn't load \"" + conf_name + "\"")

print("\nexiting program...")