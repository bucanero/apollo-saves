# Z-SaveGame Online Database

[![License][img_license]][app_license]
![PS2 Titles](https://img.shields.io/github/directory-file-count/z-jailbreak/Z-Saves/PS2?label=PS2%20Games&type=dir)
![PS3 Titles](https://img.shields.io/github/directory-file-count/z-jailbreak/Z-Saves/PS3?label=PS3%20Games&type=dir)
![PS4 Titles](https://img.shields.io/github/directory-file-count/z-jailbreak/Z-Saves/PS4?label=PS4%20Games&type=dir)
![PSP Titles](https://img.shields.io/github/directory-file-count/z-jailbreak/Z-Saves/PSP?label=PSP%20Games&type=dir)
![PSV Titles](https://img.shields.io/github/directory-file-count/z-jailbreak/Z-Saves/PSV?label=PS%20Vita%20Games&type=dir)

## Introduction

The online save database project is part of [Apollo Save Tool](https://github.com/bucanero/apollo-ps3):
 - [PlayStation 2](https://github.com/bucanero/apollo-ps2) version
 - [PlayStation 3](https://github.com/bucanero/apollo-ps3) version
 - [PlayStation 4](https://github.com/bucanero/apollo-ps4) version
 - [PlayStation Vita](https://github.com/bucanero/apollo-vita) version
 - [PlayStation Portable](https://github.com/bucanero/apollo-psp) version

#### Contents:

 - [Introduction](#introduction)
 - [Exporting a save](#exporting-a-save)
 - [Advanced](#advanced)
    - [Database structure](#database-structure)
    - [Uploading a save by pull request](#uploading-a-save-by-pull-request)
 - [License](#license)

## Exporting a save

To start, I'll assume you already have the latest version of Apollo installed. You'll also need a USB drive (FAT32) connected to your PS3 to save the exported `.zip` file.

**Steps:**

 - Within the app, browse your HDD/USB saves
 - Select the save-game you want to export
 - From the options, select `Export save game to Zip`
 - Next, select to which USB port you want to save (USB 0 or 1).
 - Wait for the `.zip` export file to be generated.

If everything went well, you'll have the exported `.zip` file ready on your USB storage device here:
`/PS4/EXPORT/XXXXXXXX.zip`

In the `EXPORT` folder you'll also find a `saves.txt` file, listing all exported `.zip`s with their Title-IDs and the save-game names.

## Advanced

### Database structure

The database structure is simple:
 - Each game has a folder, named with the TITLE-ID. (e.g. `CUSA12345`)
 - game saves are stored in `.zip` files inside the game's TITLE ID folder.
 - The Zip filename must be `XXXXXXXX.zip`, where **X** can be a number from `0` to `9`. (`.zip` extension lowercase).
 - The Zip file must contain the save-game folder and data. (e.g. `MYGAME-DATA/*`)
 - Each folder has a `saves.txt` file that lists the available saves, with the description.
 - On the root, a file `games.txt` lists all the games/title-id's available.

**Note:** if the explanation is a bit confusing, please [browse the database](https://z-jailbreak.github.io/Z-Saves/) and it should be self-explanatory.


### Uploading a save by pull request

If you're an advanced GitHub user, you can also:
 - Fork the project https://github.com/z-jailbreak/Z-Saves
 - Add your save `12345678.zip` to the `BLES00000` folder
 - Edit `saves.txt` in the folder, adding `12345678.zip` with a short description
 - Submit the changes with a Pull Request
 - Then I'll merge the changes and the saves will be available to every user.

## License


[Apollo Save Tool Original](https://github.com/bucanero/apollo-saves/) Online Database - Copyright (C) 2020-2023 [Damian Parrino](https://twitter.com/dparrino)

This program is free software: you can redistribute it and/or modify
it under the terms of the [GNU General Public License][app_license] as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[app_license]: https://github.com/bucanero/apollo-saves/blob/master/LICENSE
[img_license]: https://img.shields.io/github/license/bucanero/apollo-saves.svg?maxAge=2592000
