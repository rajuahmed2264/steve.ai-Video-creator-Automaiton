import subprocess

import ntplib
import hashlib
import json
import os
import urllib
from datetime import date, datetime
import time
import wmi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
import radar
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType  # error appears here
from os import path

global namefromsoftware,deviceidfromdb, emailfromsoftware,finalvalidityday, usernamefromsoftware, referencefromsoftware, phonenumberfromsoftware, username,usernamefromtxt,finalvaliditydays, current_time, password, videotype, videoratio, keywords, music, voiceover, heighlight, langguage, accent, gender, voice, resolution, subtitle
ui, _ = loadUiType(path.join(path.dirname(__file__), "activation.ui"))
deviceidfromdb="raju"
finalvaliditydays=0

def get_bios_serial():
    c = wmi.WMI()
    for system in c.Win32_ComputerSystem():
        raju2 = system.qualifiers["UUID"]
        return raju2

# Get BIOS serial
bios_serial = get_bios_serial()
hardware_id = hashlib.sha256((str(bios_serial) + "rajuahmed").encode()).hexdigest()
if (os.path.exists("otptdt.dt") == False):
    f = open("otptdt.dt", "w")
    f.writelines("{")
    f.writelines("}")
    f.close()
try:
    client = ntplib.NTPClient()
    time.sleep(.7)
    response = client.request('pool.ntp.org')
    time.sleep(.7)
    internet_time = datetime.fromtimestamp(response.tx_time)
    time.sleep(.7)
    local_time = datetime.now()
    time_difference = local_time - internet_time
    if time_difference.total_seconds() > 5 or  time_difference.total_seconds() < -5:
        print("Your computer's time is not in sync with the internet.")
        sys.exit()
    else:
        print("Your computer's time is in sync with the internet.")
except:
    print("Could not connect to the NTP server.")
    sys.exit()


def getusernamefromfile():
    global usernamefromtxt
    with open("username.raj", "r") as file:
        usernamefromtxt = file.readlines()[0]

def repJsonObj(file):
    global username, password, videotype, videoratio, keywords, music, voiceover, heighlight, langguage, accent, gender, voice, resolution, subtitle
    f = open(f"{file}", "r+")
    json_object = json.load(f)
    f.close()
    username = str(username)
    password = str(password)
    videotype = str(videotype)
    videoratio = str(videoratio)
    keywords = str(keywords)
    music = str(music)
    voiceover = str(voiceover)
    heighlight = str(heighlight)
    langguage = str(langguage)
    accent = str(accent)
    gender = str(gender)
    voice = str(voice)
    resolution = str(resolution)
    subtitle = str(subtitle)
    json_object['data'] = {
        "username": username,
        "password": password,
        "videotype": videotype,
        "videoratio": videoratio,
        "keywords": keywords,
        "music": music,
        "voiceover": voiceover,
        "heighlight": heighlight,
        "langguage": langguage,
        "accent": accent,
        "gender": gender,
        "voice": voice,
        "resolution": resolution,
        "subtitle": subtitle
    }
    f = open(file, "w")
    json.dump(json_object, f)
    f.close()


def getdatafromdb():
    global usernamefromtxt,finalvaliditydays, idfromdb,current_time, emailfromdb, validtillfromdb, activationdatefromdb, deviceidfromdb, namefromdb


    db = firestore.client()
    result = db.collection("users").document(usernamefromtxt).get()
    if result.exists:
        result1 = result.to_dict()
        idfromdb = result1["id"]
        emailfromdb = result1["email"]
        deviceidfromdb = result1["uniqueId"]
        namefromdb = result1["name"]
        validtillfromdb = result1["validtill"]

        today = datetime.now()
        validitydays1 = datetime.timestamp(today)
        validitydays1 = datetime.fromtimestamp(validitydays1)
        validitydays2 = datetime.timestamp(validtillfromdb)
        validitydays2 = datetime.fromtimestamp(validitydays2)
        finalvaliditydays = (validitydays2 - validitydays1).days

def savedatatofirebase():
    global namefromsoftware, emailfromsoftware, usernamefromsoftware,finalvaliditydays, referencefromsoftware, phonenumberfromsoftware, hardware_id
    validtilltoinsert = firestore.SERVER_TIMESTAMP
    db = firestore.client()

    dictionarytoinsertdata = {"username": usernamefromsoftware, "name": namefromsoftware, "registrationtime": validtilltoinsert,"validtill":validtilltoinsert, "id": emailfromsoftware,
                              "email": emailfromsoftware, "reference": referencefromsoftware, "uniqueId":hardware_id}
    db.collection("users").document(usernamefromsoftware).set(dictionarytoinsertdata)
    message = QMessageBox()
    message.setWindowTitle("User Created")
    message.setText("You Have Registered With Your Username, Please Contact Us To Buy A Package.")
    message.exec_()


config = {
  "type": "service_account",
  "project_id": "steve-be596",
  "private_key_id": "d8d5ac192ba3f0bc66f66191edc7265399b6ed0f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCsQ6NCrAvgQ+XC\nmg160G9IZ37RKGqtiAiI3SNhU7wEmezxlKLzr0UmWZC4BQO1FliapYxHCjPLrpvN\n8oSXC36oK+aPxPoXayEq6voN8dMDqBGWPx8MqEgYSvoOmCJqtkb6/1wpl9rq8oi1\nb/gqxlord8bjty+4tpsd80Z8p/MonAu5YA6MBJEGi1DEu70JJH/pjE3GC73QEYv7\nEtyG5H3cqj4iNUin7qiqUE8XIbKE3Ozw1gLEy72DCmBRhmSYnqIDysBI/l+fWnNA\naAG0+HymsBksRsy3wCX+0OPI4ln6eUO4AjPz8tPvs5Ob4j4YCg8ed4wqguQQEosC\ndNyen4+NAgMBAAECggEAG3jH6wSL+k5psFCoEKt368iRiWKULKtyjP0TPNzBMcyo\nZFhrakhL01NaSHaIQlNXewYmqleerf9hGoVwDrSHFOO3Z7smlSCBEBqcGSg1GjKt\n51OWrIqTwMgIO9aYOoNqK3IY7QsqHujh02mRXqT2UVNPNRaMNj1s3GhlF9Ei7pk8\nz9+LlExPAbvyP+0xuV62266ssFjOyh9G+eEPwdKIy5Fs/6q+3UGFuN6nKRZkyv0E\nHrhYLxwQ1ihhplud5eu4UuisdwObU3oY1FkeFVpq3STdffPItMXpBewjGd+XmBfh\n3Ik092qLJ56tUk4cEt95sh/96h6B7Bp1mBCay26MkwKBgQDo/Vaxmht8PBvAMun3\nfDvUSf9rwVE3qWY+rFXMC/cdAQux9mhdgZlYH78OAfCWfZL51z52ISgTvLjV8ZSn\n/hl2kURiKhh/Lt7O1a0LLn8Snp7wXerYppO8pRBxC+IPvu/S1CfZ94pd3NroMyRg\nb1QgxqgX+TQalXF3vTkpAnNXqwKBgQC9RvuZOpAMytp1E/6hAPBbID3RsVBmaI5+\nmR0p4iaFKvmKnQr8Xnn7mTGEsV1l0d82xXfIaw1FUaXXds2Qn5/TVsXrsSNfgByy\nFgGt2h8fp1i0DBb8hCI2+GiGrRyqy8VayUAsYx+wAqjumMz+cd4Abe+potC3BR8n\nXgQwblkdpwKBgQDV5EWjdEvJSNFdKCCcoEO4x1oijW3HQM/pt4JoeY+Z4+zdqs3z\nEdg6C6L09Bjvv0af8NeZ0SSewgGZ/1cuxlqP/BqgV+73S4smrQlYm43zBQX6uu2v\niXVVmN+4OGWHeQ1oKnaPZu5y7x9UTicWFP5RvK5ym8gWo51whJmmKWbEUwKBgHJS\njWTfmmIfpBNTIFje2E4yCyS8lHNGc8rDcHn7vohwjIjMkfYcmlD9FouvFVqKiOfs\nHY1QG5Pi3OhnOYJA56geoSzasSLdnndyE1GOjX3w9gLJyph6tq+9GmU96jK/IVTU\neY5V0K3e7WovoKGO5SgdPsSXMrlYvphokN8vx2PBAoGBANNNJReBDJVidv+TNisy\nUtFlelTm49BtLhuW1pbvKWaxEMSzjrjAWY5AOPJtGsYdsZbHysBs9U8kWxS8gd/w\nC0d7xCBWJjYdRPc70LzLElXExPeXlxRkN3S67u6hkOL29TOMYc0Z8ZlJmaB5tGil\n6EOtR7qWk+PFeRT+KWOyUoJU\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-wfy5n@steve-be596.iam.gserviceaccount.com",
  "client_id": "106367359376457618206",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-wfy5n%40steve-be596.iam.gserviceaccount.com"
}


class MainApp(QMainWindow, ui):
    global usernamefromtxt, finalvaliditydays
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.stevepass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.startbutton.clicked.connect(self.startbuttonclick)
        self.regsubmitbtn.clicked.connect(self.regsubmtbutton)
        self.tabWidget.setCurrentIndex(1)
        cred = credentials.Certificate(config)
        firebase_admin.initialize_app(cred)
        getusernamefromfile()
        getdatafromdb()
        if deviceidfromdb ==hardware_id and finalvaliditydays > 0:
            self.tabWidget.setCurrentIndex(2)
        else:
            self.tabWidget.setCurrentIndex(0)
        self.voiceckbx.stateChanged.connect(self.voiceckboxstate)
        self.lngscmbbx.activated.connect(self.languagechange)

        voicekey = 'voices'
        path = "strdt.strdt"
        if (os.path.exists(path) == False):
            f = open(path, "w")
            f.writelines("{")
            f.writelines("}")
            f.close()

        f = open("vovermsc.msc")
        data = json.load(f)
        if not data:

            self.lngscmbbx.setCurrentIndex(0)
        else:
            self.lngscmbbx.clear()
            languages = data.get(voicekey)
            self.lngscmbbx.addItems(languages)
        self.accentcmbbx.activated.connect(self.accentcmbbxcng)
        self.gndrcmbbx.activated.connect(self.gndrcmbbxcng)
        self.appstartloaddata()
    def regsubmtbutton(self):
        self.getvaluefromregistrationform()
        savedatatofirebase()

    def gndrcmbbxcng(self):
        voicekey = 'voices'
        f = open("vovermsc.msc")
        data = json.load(f)
        languages = data.get(voicekey)
        language = self.lngscmbbx.currentText()
        accents = languages.get(language)
        accent = self.accentcmbbx.currentText()
        genders = accents.get(accent)
        gender = self.gndrcmbbx.currentText()
        voices = genders.get(gender)
        if voices:
            self.voicecmbbx.clear()
            self.voicecmbbx.addItems(voices)
        else:
            self.voicecmbbx.setCurrentIndex(0)

    def accentcmbbxcng(self):
        voicekey = 'voices'
        f = open("vovermsc.msc")
        data = json.load(f)
        languages = data.get(voicekey)
        language = self.lngscmbbx.currentText()
        accents= languages.get(language)
        accent = self.accentcmbbx.currentText()
        genders = accents.get(accent)
        if genders:
            self.gndrcmbbx.clear()
            self.gndrcmbbx.addItems(genders)
            self.gndrcmbbxcng()
            self.voicecmbbx.setCurrentIndex(0)
        else:
            self.gndrcmbbx.setCurrentIndex(0)




    def languagechange(self):
        voicekey = 'voices'
        language =  self.lngscmbbx.currentText()
        f = open("vovermsc.msc")
        data = json.load(f)
        data = data.get(voicekey)
        if data:
            self.accentcmbbx.clear()
            accents= data.get(language)
            self.accentcmbbx.addItems(accents)
            self.accentcmbbxcng()
            self.gndrcmbbx.setCurrentIndex(0)
            self.gndrcmbbxcng()
            self.voicecmbbx.setCurrentIndex(0)
        else:
            self.accentcmbbx.setCurrentIndex(0)



    def voiceckboxstate(self):
        if self.voiceckbx.isChecked():
            self.tutorialframe.setVisible(False)
        elif not self.voiceckbx.isChecked():
            self.tutorialframe.setVisible(True)

    def appstartloaddata(self):
        global username, password, videotype, videoratio, keywords, music, voiceover, heighlight, langguage, accent, gender, voice, resolution, subtitle

        key = 'data'
        path = "strdt.strdt"
        if (os.path.exists(path) == False):
            f = open(path, "w")
            f.writelines("{")
            f.writelines("}")
            f.close()
            self.appstartloaddata()
        else:
            f = open(path)
            data = json.load(f)
            if not data:

                self.vdotypcmbbx.setCurrentIndex(0)
                self.ratiocmbbx.setCurrentIndex(0)
                self.lngscmbbx.setCurrentIndex(0)
                self.accentcmbbx.setCurrentIndex(0)
                self.gndrcmbbx.setCurrentIndex(0)
                self.voicecmbbx.setCurrentIndex(0)
                self.resolutioncmbbx.setCurrentIndex(0)
            elif key in data:
                data = data.get(key)
                username = data.get("username")
                password = data.get("password")
                videotype = data.get("videotype")
                videoratio = data.get("videoratio")
                keywords = data.get("keywords")
                music = data.get("music")
                if music =="True":
                    music = True
                elif music == "False":
                    music = False
                voiceover = data.get("voiceover")
                if voiceover =="True":
                    voiceover = True
                elif voiceover == "False":
                    voiceover = False
                heighlight = data.get("heighlight")
                if heighlight =="True":
                    heighlight = True
                elif heighlight == "False":
                    heighlight = False
                langguage = data.get("langguage")
                accent = data.get("accent")
                gender = data.get("gender")
                voice = data.get("voice")
                resolution = data.get("resolution")
                subtitle = data.get("subtitle")
                if subtitle =="True":
                    subtitle = True
                elif subtitle == "False":
                    subtitle = False

                self.vdotypcmbbx.setCurrentText(str(videotype))
                self.ratiocmbbx.setCurrentText(str(videoratio))
                self.kywrdtxt.setText(str(keywords))
                self.steveuser.setText(username)
                self.stevepass.setText(password)
                self.musicckbx.setChecked(music)
                self.voiceckbx.setChecked(voiceover)
                self.hilghtckbx.setChecked(heighlight)
                if self.voiceckbx.isChecked():
                    self.lngscmbbx.setCurrentText(str(langguage))
                    f2 = open("vovermsc.msc")
                    data2 = json.load(f2)
                    languages = data2.get("voices")
                    accents = languages.get(langguage)
                    self.accentcmbbx.clear()
                    self.accentcmbbx.addItems(accents)
                    self.accentcmbbx.setCurrentText(str(accent))
                    genders = accents.get(accent)
                    self.gndrcmbbx.clear()
                    self.gndrcmbbx.addItems(genders)
                    self.gndrcmbbx.setCurrentText(str(gender))
                    voiices1 = genders.get(gender)
                    self.voicecmbbx.clear()
                    self.voicecmbbx.addItems(voiices1)
                    self.voicecmbbx.setCurrentText(str(voice))
                    self.resolutioncmbbx.clear()
                    self.resolutioncmbbx.addItems(['1080p', '720p'])
                    self.resolutioncmbbx.setCurrentText(resolution)
                    self.subtitleckbx.setChecked(subtitle)

                if self.voiceckbx.isChecked():
                    self.tutorialframe.setVisible(False)
                elif not self.voiceckbx.isChecked():
                    self.tutorialframe.setVisible(True)
            else:
                self.vdotypcmbbx.setCurrentIndex(0)
                self.ratiocmbbx.setCurrentIndex(0)
                self.lngscmbbx.setCurrentIndex(0)
                self.accentcmbbx.setCurrentIndex(0)
                self.gndrcmbbx.setCurrentIndex(0)
                self.voicecmbbx.setCurrentIndex(0)
                self.resolutioncmbbx.setCurrentIndex(0)

    def startbuttonclick(self):
        hashtowrite =  hashlib.sha256((str(deviceidfromdb) + str(finalvaliditydays)).encode()).hexdigest()
        with open(r'torunprogram.tp', 'w') as fp:
            fp.truncate()
            fp.write(hashtowrite)
            fp.close()
        with open(r'vld.dt', 'w') as fp2:
            fp2.truncate()
            fp2.write(str(finalvaliditydays))
            fp2.close()
        self.getvaluefromsoftware()
        repJsonObj('strdt.strdt')
        self.hide()
        os.startfile('pytorunedge.exe')
        subprocess.call('stop.exe')
        os.remove('torunprogram.tp')
        self.loaddatatosoftware()
        self.show()

    def getvaluefromsoftware(self):
        global username, password, videotype, videoratio, keywords, music, voiceover, heighlight, langguage, accent, gender, voice, resolution, subtitle
        username = self.steveuser.text()
        password = self.stevepass.text()
        videotype  = self.vdotypcmbbx.currentText()
        videoratio  = self.ratiocmbbx.currentText()
        keywords = self.kywrdtxt.text()
        music = self.musicckbx.isChecked()
        voiceover = self.voiceckbx.isChecked()
        heighlight = self.hilghtckbx.isChecked()
        langguage = self.lngscmbbx.currentText()
        accent = self.accentcmbbx.currentText()
        gender = self.gndrcmbbx.currentText()
        voice = self.voicecmbbx.currentText()
        resolution = self.resolutioncmbbx.currentText()
        subtitle = self.subtitleckbx.isChecked()
    def getvaluefromregistrationform(self):
        global namefromsoftware, emailfromsoftware, usernamefromsoftware, referencefromsoftware, phonenumberfromsoftware

        namefromsoftware = self.rnametxt.text()
        emailfromsoftware = self.remailtxt.text()
        usernamefromsoftware = self.rusrnamtxt.text()
        phonenumberfromsoftware = self.rphonetxt.text()
        referencefromsoftware = self.rreferenctxt.text()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
