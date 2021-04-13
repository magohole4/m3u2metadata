# m3u2metadata
Simple python script to fill metadata from a .m3u file to the files in a folder.
Currently works with mp3 and wav files

## Usage
```
python m3u2metadata.py <path-to-m3u-file> <path-to-root-folder>
```

## Why?
So I legally downloaded some music, but the files (mp3 & wav) weren't ordered and missed all cool metadata, I wanted the files ordered and thankfully the program that I used had created a .m3u file containing some metadata and the right order of the files.
So I created a simple program to set all the metadata.
It ended up being more difficult because I had to also create a simple RIFF parser (because all the other ones are sh\*t) and this format isn't very well documented frankly.

## Clone
Obviously do `git submodule update --init --recursive`

## Bugs
If you encounter a bug, your file doesn't work or something, submit an issue or do what you want.

## Warranty
No warranty, backup your files before running.

## N00b
Please notice that this is my first Python program, contanct me for advice on good practices, etc.

## License
Copyright (C) 2021  magohole

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
