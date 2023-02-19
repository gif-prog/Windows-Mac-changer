import subprocess
import re
import os
import pyfiglet
def display_table():
    global listed
    listed = os.popen("getmac /v /FO TABLE | findstr /V Media").read().splitlines()[3:]
    global i
    i = 0
    print("------------------------------------------------------------------------------------------------------------")
    for line in listed:
        print("{0} | {1}".format(i,line))
        i+=1

def restart_interface():
    listed1 = os.popen("netsh interface show interface | findstr /V Disconnected").read().splitlines()[3:-1]
    j = 0
    for line in listed1:
        print("{0} {1}".format(j, ' '.join(line.split()[3:])))
        j += 1
    print("{0} {1}".format(j,"Go back"))
    print()
    opt = int(input("Select: "))
    os.system("cls")
    if (opt == j):
        return
    else:
        line = listed1[opt]
        interface = ' '.join(line.split()[3:])
        print("Trying to stop interface...")
        stop = subprocess.run(["netsh", "interface", "set", "interface", interface, "disable"])
        print("Trying to start interface...")
        start = subprocess.run(["netsh", "interface", "set", "interface", interface, "enable"])


def get_reg_path(option):
    print(i,"| Go Back")
    print()
    opt = int(input("Select option: "))
    os.system("cls")
    if (opt == i):
        return
    id = ''.join(re.findall(r"{.*}", listed[opt]))
    command1 = "reg query HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class /s /f " + id[1:9]
    path = os.popen(command1).read().splitlines()[1]
    path = ''.join(path)
    path = path.replace("\\\\",'\\')
    if(option == 1):
        if (verify(path,id,1)):
            change_mac(path)
            restart_interface()
        else:
            print("<- Couldn't change it. Something seems broken. ->")
    if(option == 2):
        if (verify(path, id, 2)):
            restore_mac(path)
            restart_interface()

        else:
            print("<- This interface has original address already ->")



def verify(path,id,option):

    if(option == 1):
        command2 = "reg query " + path + " /v NetCfgInstanceId"
        real_id = ''.join(re.findall(r"{.*}", os.popen(command2).read().splitlines()[2]))
        if (real_id == id):
            return 1
        else:
            return 0
    elif(option == 2):
        try:
            command4 = "reg query " + path + " /v OriginalNetworkAddress"
            og_mac = os.popen(command4).read().splitlines()[2].split()[2].replace("-", "")
            command5 = "reg query " + path + " /v NetworkAddress"
            edited_mac = os.popen(command5).read().splitlines()[2].split()[2]
            if (og_mac != edited_mac):
                return 1
            else:
                return 0
        except:
            return 0
def change_mac(path):
    try:
        input_mac = input("Enter the MAC: ").replace(":","").replace("-","")
        for i in range(len(input_mac)):
            if (input_mac[i] > 'F'):
                result = 0
                break
            else:
                result = 1
        if(len(input_mac)==12 and result):
            command3 = "reg add "+path+" /v NetworkAddress /t REG_SZ /d "+input_mac
            subprocess.run(["reg","add",path,"/v","NetworkAddress","/t","REG_SZ","/d",input_mac])
        else:
            print("<- Invalid Mac Address ->")
            return
    except:
        print("Error")


def main():
    os.system("cls")
    print("Made by")
    print(pyfiglet.figlet_format("Gifton Paul Immanuel"))
    print()
    print("""
                /\\
/vvvvvvvvvvvv \--------------------------------------,
`^^^^^^^^^^^^ /====================================="
            \/
    """)
    print("* Do run this script as an Administrator")
    print("* Do install all the requirements in requirements.txt")
    print("* Make sure that the interface that you wanted to change is active")
    while(1):
        print("------------------------------------------------------------------------------------------------------------")
        print("| 0 DISPLAY CURRENT MAC ADDRESS |")
        print("| 1 CHANGE EXISTING MAC ADDRESS |")
        print("| 2 RESTORE CHANGED MAC ADDRESS |")
        print("| 3 RESTART AN INTERFACE [NETSH]|")
        print("| 4            EXIT             |")
        print()
        option = int(input("Select the option: "))
        print()
        os.system("cls")
        match option:
            case 0:
                display_table()
            case 1:
                display_table()
                get_reg_path(1)
            case 2:
                display_table()
                get_reg_path(2)
            case 3:
                restart_interface()
            case 4:
                print("""
              . . .                         
              \|/                          
            `--+--'                        
              /|\                          
             ' | '                         
               |                           
               |                           
           ,--'#`--.                       
           |#######|                       
        _.-'#######`-._                    
     ,-'###############`-.                 
   ,'#####################`,               
  /#########################\              
 |###########################|             
|#############################|            
|#############################|            
|#############################|            
|#############################|            
 |###########################|             
  \#########################/              
   `.#####################,'               
     `._###############_,'                 
        `--..#####..--'
                      """)
                print("THANKS FOR USING THIS TOOL !")
                return 0

def restore_mac(path):
    subprocess.run(["reg","delete",path,"/v","NetworkAddress"])
main()