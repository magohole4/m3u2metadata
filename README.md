# m3u2metadata
Simple python script to fill metadata from a .m3u file to the files in a folder.
Currently works with mp3 and wav files

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
