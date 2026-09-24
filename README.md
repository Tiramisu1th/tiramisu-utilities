# Tiramisu's Collection of utility scripts
This repo aims to serve as an online copy of the scripts that I created for facilitating my gaming experience. While I expect this repo to be my cloud storage, feel free to download those scripts for your personal use as long as you don't use it to do bad things

## Folder Structure
```txt
tiramisu-utilities/                 # repo root
├── game-helpers/                   # scripts for misc. games
│   ├── AdComTrainTimer.py          # Adventure Communist (https://adventurecommunist.fandom.com/wiki/Exchange_Express)
│   ├── MilkywayEnhancing.ipynb     # Milky Way Idle (https://milkywayidle.wiki.gg/wiki/Enhancing#Success_Rate)
│   └── Zealots.ipynb               # Hypixel Skyblock -> Summoning Eyes (https://hypixelskyblock.minecraft.wiki/w/Special_Zealot#Spawning)
│
├── roblox-macros/                  # macros used in Roblox. Please be aware of game-specific rules regarding macro usage
│   ├── robloxAntiAFK.py            # general macro that avoids 20-minute AFK kick by jumping every 5-10 minutes
│   ├── robloxIdleMafiaDeposit.py   # macro for auto-left clicking every 5 seconds, also includes standalone random jumping logic
│   ├── robloxWW3Edge.py            # macro specifically for ww3 commander
│   └── runner.py                   # wrapper to avoid roblox game servers admin catching your Discord Rich Presence red-handed
│
├── .gitignore                      # Hiding credential files
├── README.md                       <- YOU ARE HERE
├── tiramisu-req.txt                # pip install -r tiramisu-req.txt
├── transmit_phone.py               # setup a LAN endpoint for phone and/or other devices to obtain certain file from this computer
└── youtubeAudioPipeline.ipynb      # Automates downloading royalty-free music and embedding metadata
```
## `AdComTrainTimer.py` 
**Purpose**: To track time between [Exchange Express](https://adventurecommunist.fandom.com/wiki/Exchange_Express) and receive desktop notifications when one is about to arrive, best used when running [Adventure Communist on PC](https://play.google.com/pc-store/games/details?id=com.kongregate.mobile.adventurecommunist.google)

**Feature**: `tkinter` for Simple GUI, `asyncio` and `threading`to track GUI Events ... **BUT LOOK AT THE TIME!** Timer is **uninterrupted** while handling frontend click events. [`desktop_notifier`](https://pypi.org/project/desktop-notifier/) for receiving train arrival notice, so I don't need to waste time on actively monitoring the game tab

## `MilkywayEnhancing.ipynb`
**Purpose**: To simulate possible outcomes when using [Enhancing in Milky Way Idle](https://milkywayidle.wiki.gg/wiki/Enhancing#Success_Rate) for better in-game resource management and decision-making

**Feature**: Use Large sample size simulation inspired from [Monte Carlo Casino](https://en.wikipedia.org/wiki/Monte_Carlo_method) to find out **Extreme Percentiles** so that I prevent **TRYING TO BUILD A PYRAMID, BUT THERE IS NO MORE CLAY**

## `Zealots.ipynb`
**Purpose**: To simulate avg. zealot kills and its distribution on Hypixel Skyblock in order to drop a [Summoning Eye](https://hypixelskyblock.minecraft.wiki/w/Special_Zealot#Spawning). This is a good mental placebo even when I feel unlucky in a "zealot downswing", because **IN THIS CATHEDRAL, EVERY HEADSHOT IS A PRAYER ANSWERED**

**Feature**: Use Large sample size simulation inspired from [Monte Carlo Casino](https://en.wikipedia.org/wiki/Monte_Carlo_method) to find out **Mean**, **5-number summary**, **Standard Deviation** and optional **Data Visualization** using [`matplotlib.pyplot`](https://matplotlib.org/3.5.3/api/_as_gen/matplotlib.pyplot.html)


## `robloxAntiAFK.py`, `robloxIdleMafiaDeposit.py` and `robloxWW3Edge.py`
**Purpose**: Self-explanatory

**Feature**: Use [numpy](https://numpy.org/doc/stable/) for basic randomness pattern such as [Uniform](https://en.wikipedia.org/wiki/Discrete_uniform_distribution) and [Gaussian](https://en.wikipedia.org/wiki/Normal_distribution) when deciding input intervals to suit different in-game tactical needs

### WARNING: Use Macros at your own risk! While macro is not bannable by Roblox, it can be bannable in some specific games. Also, I don't think an ordinary University student is capable of outsmarting a team of Professional Cheat Detectives and Data Analysts. I am just trying to make my macro behaviour not the most blatant, but they will definitely be able to find data anomalies if they so wish, especially if left unattended for extended period of time e.g. sleeping overnight.

## `transmit_phone.py`
**Purpose**: To set up an endpoint so that other devices can directly download files specified by the code via LAN (e.g. mobile hotspot)

**Feature**: Use [flask](https://flask.palletsprojects.com/en/stable/) to set up a LAN-accessible endpoint, and use **Hard-coded folder path with no additional input route parameter** to control what files can be downloaded by other devices. 

### WARNING: Hard-coded folder path with no additional input route parameter is INTENDED DESIGN. There can be malicious devices inside the same LAN, and giving devices freedom of [Directory Traversal](https://en.wikipedia.org/wiki/Directory_traversal_attack) can be DISASTER, AN ABSOLUTE DISASTER!

## `youtubeAudioPipeline.ipynb`
**Purpose**: To automate the process of downloading royalty-free music, and attaching customizable metadata such as **Title**, **Artist**, **Cover Photo** and **Download Destination** for further processing

**Feature**: Use [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) to download royalty-free music, `PIL` for processing cover photo, and [`eyed3`](https://eyed3.readthedocs.io/en/v0.9.8/) for inserting file metadata, so that music can be downloaded in just one click, without relying on external websites and enduring their pop-up ads