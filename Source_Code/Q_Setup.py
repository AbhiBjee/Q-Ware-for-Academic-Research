# -*- coding: utf-8 -*-

# An advanced setup script to create multiple executables and demonstrate a few
# of the features available to setup scripts
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import sys
from cx_Freeze import setup, Executable

#Dependencies are automatically detected, but it might need fintuning.

build_options = {'packages':[], 'excludes':[]}

base = 'Win32GUI' if sys.platform=='win32' else None

##options = {
##    'build_exe': {
##        'includes': [
##            'testfreeze_1',
##            'testfreeze_2'
##        ],
##        'path': sys.path + ['modules']
##    }
##}

executables = [
    Executable('QwareOpen.py', base=base)
    
]

setup(name='QSTM Q-Ware',
      version='1.2',
      description='Software for Digital Manual Therapy and Soft Tissue Manipulation',
      options= {'build_exe': build_options},
      executables=executables
      )
