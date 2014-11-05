#! /usr/bin/env python
__author__ = 'Deniz'

import os
import sys
from tempfile import TemporaryFile
from subprocess import Popen, call, STDOUT

try:
    import SeleniumLibrary
except ImportError:
    print 'Importing SeleniumLibrary module failed.'
    print 'Please make sure you have SeleniumLibrary installed.'
    sys.exit(1)


ROOT = os.path.dirname(os.path.abspath(__file__))

def run_tests(args):
    start_selenium_server()
    call(['pybot'] + args, shell=(os.sep == '\\'))
    stop_selenium_server()

def start_selenium_server():
    logfile = open(os.path.join(ROOT, 'selenium_log.txt'), 'w')
    SeleniumLibrary.start_selenium_server(logfile)

def stop_selenium_server():
    SeleniumLibrary.shut_down_selenium_server()

def print_help():
    print __doc__

def print_usage():
    print 'Usage: Get_Most_Used_Champion.py [options] datasource'
    print '   or: Get_Most_Used_Champion.py selenium start|stop'
    print '   or: Get_Most_Used_Champion.py help'


if __name__ == '__main__':
    action = {'selenium-start': start_selenium_server,
              'selenium-stop': stop_selenium_server,
              'help': print_help,
              '': print_usage}.get('-'.join(sys.argv[1:]))
    if action:
        action()
    else:
        run_tests(sys.argv[1:])
