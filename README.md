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
If you want to use Shadowdice, head over to the [release page](https://github.com/Pixelated-Raptor/Shadowdice/releases) and download the version for your operating system.

Mind you that there is no download available for MacOS. We are able to build and run it.
But downloading the zip from the release page somehow broke the application.
We don't know why this happens, could be an issue with code signing (because there is none).
Your best bet to use it on MacOS is to build it yourself.

---
# Building Shadowdice
There are differences in building Shadowdice between Windows, Linux and MacOS.
In either case create a virtual environment first and download these libraries:
+ pillow
+ configparser
+ tkinter (should come preinstalled with python)
+ json (should come preinstalled with python)
+ glob (should come preinstalled with python)

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
