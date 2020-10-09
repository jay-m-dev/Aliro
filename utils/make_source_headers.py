"""~This file is part of the PennAI library~

Copyright (C) 2017 Epistasis Lab, University of Pennsylvania

PennAI is maintained by:
    - Heather Williams (hwilli@upenn.edu)
    - Weixuan Fu (weixuanf@pennmedicine.upenn.edu)
    - William La Cava (lacava@upenn.edu)
    - Michael Stauffer (stauffer@upenn.edu)
    - and many other generous open source contributors

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

(Autogenerated header, do not modify)

"""
import os
from pathlib import Path

with open('utils/source_file_header.txt','r') as f:
    header = f.read()
identifier = "~This file is part of the PennAI library~" 

exts = ['.py','.jsx','.js']
newline = '\n'

# get file paths recursively
python_files = Path('./').rglob('*.py') 
json_files = list(Path('./').rglob('*.js'))
json_files += list(Path('./').rglob('*.jsx')) 

py_comment = '"""'
python_header = py_comment + header + newline + py_comment
js_comment = '/*' 
json_header = js_comment + ' ' + header + newline + js_comment[::-1] 

# print('python_header',python_header)
# print('json_header',json_header)

def cut_data(data,comment,identifier):
    id_idx = data.find(identifier)
    start = data.rfind(comment,0,id_idx)
    end = data.find(comment[::-1], id_idx) + len(comment)+len(newline)
    print('header found for',f,' rewriting')
    data = data[:start] + data[end:]
    return data

# recurse thru files and add header w/ appropriate block comments
for f in python_files:
    with open(f, 'r') as original: 
        data = original.read()
    if identifier in data:
        data = cut_data(data, py_comment, identifier)
    print('updating',f)
    with open(f, 'w') as modified: 
        modified.write(python_header + newline+ data)

for f in json_files:
    if any([jf in str(f) for jf in ['node_modules','dist']]):
        continue
    with open(f, 'r') as original: 
        data = original.read()
    if identifier in data:
        data = cut_data(data, js_comment, identifier)
    print('updating',f)
    with open(f, 'w') as modified: 
        modified.write(json_header + newline+ data)