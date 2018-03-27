# The Three-Body Problem Extractor
Tool for extracting / reformatting text from a PDF of the novel The Three-Body Problem (三体) by Cixin Liu.

If you happen to have a PDF copy of the novel The Three-Body Problem that has the SHA256 hash (`sha256sum`)
`b15ff4c7e26e0d58a250ed892f170e869ce435fd067ec8546f1bd0b25c00b429`, then you can use the tool `extract.py` in
this repo to reformat it into a plain text file (copy and paste doesn't work because the text comes out
with weird line breaks and the sidebar text randomly interspersed). You can then take this text file and do
things like increase the font size and make it double-spaced so that when you print it out you have room to
write notes between the lines.

To use `extract.py`, you will need the tool `pdftotext` installed on your machine, as well as a copy of 
Python 3.
