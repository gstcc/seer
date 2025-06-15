#!/bin/bash

cp "plugin/liveshare.py" "rplugin/python3/liveshare/__init__.py"
nvim "-u" "vimrc" "."
