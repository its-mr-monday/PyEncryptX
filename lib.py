#
#   EncryptX Function Library Module v 1.1
#   
#
#
#

import os
import sys
import platform


def sysCheck(): #tells what system the user is running
    pctype = platform.system()
    if pctype == "Darwin":
        pctype = "MacOS"
    return pctype

def passwCheck(passw):  #checks if the password is > 1
    if len(passw) >=1:
        return True
    else:
        return False

def splitPath(path_to_file):    #returns a tuple with the filename and the path to the root dir of the file
    split_path = os.path.split(path_to_file)
    return split_path
    
def checkExistance(file_path):   #Checks if a file exists in the current directory
    if len(file_path)>=1:
        check1 = os.path.exists(file_path)  #make sure that this path is one that exists
        if check1 is True:
            if os.path.isfile(file_path) is True:   #if it is a file then were good to go
                return True
            else:
                return False    #if it aint a file then we cant encrypt it
        else: #There isnt a file then
            return False
    else:
        return False #Cant be a file if the path has 0 characters