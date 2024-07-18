import zipfile,os,shutil,gdown

def CheckUSB():
    Usb = os.popen("wmic logicaldisk where drivetype=2 get deviceid").read()

    if Usb.find("DeviceID") != -1:
        N1 = Usb.split(":")[0].split("\n")[2]
        print(f"USB Is Plugged, Found {N1}:")
        return N1 + ":"
    else:
        print("\033[0;31mThere's No USB")
        input("")
        exit()

def fromZiptoUSB(zipname:str):
    check = CheckUSB()
    if check:
        with zipfile.ZipFile(zipname) as newzip:
            if newzip.filelist[0].filename.startswith("PS4/"):
                newzip.extractall(check)
                print("Your PS4 Save Is Ready, Enjoy <3")
            else:
                newzip.extractall(check)
                shutil.move(check + newzip.filelist[1].filename,check)
                shutil.rmtree(check + newzip.filelist[0].filename)
                print("I Moved Your Save To The Right Place, Enjoy <3")

def fromGDrivetoUSB(url:str):
    if url.startswith("https://drive.google.com/file/d/"):
        if url.endswith("/edit") or url.endswith("/view?usp=sharing"):
            file_id = url.split("/d/")[1].split("/")[0]
        else:
            file_id = url.split("/d/")[1]
    elif url.startswith("https://drive.google.com/uc?id="):
        file_id = url.split("=")[1].split("&")[0]
    
    dzip = gdown.download("https://docs.google.com/uc?export=download&id=" + file_id)
    if dzip.endswith(".zip"):
        fromZiptoUSB(dzip)
        os.remove(dzip)
        
start = input("Input a Value: ")
if start.startswith("https://drive.google.com"):
    print("Waiting For Download ...")
    fromGDrivetoUSB(start)
if start.endswith(".zip"):
    print(f"Prepareing {start} ...")
    fromZiptoUSB(start)