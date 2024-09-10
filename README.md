# Shadowdice
Shadowdice is an inofficial companion application for the fourth edition of the TTRPG Shadowrun by Catalyst Game Labs.
This project is not affiliated with Catalyst Game Labs.

This project is my final exam for the scripting languages module in the computer science course.

---
# Features
The following features are planned for this application:
- [x] Graphical User Interface
- [x] Support for multiple languages (german and english for now)
- [x] Graphical depiction of the dice roll
- [x] Automatically determine the number of hits and wether or not a glitch occured
- [x] Keeping track of past rolls
- [x] Dedicated buttons for certain actions 

---
# Download
If you want to use Shadowdice, head over to the release page and download the version for your operating system.

---
# Building Shadowdice
There are differences in building Shadowdice between Windows, Linux and MacOS.
In either case create a virtual environment first and download these libraries:
+ pillow
+ configparser
+ tkinter
+ json
+ glob

## Building for Windows and Linux
In addition to the above you will need to install PyInstaller.

**Windows**
```Powershell
pyinstaller --onedir --add-data "Assets/Black_Die_Dotted/*.png;Assets/Black_Die_Dotted/" --add-data "Assets/Black_Die_Numbered/*.png;Assets/Black_Die_Numbered/" --add-data "Assets/Coloured_Die_Dotted/*.png;Assets/Coloured_Die_Dotted" --add-data "Assets/Coloured_Die_Numbered/*.png;Assets/Coloured_Die_Numbered" --add-data "Assets/icon.png;Assets/" --add-data "lang/*.json;lang" --name "Shadowdice" --noconsole --icon=.\Assets\icon.png --noconfirm .\src\main.py
```

**Linux**
```Bash
pyinstaller --onedir --add-data "Assets/Black_Die_Dotted/*.png:Assets/Black_Die_Dotted/" --add-data "Assets/Black_Die_Numbered/*.png:Assets/Black_Die_Numbered/" --add-data "Assets/Coloured_Die_Dotted/*.png:Assets/Coloured_Die_Dotted" --add-data "Assets/Coloured_Die_Numbered/*.png:Assets/Coloured_Die_Numbered" --add-data "Assets/icon.png:Assets/" --add-data "lang/*.json:lang" --name "Shadowdice" --noconsole --icon=./Assets/icon.png --hidden-import="PIL._tkinter_finder" --noconfirm ./src/main.py
```
## Building for MacOS
This has been tested on an ARM MacBook.
For MacOS you need to install py2app and setuptools 70.3.0.
At time of writing the newest version of setuptools was bugged and builds failed.
So we had to downgrade to version 70.3.0.
```zsh
python setup.py py2app
```
