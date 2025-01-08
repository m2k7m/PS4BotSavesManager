
import zipfile
import os
import shutil
import gdown
import time
import json

USBdata={}

if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        config = json.load(f)
else:
    config = {}

second_run = False

def SaveSitting(zipname:str = None):
    global second_run
    if not os.path.exists('config.json') or zipname == "save":
        sit = input("Do You Want Keep ZIP Files? (Y or N): ")
        if sit.upper() == "Y":
            config["Save"] = True
        elif sit.upper() == "N":
            config["Save"] = False
    
        with open("config.json", "w") as f:
            json.dump(config, f,indent=4)
    
    elif config["Save"] is False and zipname:
        os.remove(zipname)
        print(f"\033[0;31m{zipname}\033[32m Removed Successfully.\033[0m")
    
    elif second_run == True:
        input("Anything Else? ")
        second_run = False
        main()

def CheckUSB():
    if USBdata:
        for usb,data in USBdata.items():
            letter = data['letter']
            system = data['system']
            name = data['name']
            size = data['size']
            print(f"\033[32mPrepareing {name} - {size} USB ...\033[0m")
            return letter,system,name,size
    usb = os.popen("wmic logicaldisk where drivetype=2 get filesystem,volumename,deviceid,Size").read()
    if usb.find("DeviceID") != -1:
        if usb.split("\n")[4]:
            Number = input("USB Number(Defult Is The First USB): ")
            if Number == "":
                Number = 0
            elif not Number.isdigit():
                print(f"\033[0;31m{Number} Is Not a Number Please Try Again\033[0m")
                Number = 0
                CheckUSB()
            else:
                Number =int(Number)
        else:
            Number = 0
        
        def filterNumbers(num):
            if num == 0 :
                return 1
            elif (num % 2) == 0: 
                return num + 1
            else:
                return num
        
        def CalculateDiskSize(bytes):
            gibibytes = bytes / (1024 * 1024 * 1024)
            return f"{gibibytes:.2f} GB"
        
        Number = filterNumbers(Number)
        try:
            nusb = usb.split("\n")[Number + 1 ]
            letter = nusb.split(" ")[0]
            system = nusb.split(" ")[8]
            size = CalculateDiskSize(int(nusb.split(" ")[15]))
            name = nusb.split(" ")[17]
            USBdata["USB"] = {
                    "letter": letter,
                    "system": system,
                    "size":size,
                    "name":name
                    }
            return letter,system,name,size
        except IndexError:
            print(f"\033[0;31mThere's No {Number}th USB, Please Try Again\033[0m")
            CheckUSB()
    else:
        os.system('cls' if os.name=='nt' else 'clear')
        print("\033[0;31mThere's No USB, Waiting for a USB ...")
        while True:
            usb = os.popen("wmic logicaldisk where drivetype=2 get filesystem,volumename,deviceid,Size").read()
            if usb.find("DeviceID") != -1:
                letter = usb.split("\n")[2].split(" ")[0]
                system = usb.split("\n")[2].split(" ")[8]
                size = CalculateDiskSize(int(usb.split("\n")[2].split(" ")[15]))
                name = usb.split("\n")[2].split(" ")[17]
                USBdata["USB"] = {
                    "letter": letter,
                    "system": system,
                    "size":size,
                    "name":name
                    }
                return letter,system,name,size
            time.sleep(5)

def fromZiptoUSB(zipname:str):
    global second_run
    check = CheckUSB()
    if check:
        with zipfile.ZipFile(zipname) as newzip:
            print(f"\033[32mPrepareing {zipname} ...\033[0m")
            if newzip.filelist[0].filename.startswith("PS4/"):
                newzip.extractall(check[0])
                print("\033[32mYour PS4 Save Is Ready, Enjoy <3")
            else:
                newzip.extractall(check[0])
                shutil.copytree(check[0] + newzip.filelist[0].filename,check[0],dirs_exist_ok=True)
                shutil.rmtree(check[0] + newzip.filelist[0].filename)
                print(f"\033[32mYour Save Moved To {check[2]} - {check[3]}, Enjoy <3")
        second_run = True
        SaveSitting(zipname)

def fromGDrivetoUSB(url:str):
    if url.startswith("https://drive.google.com/file/d/"):
        if url.endswith("/edit") or url.endswith("/view?usp=sharing"):
            file_id = url.split("/d/")[1].split("/")[0]
        else:
            file_id = url.split("/d/")[1]
    elif url.startswith("https://drive.google.com/uc?id=") or url.startswith("https://drive.usercontent.google.com/download?id="):
        file_id = url.split("=")[1].split("&")[0]
    elif "folders" in url:
        return input("\033[0;31mSorry, It Should Be ZIP File.")
    print("\033[32mWaiting For Download ...\033[0m")
    dzip = gdown.download("https://docs.google.com/uc?export=download&id=" + file_id)
    if dzip.endswith(".zip"):
        fromZiptoUSB(dzip)
    else:
        SaveSitting(dzip)
        input("\033[0;31mThe Link Is Not For a Save.")

def format(usbdata:list):
    check = USBFiles(usbdata[0])
    if not check:
        time.sleep(3)
        main()
    cmd = f"format {usbdata[0]} /FS:{usbdata[1]} /Q /V:{usbdata[2]} /y"
    os.system(cmd)
    os.system('cls' if os.name=='nt' else 'clear')
    print(f"\033[32m{usbdata[2]} Has Been Formatted Successfully\033[0m")
    time.sleep(3)
    main()

def USBFiles(usbletter: str):
    files = os.listdir(usbletter)
    if files == ['System Volume Information']:
        return print("\033[0;31mThere are no files in the USB.\033[0m")
    files.remove("System Volume Information")
    return files

def AutoCorrection(Word:str,database={"format","changeusb","savesettings"},simlimit:int = 0.4):
    def createBigram(word:str):
        return [word[i] + word[i+1] for i in range(len(word)-1)]

    def getSim(FirstWord:str,SecondWord:str):
        FirstWord,SecondWord = FirstWord.lower(),SecondWord.lower()

        Sim = []
        FirstBigram,SecondBigram = createBigram(FirstWord),createBigram(SecondWord)

        for i in range(len(FirstBigram)):
            try:
                SecondBigram.index(FirstBigram[i])
                Sim.append(FirstBigram[i])
            except:
                continue

        return len(Sim)/max(len(FirstBigram),len(SecondBigram))
    
    max_sim = 0.0

    for data_word in database:
        cur_sim = getSim(Word,data_word)
        if cur_sim > max_sim:
            max_sim = cur_sim
            most_sim_word = data_word
    
    return most_sim_word if max_sim>simlimit else Word

def main():
    os.system('cls' if os.name=='nt' else 'clear')
    SaveSitting()
    check = CheckUSB()
    if check:
        os.system('cls' if os.name=='nt' else 'clear')
        
        print(f"\033[32mFound USB: {check[2]} - {check[3]}\033[0m")

        fi = USBFiles(check[0])

        if fi:
            print("\033[32mFound {} File{} In {} - {}\033[0m".format(len(fi), "s" if len(fi) != 1 else "", check[2], check[3]))
        
        Value = input("Input a Value: ")

        if Value.startswith("https://drive.google.com") or Value.startswith("https://drive.usercontent.google.com"): 
            fromGDrivetoUSB(Value)
        elif Value.endswith(".zip"):
            fromZiptoUSB(Value)
        elif AutoCorrection(Value.lower()) == "format":
            format(check)
        elif AutoCorrection(Value.lower()) == "changeusb":
            global USBdata
            USBdata = {}
            main()
        elif AutoCorrection(Value.lower()) == "savesettings":
            SaveSitting("save")
        else:
            input(f"USB: {check[2]} - {check[3]}\n\nZIPFile: Move The Saves To {check[2]}.\nGoogleDriveLink: Download And Move Your Save To {check[2]}\nFormat: Format {check[2]}\nChangeUSB: Change From {check[2]} To Any other USBs\nSaveSettings: Changing nSaveSettings\n\nPress any key to continue ...")
            main()
            
main()