#not fin

import json

with open('/home/anja/Desktop/cornell movie-dialogs corpus/raw_script_urls.txt', 'r', encoding = 'latin-1') as f:
    fi = f.readlines()

for i in range(len(fi)):
    fi[i] = fi[i].split(' +++$+++ ')