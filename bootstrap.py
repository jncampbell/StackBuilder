#!/usr/bin/env python

open("/tmp/__init__.py", "a") #We can't import the StackBuilder without this
from stackBuilder import StackBuilder
builder = StackBuilder()

# Start building your stack

builder.python_software_properties()
builder.build_essential()
# builder.apache()
# builder.nginx()
# builder.curl()
# builder.php()
# builder.mysql()
# builder.emacs()
# builder.vim()
# builder.git()
# builder.php()
builder.composer()
builder.nodejs()
# builder.npm_install_globally("gulp")
# builder.npm_install_globally("bower")
# builder.npm_install("gulp-sass")
