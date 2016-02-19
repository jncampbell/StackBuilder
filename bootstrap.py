#!/usr/bin/env python

#We need this so we can import the StackBuilder
open("/tmp/__init__.py", "a")
from stackBuilder import StackBuilder

builder = StackBuilder()

# call stackBuilder methods here
builder.installBuildDependencies()
builder.nodejs()
builder.npmInstallGlobally("gulp")
builder.npmInstallGlobally("bower")
builder.npmInstall("gulp-sass")
