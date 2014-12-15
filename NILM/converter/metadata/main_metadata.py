from os.path import isdir, isfile, join, splitext
import yaml
import json




name2='/Users/thibaut/GitHub/NILM/BLUED_Python/converter/metadata/metadata_user1.json'
isfile(name2)

with open(name2) as fh:
     b= json.load(fh)