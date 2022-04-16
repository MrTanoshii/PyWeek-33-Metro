<div align="center">

[![PyWeek 33](https://img.shields.io/badge/PyWeek-33-blue)](https://pyweek.org/33/)
[![PyWeek 33 Rules - Revision 2020-02-06](https://img.shields.io/badge/Rules-2020--02--06-blue)](https://pyweek.readthedocs.io/en/latest/rules.html)
[![Team Metroids](https://img.shields.io/badge/Team-Metroids-brightgreen)](https://pyweek.org/e/meme_py123/)
[![Game Name - Metro](https://img.shields.io/badge/Game-Metro-brightgreen)](https://pyweek.org/e/meme_py123/)
[![Game Theme - My evil twin](https://img.shields.io/badge/Game%20Theme-My%20evil%20twin-blue)](https://pyweek.org/p/37/)
[![Game Rating](https://img.shields.io/badge/Game%20Rating-5th%20place-blue)](https://pyweek.org/33/ratings/)

</div>
<div align="center">

[![Python v3.10](https://img.shields.io/badge/Python-v3.10-blue)](https://docs.python.org/3.10/)
[![Arcade v2.6.13](https://img.shields.io/badge/Arcade-v2.6.13-blue)](https://api.arcade.academy/en/2.6.13/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-blue)](https://www.ffmpeg.org/download.html)

</div>
<div align="center">

[![Python Check](https://github.com/MrTanoshii/PyWeek-33-Metro/actions/workflows/python_check.yml/badge.svg)](https://github.com/MrTanoshii/PyWeek-33-Metro/actions/workflows/python_check.yml)
[![codecov](https://codecov.io/gh/MrTanoshii/PyWeek-33-Metro/branch/main/graph/badge.svg?token=V2Q6AALIKQ)](https://codecov.io/gh/MrTanoshii/PyWeek-33-Metro)

</div>

# PyWeek 33 | Team Pastafobia | The Epic of Goat

## Repo status: Active

PyWeek 33 has ended on the 27th of March 2022 at 0000 UTC

Submitted version:
https://github.com/MrTanoshii/PyWeek-33-Metro/releases/tag/v1.1.0

Further development:
`main` branch

## Featuring

- Jeb | https://github.com/JesperKauppinen
- MrTanoshii | https://github.com/MrTanoshii
- Memehunter | https://github.com/mohith01
- Cat | https://github.com/Catto-YFCN
- Krzysztof | https://github.com/IrrationalBoolean
- ATC_Tower | https://github.com/BriscoRP

## Operating System

|      OS | Status               |
| ------: | :------------------- |
|   Linux | Fully Supported      |
|   macOS | Should run, untested |
| Windows | Fully Supported      |

## Required Dependencies

| Dependencies | Version | Function                              |
| -----------: | :-----: | :------------------------------------ |
|       Python |  V3.9   | https://www.python.org/               |
|       Arcade | V2.6.13 | https://api.arcade.academy/en/2.6.13/ |
|       FFmpeg | V2.6.11 | https://www.ffmpeg.org/download.html  |

Note: Python dependencies may be installed using the `pip install -r requirements.txt` command

## Running the game from source

```shell
python run_game.py
```

## How to play

### Controls

|         Controls | Function     |
| ---------------: | :----------- |
|             WASD | Move         |
|       Arrow Keys | Move         |
|         Spacebar | Shoot        |
| Left Mouse Click | Shoot        |
|                R | Reload       |
|              1-4 | Swap Weapons |
|           Escape | Pause        |

## Packaging the game using PyInstaller

### Windows

```shell
pip install -r requirements-dev.txt
pip install pypiwin32
pyinstaller The_Epic_of_Goat.spec
```

## [License](https://github.com/MrTanoshii/PyWeek-33-Metro/blob/main/LICENSE)

## Assets Licenses

Individual assets licenses are available in their respective directory `README.md`s

Assets that do not have their own `README.md`s can be assumed to have been produced internally and are thus licensed under the project license
