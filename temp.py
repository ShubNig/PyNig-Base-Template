#!/usr/bin/env python
# coding=utf-8

#####################################################
# ghtoc   : markdown folder toc generator
# Author  : sinlov <sinlovgmppt@gmail.com>
# Usage   : toc.py <markdown file>
# Date    : 2016-10-24
# License : see https://github.com/sinlov/markdown-folder-toc
# Copyright (C) 2016 sinlov
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
import os
import re
import sys
import optparse

__author__ = 'sinlov'

is_verbose = False
top_level = 1
folder_path = os.getcwd()

hint_help_info = """
more information see
"""

error_info = """
Your input error
    Usage:
        ./temp.py --help
    or input [-h] to see help
"""


if __name__ == '__main__':
    folder_path = ''
    if len(sys.argv) < 2:
        print error_info
        exit(1)
    parser = optparse.OptionParser('\n%prog ' + ' -p \n\tOr %prog <folder>\n' + hint_help_info)
    parser.add_option('-v', dest='v_verbose', action="store_true", help="see verbose", default=False)
    parser.add_option('-f', '--folder', dest='f_folder', type="string", help="path of folder Default is .",
                      default=".", metavar=".")
    parser.add_option('-l', '--level', dest='l_level', type="int", help="top level Default 77",
                      default=77, metavar=77)
    (options, args) = parser.parse_args()
    if options.v_verbose:
        is_verbose = True
    if options.l_level is not None:
        top_level = options.l_level
    if options.f_folder is not None:
        folder_path = options.f_folder
    if not is_verbose:
        print 'todo what you want before'
        exit(1)
    if not os.path.exists(folder_path):
        print "Your input Folder is not exist " + folder_path
        exit(1)
    if os.path.isdir(folder_path) < 1:
        print "You input " + folder_path + "is not folder"
        exit(1)
