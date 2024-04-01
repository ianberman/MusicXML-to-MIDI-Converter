Simple converter script for MusicXML files to midi files. 

Requires music21, which runs on python 3.10+
https://web.mit.edu/music21/doc/usersGuide/usersGuide_01_installing.html

run with `python convert.py input_dir output_dir` with optional flag `--verbose` for print statements.

Right now, if your input xml file has multiple parts/voices, this will be preserved in the output midi file, so when you drag it into ableton for instance each voice will appear as a separate clip. I don't have a reason to change this behavior currently but if people end up using this I can look into an option to combine this.
