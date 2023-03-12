import codecs
import hashlib
import json
import pathlib
import random
import shutil
import time
import chardet
import undetected_chromedriver as uc
import sys

import wmi
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException, StaleElementReferenceException,
                                        ElementClickInterceptedException, ElementNotInteractableException,
                                        TimeoutException)
import os

global username, password, filename, videotype,video_name,video_description, videoratio, keywords, music, voiceover, heighlight, langguage, accent, gender, voice, resolution, subtitle

f = open("otptdt.dt", "w")
f.writelines("{")
f.writelines("}")
f.close()

sys.setrecursionlimit(999999999)
def getandwritemainprocesspid():
    pidtotext = os.getpid()
    pidtextfile = open("processtemp.file", "r+")
    pidtextfile.seek(0)
    pidtextfile.truncate()
    pidtextfile.close()
    pidtextfile = open("processtemp.file", "w")
    pidtextfile.writelines(str(pidtotext))
    pidtextfile.close()

getandwritemainprocesspid()
with open("torunprogram.tp", "r") as file:
    deviceidfromdb = file.readlines()[0]
    file.close()

with open("vld.dt", "r") as file2:
    vddt = file2.readlines()[0]
    file2.close()

def get_bios_serial():
    c = wmi.WMI()
    for system in c.Win32_ComputerSystem():
        raju2 = system.qualifiers["UUID"]
        return raju2

# Get BIOS serial
bios_serial = get_bios_serial()

hardware_id = hashlib.sha256((str(bios_serial) + "rajuahmed").encode()).hexdigest()
hardware_id = hashlib.sha256((str(hardware_id) + str(vddt)).encode()).hexdigest()

def repJsonObj(outputtext,numbertooutput):

    f = open(f"otptdt.dt", "r+")
    json_object = json.load(f)
    f.close()
    json_object['data'] = {"outputtext": outputtext, "numbertooutput":numbertooutput}
    f = open("otptdt.dt", "w")
    json.dump(json_object, f)
    f.close()

if deviceidfromdb==hardware_id:
    runprogram = True
else:
    sys.exit()

path = "chromedriver.exe"
path2 = "strdt.strdt"
files_directory = "texts"
outputtext = "initializing.."
numbertooutput = "2"
repJsonObj(outputtext,numbertooutput)

paragraph_list=[]

if (os.path.exists("otptdt.dt") == False):
    f = open("otptdt.dt", "w")
    f.writelines("{")
    f.writelines("}")
    f.close()

def get_first_file_path(files_directory):
    global first_file_path
    first_file_path = None
    for root, dirs, files in os.walk(files_directory):
        if len(files) > 0:
            first_file_path = os.path.join(root, files[0])
            break
def getscripts():
    global video_name,video_description,first_file_path, paragraph_list, filename
    get_first_file_path(files_directory)
    filename = first_file_path
    outputtext = "Working on Scripts"
    numbertooutput = "10"
    repJsonObj(outputtext, numbertooutput)
    pathname, extension = os.path.splitext(filename)

    video_name = pathname.split('\\')[-1]
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
        encodingformat = result['encoding']
    with codecs.open(filename, 'r', encodingformat) as f:
         text = f.read()
    with codecs.open(filename, 'w', 'ansi') as outfile:

        outfile.write(text)
        f.close()

    f = open(filename, mode='rt', encoding='ANSI')
    video_description = f.read()
    f.close()

    video_description = video_description.replace("!", "!\n")
    video_description = video_description.replace("?", "?\n")
    video_description = video_description.replace("þ", "")
    video_description = str(video_description)

def split_text(text, char_limit, min_char_limit):
    paragraphs = text.split('. ') if '. ' in text else text.split(', ') if ', ' in text else text.split()
    split_paragraphs = []
    for paragraph in paragraphs:
        words = paragraph.split()
        current_paragraph = []
        current_length = 0
        for word in words:
            if current_length + len(word) + 1 <= char_limit:
                current_paragraph.append(word)
                current_length += len(word) + 1
            elif current_length >= min_char_limit:
                split_paragraphs.append(' '.join(current_paragraph))
                current_paragraph = [word]
                current_length = len(word) + 1
            else:
                current_paragraph.append(word)
                current_length += len(word) + 1
                if '. ' not in text and ', ' not in text:
                    if len(words) > 1:
                        random_index = random.randint(1, len(words) - 1)
                        split_paragraphs.append(' '.join(words[:random_index]))
                        current_paragraph = words[random_index:]
                        current_length = len(' '.join(current_paragraph)) + 1
        if current_length >= min_char_limit:
            split_paragraphs.append(' '.join(current_paragraph))
    return split_paragraphs

def save_to_file(split_paragraphs, file_name):
    with open(file_name, 'w') as file:
        for paragraph in split_paragraphs:
            file.write(paragraph + '.\n\n')
#getscripts()
#split_paragraphs = split_text(video_description, 190, 100)
#save_to_file(split_paragraphs, filename)

getscripts()

current_dir = pathlib.Path(__file__).parent.absolute()

def loaddatafromjson():

    global username, password, videotype, videoratio, keywords, music, voiceover, heighlight, langguage, accent, gender, voice, resolution, subtitle

    f = open("strdt.strdt")
    data = json.load(f)

    data = data.get("data")
    username = data.get("username")
    password = data.get("password")
    videotype = data.get("videotype")
    videoratio = data.get("videoratio")
    keywords = data.get("keywords")
    music = data.get("music")
    if music == "True":
        music = True
    elif music == "False":
        music = False
    voiceover = data.get("voiceover")
    if voiceover == "True":
        voiceover = True
    elif voiceover == "False":
        voiceover = False
    heighlight = data.get("heighlight")
    if heighlight == "True":
        heighlight = True
    elif heighlight == "False":
        heighlight = False
    langguage = data.get("langguage")
    accent = data.get("accent")
    gender = data.get("gender")
    voice = data.get("voice")
    resolution = data.get("resolution")
    subtitle = data.get("subtitle")
    if subtitle == "True":
        subtitle = True
    elif subtitle == "False":
        subtitle = False
loaddatafromjson()
chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--user-data-dir=C:\\Users\\Raj\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1')
#chrome_options.add_argument(f'--headless')
chrome_options.add_argument(f'--disable-gpu')
chrome_options.add_argument(f'--no-sandbox')
chrome_options.add_argument(f'--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

driver = uc.Chrome(use_subprocess=True, options=chrome_options, driver_executable_path=path)
outputtext = "Drive into website"
numbertooutput = "3"
repJsonObj(outputtext, numbertooutput)
driver.get('https://app.steve.ai/steveai/')
driver.maximize_window()

try:

    outputtext = "Checking Authorization...."
    numbertooutput = "4"
    repJsonObj(outputtext, numbertooutput)
    driver.implicitly_wait(5)
    email_input = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div[4]/input')
    time.sleep(1)
    email_input.clear()
    email_input.send_keys(username)
    password_input= driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div[5]/input')
    time.sleep(1)
    password_input.clear()
    password_input.send_keys(password)

    loginbutto= driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div[6]/button')
    loginbutto.click()
except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException, ElementNotInteractableException,TimeoutException):
    raju = True
try:
    outputtext = "Initilize Video Type"
    numbertooutput = "6"
    repJsonObj(outputtext, numbertooutput)
    if videoratio == "Horizontal":
        driver.implicitly_wait(100)
        select_ratio = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[1]')
        select_ratio.click()
    elif videoratio =="Vertical":
        driver.implicitly_wait(100)
        select_ratio = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[2]')
        select_ratio.click()
    elif videoratio == "Square":
        driver.implicitly_wait(100)
        select_ratio = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[3]/div[3]')
        select_ratio.click()
    driver.implicitly_wait(100)
    liveoranimationbutton = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/div[1]/div[2]/span')
    liveoranimationbutton.click()
    if videotype == "Live video":
        driver.implicitly_wait(100)
        animationvideoselect = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/div[1]/div[3]/div[1]')
        animationvideoselect.click()
    elif videotype == "Animation Video":
        driver.implicitly_wait(100)
        animationvideoselect = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/div[1]/div[3]/div[2]')
        animationvideoselect.click()
    time.sleep(3)
    driver.implicitly_wait(100)
    wriewonscript = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/div[6]')
    wriewonscript.click()
    getscripts()
    driver.implicitly_wait(100)
    videotitle = driver.find_element(By.XPATH, '//*[@id="video_title"]')
    videotitle.clear()
    videotitle.send_keys(video_name)
    typescripthere = driver.find_element(By.XPATH, '//*[@id="contentCont1"]')
    typescripthere.clear()
    typescripthere.send_keys(video_description)
    keywordofvideo = driver.find_element(By.XPATH, '//*[@id="context_text"]')
    keywordofvideo.clear()
    keywordofvideo.send_keys(keywords)
    driver.implicitly_wait(100)
    video_name = 'raju'
    video_description = 'raju'
    if music==True:
        outputtext = "Initilize Music"
        numbertooutput = "12"
        repJsonObj(outputtext, numbertooutput)
        driver.implicitly_wait(100)
        checkmusiccheckbox=driver.find_element(By.XPATH, '//*[@id="music_check"]')
        if checkmusiccheckbox.is_selected():
            print("Checkbox is selected")
        else:
            checkmusiccheckbox.click()
    elif music==False:
        driver.implicitly_wait(100)
        checkmusiccheckbox = driver.find_element(By.XPATH, '//*[@id="music_check"]')
        if checkmusiccheckbox.is_selected():
            checkmusiccheckbox.click()
        else:
            print("Checkbox is selected")
    if heighlight== True:
        driver.implicitly_wait(100)
        highlightcheckbox=driver.find_element(By.XPATH, '//*[@id="autohighlight_check"]')
        if highlightcheckbox.is_selected():
            print("Checkbox is selected")
        else:
            driver.implicitly_wait(100)
            highlightcheckbox = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/div[7]/div/div[1]/span')
            highlightcheckbox.click()
    elif heighlight==False:
        driver.implicitly_wait(100)
        highlightcheckbox = driver.find_element(By.XPATH, '//*[@id="autohighlight_check"]')
        if highlightcheckbox.is_selected():
            highlightcheckbox.click()
        else:
            print("Checkbox is selected")

    if voiceover == True:
        outputtext = "Initilize Voice Over"
        numbertooutput = "20"
        repJsonObj(outputtext, numbertooutput)
        driver.implicitly_wait(100)
        voiceoverckbx=driver.find_element(By.XPATH, '//*[@id="speech_check"]')
        if voiceoverckbx.is_selected():
            print("Checkbox is selected")
        else:
            driver.implicitly_wait(100)
            voiceoverckbx = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/div[7]/div/div[2]/span')
            voiceoverckbx.click()
            driver.implicitly_wait(100)
            languagedropdown = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[1]/div[2]/span')
            languagedropdown.click()
            driver.implicitly_wait(100)
            languagelist = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[1]/div[3]')
            try:
                driver.implicitly_wait(100)
                allchildlanguage = languagelist.find_elements(By.XPATH, './*')
                for lng1 in allchildlanguage:
                    lntxt = lng1.text
                    if lntxt == langguage:
                        lng1.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException,
                    ElementNotInteractableException, TimeoutException):
                raju = False

            time.sleep(1)
            driver.implicitly_wait(100)
            accentdropdown = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[2]/div[2]/span')
            accentdropdown.click()
            driver.implicitly_wait(100)
            accentlist = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[2]/div[3]')
            try:

                driver.implicitly_wait(100)

                allchildaccent = accentlist.find_elements(By.XPATH, './*')
                for acnt1 in allchildaccent:
                    acnttxt = acnt1.text
                    if acnttxt == accent:
                        acnt1.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException,
                    ElementNotInteractableException, TimeoutException):
                raju = False

            time.sleep(1)
            driver.implicitly_wait(100)

            genderdropdown = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[3]/div[2]/span')
            genderdropdown.click()

            driver.implicitly_wait(100)
            genderlist = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[3]/div[3]')

            try:
                driver.implicitly_wait(100)
                allchildgender = genderlist.find_elements(By.XPATH, './*')
                for gndr1 in allchildgender:
                    gndrtxt =  gndr1.text
                    if gndrtxt == gender:
                        gndr1.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException,
                    ElementNotInteractableException, TimeoutException):
                raju = False
            time.sleep(1)
            driver.implicitly_wait(100)

            voicedropdown = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[4]/div[2]/span')
            voicedropdown.click()
            driver.implicitly_wait(100)
            voicelist = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[4]/div[3]')
            try:
                driver.implicitly_wait(100)
                allchildvoice = voicelist.find_elements(By.XPATH, './*')
                for vc1 in allchildvoice:
                    voicetext = vc1.text
                    if voicetext == voice:
                        vc1.click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException,
                    ElementNotInteractableException, TimeoutException):
                raju = False

            driver.implicitly_wait(100)
            generatevoicebutton = driver.find_element(By.XPATH, '/html/body/div[7]/div/div/div[2]/div[5]/div[2]')
            generatevoicebutton.click()

    elif voiceover==False:
        voiceoverckbx = driver.find_element(By.XPATH, '//*[@id="speech_check"]')
        if voiceoverckbx.is_selected():
            voiceoverckbx.click()
        else:
            print("Checkbox is selected")
    outputtext = "Selecting Suitable Theme"
    numbertooutput = "40"
    repJsonObj(outputtext, numbertooutput)
    driver.implicitly_wait(100)
    nextbutton = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/div[10]')
    nextbutton.click()
    driver.implicitly_wait(100)
    themeselectionbuttton = driver.find_element(By.XPATH, '//*[@id="animaker-ttv-theme-selection-page"]')
    driver.implicitly_wait(200)
    allchildthemeselection = themeselectionbuttton.find_elements(By.XPATH, './*')
    if videotype == "Animation Video":
        allchildthemeselection = allchildthemeselection[ : -1]

    singletheme = random.choice(allchildthemeselection)
    singletheme.click()
    if subtitle ==True:
        driver.implicitly_wait(200)
        subtitleeye = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[1]/div/div[5]/ul/li[7]/img')
        subtitleeye.click()
        driver.implicitly_wait(100)
        hideallsubtitle = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div[1]/div[2]/div[2]/div[2]/label')
        hideallsubtitle.click()

    outputtext = "Wait For a Moment"
    numbertooutput = "70"
    repJsonObj(outputtext, numbertooutput)

    driver.implicitly_wait(100)
    publishbutton = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div[2]')
    publishbutton.click()
    driver.implicitly_wait(100)
    outputtext = "Initilizing Resolution"
    numbertooutput = "90"
    repJsonObj(outputtext, numbertooutput)
    resolutiodropdown= driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/img')
    resolutiodropdown.click()
    driver.implicitly_wait(100)
    if resolution == "1080p":
        pixel1080p = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[3]')
        pixel1080p.click()
    else:
        pixel720p  = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[2]')
        pixel720p.click()

    outputtext = "Almost Done"
    numbertooutput = "98"
    repJsonObj(outputtext, numbertooutput)
    download = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div[2]/div[5]/div')
    download.click()

    driver.implicitly_wait(100)
    queuedstatus = driver.find_element(By.XPATH, '//*[@id="videotoolrefresh"]/div[3]/div[9]/div[1]/h3')
    
    time.sleep(3)
    trg_path = 'texts\\Completed'
    shutil.move(filename, trg_path)
    print("done everythin")
    driver.quit()
    outputtext = "Done"
    numbertooutput = "100"
    repJsonObj(outputtext, numbertooutput)

except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException,
                ElementNotInteractableException, TimeoutException):
    driver.close()
    outputtext = "Something Went Wrong"
    numbertooutput = "0"
    repJsonObj(outputtext, numbertooutput)