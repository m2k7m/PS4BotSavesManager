import zipfile,os,shutil,gdown,time,json

if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        config = json.load(f)
else:
    config = {}

def SaveSitting(zipname:str = None):
    if not os.path.exists('config.json') or zipname=="save":
        sit = input("Do You Want Keep ZIP Files? (T or F):")
        if sit.upper() == "T":
            config["Save"] = True
        elif sit.upper() == "F":
            config["Save"] = False
        with open("config.json", "w") as f:
            json.dump(config, f,indent=4)
        main()
    for save,value in config.items():
        if value is False and zipname:
            os.remove(zipname)
            print(f"\033[32m{zipname} Removed Successfully.\033[0m")

def filterNumbers(num):
    if num == 0 :
        return num + 1
    if (num % 2) == 0: 
        return num + 1

def CheckUSB():
    usb = os.popen("wmic logicaldisk where drivetype=2 get filesystem,volumename,deviceid").read()
    if usb.find("DeviceID") != -1:
        if usb.split("\n")[4]:
            Number = input("USB Number(Defult Is The First USB): ")
            if Number == "":
                Number = 0
            elif not Number.isdigit():
                print(f"{Number} Is Not a Number Please Try Again")
                Number = 0
                CheckUSB()
            else:
                Number =int(Number)
        else:
            Number = 0

        if filterNumbers(Number):
            Number = filterNumbers(Number)

        nusb = usb.split("\n")[Number + 1 ]
        letter = nusb.split(" ")[0]
        system = nusb.split(" ")[8]
        name = nusb.split(" ")[15]
        return letter,system,name
    else:
        os.system('cls' if os.name=='nt' else 'clear')
        print("\033[0;31mThere's No USB, Waiting for a USB ...")
        while True:
            usb = os.popen("wmic logicaldisk where drivetype=2 get filesystem,volumename,deviceid").read()
            if usb.find("DeviceID") != -1:
                letter = usb.split("\n")[2].split(" ")[0]
                system = usb.split("\n")[2].split(" ")[8]
                name = usb.split("\n")[2].split(" ")[15]
                return letter,system,name
            time.sleep(5)

def fromZiptoUSB(zipname:str):
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
                print(f"\033[32mYour Save Moved To {check[2]}, Enjoy <3")
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
        os.remove(dzip)
        input("\033[0;31mThe Link Is Not For a Save.")

def format(usbdata:list):
    cmd = f"format {usbdata[0]} /FS:{usbdata[1]} /Q /V:{usbdata[2]} /y"
    os.system(cmd)
    os.system('cls' if os.name=='nt' else 'clear')
    print(f"\033[32m{usbdata[2]} Has Been Formatted Successfully\033[0m")
    time.sleep(3)
    main()

def main():
    os.system('cls' if os.name=='nt' else 'clear')
    SaveSitting()
    check = CheckUSB()
    if check:
        os.system('cls' if os.name=='nt' else 'clear')
        print(f"\033[32mUSB Found {check[2]} \033[0m")
        Value = input("Input a Value: ")
        if Value.startswith("https://drive.google.com") or Value.startswith("https://drive.usercontent.google.com"): 
            fromGDrivetoUSB(Value)
        if Value.endswith(".zip"):
            fromZiptoUSB(Value)
        if Value.lower() == "format":
            format(check)
        if Value.lower() == "change":
            main()
        if Value.lower() == "save":
            SaveSitting("save")

main()