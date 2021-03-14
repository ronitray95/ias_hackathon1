'''initial program to application developer to check login and upload algorithms
author : rbachina
date : 14 mar 2021
purpose : team hackathon
'''
#!/usr/bin/python3
import os
import pymongo
from pymongo import MongoClient
from subprocess import call



def __copy_alg_to_repo__(destinationDir):
    print(" \n")
    sourceDir = input("Provide source directory/folder: ")
    call(['cp', '-r', sourceDir, destinationDir])
    print("Algorithm is hosted now")
    __app_dev_operations__()

def __list_all_alg__(algRepPath):
    __repo_exist__(algRepPath)
    my_algorithms = os.listdir(algRepPath)
    print(my_algorithms)

def __delete_alg__(dirNameWithFullPath):
    try: 
        os.rmdir(dirNameWithFullPath) 
        print("algorithm removed successfully") 
    except OSError as error: 
        print(error) 
        print("Error deleting the algorithm") 

def __repo_exist__(algRepPath):
    isExist = os.path.exists(algRepPath)
    if not isExist: 
        print("creating dir now")
        os.makedirs(algRepPath)

def __upload_algorithm__(algRepPath):
    __repo_exist__(algRepPath)
    __copy_alg_to_repo__(algRepPath)

def __newUser_registration__(userName,name,password):
    client = MongoClient("mongodb+srv://admin:admin123@cluster0.ze4na.mongodb.net/myFirstDatabase")
    db = client['IOT']
    TexDB = db['user_details']
    mydict = {'userid':userName, 'name': name, 'password': password}
    x = TexDB.insert_one(mydict)
    print(x)

def __validation__(userName,password):
    client = MongoClient("mongodb+srv://admin:admin123@cluster0.ze4na.mongodb.net/myFirstDatabase")
    db = client['IOT']
    UserDB = db['user_details']
    
    for x in UserDB.find( {'userid': userName, 'password': password } ):
        print(x)
    
    if x['password'] != password:
        print("please enter proper credentials, userid/password wrong")
        login()
    else:
        print("login successful")
        __app_dev_operations__()



def __app_dev_operations__():
    print('Select "1" to upload algorithm \n')
    print('Select "2" list the algorithms from repo \n')
    print('Select "3" delete algorithms from repo \n')
    print('Select "4" to logout and exit \n')
    devChoice = input("Choice: ")
    homePath=os.environ['HOME']
    algRepPath=homePath+"/AlgorithmRepo"
    if devChoice=="1":
        __upload_algorithm__(algRepPath)
    elif devChoice=="2":
        __list_all_alg__(algRepPath)
        __app_dev_operations__()
    elif devChoice=="3":
        __list_all_alg__(algRepPath)
        deleteDirName = input("Enter Dir Name: ")
        dirNameWithFullPath = algRepPath+'/'+deleteDirName
        __delete_alg__(dirNameWithFullPath)
        __list_all_alg__(algRepPath)
        __app_dev_operations__()
    elif devChoice=="4":
        exit()
    else:
        print("please select appropriate choice")
        __app_dev_operations__()
        

def registration():
    userName = input("Enter Username: ")
    name = input("Enter Full Name: ")
    password = input("Enter Password: ")
    print(userName +"\n" + name + "\n" + password)
    __newUser_registration__(userName,name,password)
    print("registration successful")
    print("Now please login with your credentials \n")
    login()

def login():
    userName = input("Enter Username: ")
    password = input("Enter password: ")
    __validation__(userName,password)



def main():
    print('****************Welcome to IOT Platform****************')
    print('Please enter appropriate action from below choice \n')
    print('Select "1" for new user registration \n')
    print('Select "2" for existing user login \n')
    print('Select "3" to exit')
    userChoice = input("Choice: ")

    if userChoice=="1":
        registration()
    elif userChoice=="2":
        login()
    elif userChoice=="3":
        exit()
    else:
        print("please select appropriate choice")

if __name__=="__main__":
    main()

