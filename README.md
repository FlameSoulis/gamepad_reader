# Gamepad Reader

This is just a simple python script, originally written for NeosVR, to host the button presses occuring on a controller to be presented in VR.

This is just a project I did for fun. It has been tested to work on a SteamDeck, even while in Steam's main UI.

## Prerequisites

You will need [pygame](https://github.com/pygame/pygame) and [websocket-server](https://github.com/Pithikos/python-websocket-server).

```
pip install pygame websocket-server
```

This was originally created for pygame 2.2.0 and websocket-server 0.6.4 with [Python](https://www.python.org/) 3.10.9. It has been tested on Windows 10 and SteamOS 3.4.6, but should play safely on most Linux distributions.