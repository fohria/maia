# Maia install instructions

You need to install the following applications:
- Java JDK (http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
- Minecraft (http://www.minecraft.net)
- nodeJS (http://www.nodejs.org)
- Python 2.7 (http://www.python.org)
- NBT Explorer (optional; http://www.minecraftforum.net/forums/mapping-and-modding/minecraft-tools/1262665-nbtexplorer-nbt-editor-for-windows-and-mac)

You also need these addons for Python:
- Pywin32 (http://sourceforge.net/projects/pywin32/)
- Microsoft Python C++ compiler: http://aka.ms/vcpython27 (required by numpy)

With Python installed, install the following packages with PIP:
- numpy (pip install numpy)
- pillow (pip install pillow)
- websockets (pip install websocket-client)
- dill (pip install dill)

And, finally, the CanaryMod server (https://canarymod.net/releases/) with RaspberryJuice plugin (https://github.com/martinohanlon/CanaryRaspberryJuice). A prepared server with most settings done can be found here: (link to minecraft-server.zip)

## Further instructions

1. If Minecraft was not already installed on your computer, start it up and create a new single player game and then exit. This will create the option file.
2. Edit options file, located in %appdata%/.minecraft/options.txt and set pauseOnLostFocus to false
3. Run start.bat in minecraft-server folder, it should generate world and inform that raspberryjuice plugin is enabled
4. Run server.js file in maia/api folder
5. Run Minecraft, select multiplayer and connect to localhost
6. In the Minecraft video settings, set particles to minimum
7. Go to the console window running the Minecraft server and enter the following commands:
- /give playername iron_sword (exchange playername with your name)
- /time set day
- /gamerule doDaylightCycle false
- /weather clear 1000000
- /gamerule doTileDrops false
8. Exit Minecraft and shut down the server with the 'stop' command in the server console
9. Open NBT Explorer, navigate to the worlds/players/UUID.dat file and open that
10. Set 'invulnerability' to 1

The invulnerability setting is a workaround for an issue where player sometimes fell to its death, despite walking around on flat ground

If you downloaded CanaryMod and CanaryRaspberryJuice plugin on your own, these commands may also be useful to enter in the server console:
- /effect playername 8 1000000 255 false
- /op playername (or blocks will respawn instantly)

You may also want to edit the world config file and set these values:
enable-experience=false
enable-health=false
spawn-villagers=false
spawn-golems=false
spawn-animals=true
spawn-monsters=false
difficulty=0
