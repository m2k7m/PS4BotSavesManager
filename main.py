import zipfile,os,shutil,gdown,time

def CheckUSB():
    usb = os.popen("wmic logicaldisk where drivetype=2 get filesystem,volumename,deviceid").read()
    if usb.find("DeviceID") != -1:
        usb_letter = usb.split("\n")[2].split(" ")[0]
        usb_system = usb.split("\n")[2].split(" ")[8]
        usb_name = usb.split("\n")[2].split(" ")[15]
        return usb_letter,usb_system,usb_name
    else:
        os.system('cls' if os.name=='nt' else 'clear')
        print("\033[0;31mThere's No USB, Waiting for a USB ...")
        while True:
            usb = os.popen("wmic logicaldisk where drivetype=2 get filesystem,volumename,deviceid").read()
            if usb.find("DeviceID") != -1:
                usb_letter = usb.split("\n")[2].split(" ")[0]
                usb_system = usb.split("\n")[2].split(" ")[8]
                usb_name = usb.split("\n")[2].split(" ")[15]
                return usb_letter,usb_system,usb_name
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
                print(f"\033[32mI Moved Your Save To {check[2]}, Enjoy <3")

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

def main():
    os.system('cls' if os.name=='nt' else 'clear')
    check = CheckUSB()
    if check:
        os.system('cls' if os.name=='nt' else 'clear')
        print(f"\033[32mUSB Found {check[2]} \033[0m")
        Value = input("Input a Value: ")
        if Value.startswith("https://drive.google.com") or Value.startswith("https://drive.usercontent.google.com"): 
            fromGDrivetoUSB(Value)
        if Value.endswith(".zip"):
            fromZiptoUSB(Value)

main()