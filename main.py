import zipfile,os,shutil,gdown

def CheckUSB():
    Usb = os.popen("wmic logicaldisk where drivetype=2 get deviceid").read()
    if Usb.find("DeviceID") != -1:
        N1 = Usb.split(":")[0].split("\n")[2]
        return N1 + ":"
    else:
        print("\033[0;31mThere's No USB")
        input("")
        exit()

def fromZiptoUSB(zipname:str):
    check = CheckUSB()
    if check:
        with zipfile.ZipFile(zipname) as newzip:
            print(f"\033[32mPrepareing {zipname} ...\033[0m")
            if newzip.filelist[0].filename.startswith("PS4/"):
                newzip.extractall(check)
                print("\033[32mYour PS4 Save Is Ready, Enjoy <3")
            else:
                newzip.extractall(check)
                shutil.copytree(check + newzip.filelist[0].filename,check,dirs_exist_ok=True)
                shutil.rmtree(check + newzip.filelist[0].filename)
                print(f"\033[32mI Moved Your Save To {check}, Enjoy <3")

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
        print("\033[0;31mThe Link Is Not For a Save.")
        os.remove(dzip)
        input("")
        exit()

def main():
    os.system('cls' if os.name=='nt' else 'clear')
    check = CheckUSB()
    print(f"\033[32mUSB Found {check} \033[0m")
    Value = input("Input a Value: ")
    if check:
        if Value.startswith("https://drive.google.com") or Value.startswith("https://drive.usercontent.google.com/download?id="): 
            fromGDrivetoUSB(Value)
        if Value.endswith(".zip"):
            fromZiptoUSB(Value)

main()