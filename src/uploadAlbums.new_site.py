#!/usr/bin/env python
###############################################################################################
#  Author: 
__author__ = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program: 
__program__ = 'uploadAlbums.new_site'
# Package:
__package__ = ''
# Descrip: 
__description__ = '''Uploads the personal photo repository to ...'''
# Version: 
__version__ = '0.0.0'
#    Date:
__date__ = 'YYYYMMDD'
# License: This script doesn't require any license since it's not intended to be redistributed.
#          In such case, unless stated otherwise, the purpose of the author is to follow GPLv3.
# History: 
#          0.0.0 (YYYYMMDD)
#            -Initial release
###############################################################################################

# Imports
import logging
import sys
import doctest
import datetime, time
import os
import optparse
import inspect
import ConfigParser
import glob
import traceback

# Parameters, Globals n' Constants
KIBI = 1024
MEBI = 1024 * KIBI
LOG_MODE = "Screen"
LOG_LEVEL = logging.DEBUG
LOG_MAX_BYTES = 1 * MEBI

realScriptPath = os.path.realpath(__file__)
realScriptDirectory = os.path.dirname(realScriptPath)
callingDirectory = os.getcwd()
if os.path.isabs(__file__ ):
    linkScriptPath = __file__
else:
    linkScriptPath = os.path.join(callingDirectory, __file__)
linkScriptDirectory = os.path.dirname(linkScriptPath)

propertiesName = __program__ + ".properties"
propertiesPath = os.path.join(realScriptDirectory, '..', propertiesName) 

logFileName = __program__ + '_' + time.strftime("%Y%m%d%H%M%S") + '.log'
logDirectory = os.path.join(realScriptDirectory, '..', 'logs')
logPath = os.path.join(logDirectory, logFileName)
loggerName = __package__ + "." + __program__

# User-libs imports (This is the correct way to do this)
libPath =  os.path.join(realScriptDirectory, '..', 'lib')
sys.path.insert(0, libPath)
for infile in glob.glob(os.path.join(libPath, '*.*')):
    sys.path.insert(0, infile)
    

#NEWSITE_APP_ID = "242045042608505"
#NEWSITE_APP_SECRET = "7d74ccba3763c16947ade8a56bb93c09"
# Be sure to enable offline_access permission in developers.facebook.com

def isTokenValid(token):
    ''' Receives token as string and returns boolean
    '''


def getValidToken():
    ''' Returns token in a string format
    '''
     

def addAlbum(albumName):
    ''' Adds a new album 
    '''


def isThereAlbum(albumName):
    ''' Returns boolean whether the album is already there 
    '''


def addPhoto(albumName, photoPath):
    ''' Adds a new photo to the selected album. This library must handle the restictions
        of the online service as number of photos per album, etc.
    '''


def isTherePhoto():
    ''' Returns boolean whether the photo is already in the album
    '''


def addVideo(albumName, videoPath):
    ''' Adds a new video to the selected album
    '''


def isThereAlbum(albumName):
    ''' Returns boolean whether the video is already in the album
    '''


def init():
    '''
    '''


# No Entry point
if __name__ == '__main__':
    try:
        # Testing porpouse
        token="olakease"
        if not isTokenValid(token):
            token=getValidToken()
	graph = facebook.GraphAPI(token)
        user = graph.get_object("me")
        friends = graph.get_connections(user["id"], "friends")
        pass
    
    except KeyboardInterrupt:
        print "Shutdown requested. Exiting"
    except SystemExit:
        pass
    except:
        logging.error("Unexpected error:" + traceback.format_exc())
        raise
