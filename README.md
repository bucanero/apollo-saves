# Apollo Save Game Database

[![License][img_license]][app_license]
![PS1 Titles](https://img.shields.io/github/directory-file-count/bucanero/apollo-saves/PS1?label=PS1%20Games&type=dir)
![PS2 Titles](https://img.shields.io/github/directory-file-count/bucanero/apollo-saves/PS2?label=PS2%20Games&type=dir)
![PS3 Titles](https://img.shields.io/github/directory-file-count/bucanero/apollo-saves/PS3?label=PS3%20Games&type=dir)
![PS4 Titles](https://img.shields.io/github/directory-file-count/bucanero/apollo-saves/PS4?label=PS4%20Games&type=dir)
![PSP Titles](https://img.shields.io/github/directory-file-count/bucanero/apollo-saves/PSP?label=PSP%20Games&type=dir)
![PSV Titles](https://img.shields.io/github/directory-file-count/bucanero/apollo-saves/PSV?label=PS%20Vita%20Games&type=dir)

## Introduction

The online save database project is part of [Apollo Save Tool](https://github.com/bucanero/apollo-ps3):
 - [PlayStation 2](https://github.com/bucanero/apollo-ps2) version
 - [PlayStation 3](https://github.com/bucanero/apollo-ps3) version
 - [PlayStation 4](https://github.com/bucanero/apollo-ps4) version
 - [PlayStation Portable](https://github.com/bucanero/apollo-psp) version
 - [PlayStation Vita](https://github.com/bucanero/apollo-vita) version

#### Contents:

 - [Introduction](#introduction)
 - [Exporting a save](#exporting-a-save)
 - [Uploading a save](#uploading-a-save)
 - [Advanced](#advanced)
    - [Database structure](#database-structure)
    - [Exporting a save manually](#exporting-a-save-manually)
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
`/PS3/EXPORT/XXXXXXXX.zip`

In the `EXPORT` folder you'll also find a `saves.txt` file, listing all exported `.zip`s with their Title-IDs and the save-game names.

## Uploading a save

To upload the zipped save file and share it with the community:

The simple way is to create a [GitHub issue](https://github.com/bucanero/apollo-saves/issues/new/choose) with the provided template, then you can write down the save description and upload the Zip file directly there (just drag&drop the `.zip`): https://github.com/bucanero/apollo-saves/issues/new/choose

### Alternative

If you don't know about GitHub (forks, pull requests, etc.), don't worry. Just upload the `.zip` file you created to [Mediafire](http://www.mediafire.com) or any other file-sharing service, then just send me [a message here](http://www.bucanero.com.ar) with the link and information/description so I can add it.

## Advanced

### Database structure

The database structure is simple:
 - Each game has a folder, named with the TITLE-ID. (e.g. `BLUS12345`)
 - game saves are stored in `.zip` files inside the game's TITLE ID folder.
 - The Zip filename must be `XXXXXXXX.zip`, where **X** can be a number from `0` to `9`. (`.zip` extension lowercase).
 - The Zip file must contain the save-game folder and data. (e.g. `MYGAME-DATA/*`)
 - Each folder has a `saves.txt` file that lists the available saves, with the description.
 - On the root, a file `games.txt` lists all the games/title-id's available.

**Note:** if the explanation is a bit confusing, please [browse the database](https://github.com/bucanero/apollo-saves/) and it should be self-explanatory.


### Uploading a save by pull request

If you're an advanced GitHub user, you can also:
 - Fork the project https://github.com/bucanero/apollo-saves
 - Add your save `12345678.zip` to the `BLES00000` folder
 - Edit `saves.txt` in the folder, adding `12345678.zip` with a short description
 - Submit the changes with a Pull Request
 - Then I'll merge the changes and the saves will be available to every user.

## License


[Apollo Save Tool](https://github.com/bucanero/apollo-saves/) Online Database - Copyright (C) 2020-2023 [Damian Parrino](https://twitter.com/dparrino)

This program is free software: you can redistribute it and/or modify
it under the terms of the [GNU General Public License][app_license] as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

[app_license]: https://github.com/bucanero/apollo-saves/blob/master/LICENSE
[img_license]: https://img.shields.io/github/license/bucanero/apollo-saves.svg?maxAge=2592000
