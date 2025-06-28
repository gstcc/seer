#!/bin/bash

cp "plugin/liveshare.py" "rplugin/python3/liveshare/__init__.py"
cp "plugin/server.py" "rplugin/python3/liveshare/server.py"
nvim "-u" "vimrc" "."
