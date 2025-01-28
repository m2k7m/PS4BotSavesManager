
import zipfile
import shutil
import time
import json
import os
import re

USBdata = []

if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        config = json.load(f)
else:
    config = {}

second_run = False

def SaveSitting(zipname:str = None) -> None:
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
    
    if second_run == True:
        input("Anything Else?")
        second_run = False
        main()

def CheckUSB() -> list:
    global USBdata

    # Fetch USB information using WMIC (Windows Management Instrumentation Command)
    usb = os.popen("wmic logicaldisk where drivetype=2 get filesystem,volumename,deviceid,Size").read()

    # Check if any USB is connected
    if usb.find("DeviceID") != -1:
        # Split the output into lines and remove empty strings
        usb_lines = [line.strip() for line in usb.split("\n") if line.strip()]
        #print(usb_lines)  # Debugging: Print the cleaned lines

        # Extract USB entries
        usb_entries = usb_lines[1:]  # Remaining lines are USB entries

        # Prompt user to select a USB (default is the first one)
        if len(usb_entries) != 1:
            Number = input("USB Number (Default is the first USB): ")
        else:
            Number = 0
        
        if not Number:
            Number = 0
        elif not Number.isdigit():
            print(f"\033[0;31m{Number} Is Not a Number. Please Try Again.\033[0m")
            return CheckUSB()  # Recursively call the function to retry
        else:
            Number = int(Number) - 1

        # Validate the selected USB number
        if Number >= len(usb_entries):
            print(f"\033[0;31mThere's No {Number + 1}th USB. Please Try Again.\033[0m")
            return CheckUSB()  # Recursively call the function to retry

        # Extract USB details
        nusb = usb_entries[Number].split()
        letter = nusb[0]
        system = nusb[1]
        size = CalculateDiskSize(int(nusb[2]))
        name = " ".join(nusb[3:])  # Handle USB names with spaces

        # Save USB data to the global List
        USBdata.append(letter)
        USBdata.append(system)
        USBdata.append(name)
        USBdata.append(size)

        return USBdata
    else:
        # No USB found, wait for a USB to be connected
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[0;31mThere's No USB. Waiting for a USB ...\033[0m")
        while True:
            usb = os.popen("wmic logicaldisk where drivetype=2 get filesystem,volumename,deviceid,Size").read()
            if usb.find("DeviceID") != -1:
                usb_lines = [line.strip() for line in usb.split("\n") if line.strip()]
                nusb = usb_lines[1].split()
                letter = nusb[0]
                system = nusb[1]
                size = CalculateDiskSize(int(nusb[2]))
                name = " ".join(nusb[3:])  # Handle USB names with spaces

                # Save USB data to the global List
                USBdata.append(letter)
                USBdata.append(system)
                USBdata.append(name)
                USBdata.append(size)

                return USBdata
            time.sleep(5)

def CalculateDiskSize(bytes: int) -> str:
    """Convert bytes to a human-readable size format."""
    gibibytes = int(bytes) / (1024 * 1024 * 1024)
    return f"{gibibytes:.2f} GB"

def fromZiptoUSB(zipname: str) -> None:
    global second_run

    if USBdata:
        check = USBdata
    else:
        check = CheckUSB()

    print(f"\033[32mPrepareing {zipname} ...\033[0m")

    with zipfile.ZipFile(zipname) as newzip:
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

def fromGDrivetoUSB(url: str) -> None:
    try:
        import gdown
    except ModuleNotFoundError:
        raise ImportError("The 'gdown' module is not installed. Please install it using 'pip install gdown'.")

    # Regex pattern to extract file_id from Google Drive URL
    pattern = re.compile(r'(?:https://drive\.google\.com/file/d/|https://drive\.google\.com/uc\?id=|https://drive\.usercontent\.google\.com/download\?id=)([a-zA-Z0-9_-]+)')
    
    match = pattern.search(url)
    if match:
        file_id = match.group(1)
    else:
        if "folders" in url:
            raise ValueError("The provided URL is for a folder. Please provide a URL for a ZIP file.")
        else:
            raise ValueError("Invalid Google Drive URL. Please provide a valid file URL.")

    print("\033[32mWaiting For Download ...\033[0m")
    dzip = gdown.download("https://docs.google.com/uc?export=download&id=" + file_id)
    
    if dzip.endswith(".zip"):
        fromZiptoUSB(dzip)
    else:
        SaveSitting(dzip)
        raise ValueError("The downloaded file is not a ZIP file. Please provide a valid ZIP file URL.")

def format(usbdata: list) -> None:
    check = USBFiles(usbdata[0])
    if not check:
        time.sleep(3)
        main()

    # Construct the format command
    cmd = f"format {usbdata[0]} /FS:{usbdata[1]} /Q /V:{usbdata[2]} /y"

    # Run the command without showing output in the terminal
    try:
        import subprocess
        print("\033[32mFormating ...")
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"{usbdata[2]} Has Been Formatted Successfully\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[0;31mFailed to format {usbdata[2]}. Error: {e}\033[0m")

    time.sleep(3)
    main()

def USBFiles(USB: str) -> int:
    files = os.listdir(USB)
    if files == ['System Volume Information']:
        return print("\033[0;31mThere are no files in the USB.\033[0m")
    files.remove("System Volume Information")
    return len(files)

def AutoCorrection(Word: str, database: dict = {"format", "changeusb", "savesettings"}, simlimit: int = 0.4) -> str:

    def createBigram(word: str) -> list[str]:
        return [word[i] + word[i+1] for i in range(len(word)-1)]

    def getSim(FirstWord: str, SecondWord: str) -> float:
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
    
    return most_sim_word if max_sim > simlimit else Word

def main() -> None:
    SaveSitting()
    check = CheckUSB()

    os.system('cls' if os.name=='nt' else 'clear')

    print(f"\033[32mFound USB: {check[2]} - {check[3]}\033[0m")

    FilesNumber = USBFiles(check[0])

    if FilesNumber:
        print("\033[32mFound {} File{} In {} - {}\033[0m".format(FilesNumber, "s" if FilesNumber != 1 else "", check[2], check[3]))
    
    Value = input("Input a Value: ")

    if Value.startswith("https"): 
        fromGDrivetoUSB(Value)

    elif Value.endswith(".zip"):
        fromZiptoUSB(Value)

    elif AutoCorrection(Value.lower()) == "format":
        format(check)

    elif AutoCorrection(Value.lower()) == "changeusb":
        global USBdata
        USBdata = []
        main()

    elif AutoCorrection(Value.lower()) == "savesettings":
        SaveSitting("save")

    else:
        input(f"USB: {check[2]} - {check[3]}\n\nZIPFile: Move The Saves To {check[2]}.\nGoogleDriveLink: Download And Move Your Save To {check[2]}\nFormat: Format {check[2]}\nChangeUSB: Change From {check[2]} To Any other USBs\nSaveSettings: Changing nSaveSettings\n\nPress any key to continue ...")
        main()
            
main()