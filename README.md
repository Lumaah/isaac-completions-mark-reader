# isaac-save-edit-script
A script in python to know what completions marks you have in the binding of isaac repentance (+).
This script uses code from https://github.com/jamesthejellyfish/isaac-save-edit-script
credits to jamesthejellyfish

## Opening your save file
Select the "Open Isaac Save File" menu item to locate your save file. By default, you will be navigated to your steam userdata folder. To find your save file, go to 
```
{steam_installation_path}\Steam\userdata\{steamid}\250900\remote\rep_persistengamedata{1|2|3}.dat
```
where {1|2|3} is either 1,2, or 3 depending on the save file you want to edit.
For non-steam users, your save file location is generally in Documents\My Games\Binding of Isaac Repentance\persistentgamedata{1|2|3}.dat

# How to use ?
put your save file in the same folder as the script and do:
```bash
python script_isaac.py rep_persistengamedata{1|2|3}.dat
```

