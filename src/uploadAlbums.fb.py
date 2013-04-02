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
import urllib
from re import search
import json

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
    
import facebook

FACEBOOK_APP_ID = "242045042608505"
FACEBOOK_APP_SECRET = "7d74ccba3763c16947ade8a56bb93c09"
# Be sure to enable offline_access permission in developers.facebook.com


def isTokenValid(token):
    ''' Receives token as string and returns boolean
    '''
    try:
        graph = facebook.GraphAPI(token)
        user = graph.get_object("me")
        #TODO: Hacer todas las operaciones necesarias, para ver q tengo tooodos los permisos necesarios
        return True
    except:
        #Send message to pushover here
        return False


def getValidToken():
    ''' Returns token in a string format
    '''
    FB_OAUTH_ENDPOINT="https://www.facebook.com/dialog/oauth"
    FB_REDIRECT_URI="https://www.facebook.com/connect/login_success.html"
    FB_PERMISSIONS="user_photos,user_videos,offline_access,publish_stream,photo_upload,video_upload"
    FB_OAUTH_LL_ENDPOINT="https://graph.facebook.com/oauth/access_token"


    args = {
           'client_id': FACEBOOK_APP_ID,
           'redirect_uri': FB_REDIRECT_URI,
           'scope': FB_PERMISSIONS,
           'response_type': 'token'
    }

    url = FB_OAUTH_ENDPOINT + "?" + urllib.urlencode(args)

    #Inform user
    print "Copy this url and paste it in a browser, then login to facebook to authorize it"
    print url 
    result = raw_input('When you are all done, paste here the resulting url: ')
  
    match = search("access_token=(\w*)&", result)
    if match == None: 
        print "Invalid URL"
        return None
    else:
        groups = match.groups()
        access_token = groups[0]
        print "Got access token!: " + access_token
        
        args = {
          'grant_type': 'fb_exchange_token',
          'client_id': FACEBOOK_APP_ID,
          'client_secret': FACEBOOK_APP_SECRET,
          'fb_exchange_token': access_token
        }
    
        url = FB_OAUTH_LL_ENDPOINT + "?" + urllib.urlencode(args)
        result =  urllib.urlopen(url).read()
        match = search("access_token=(\w*)&", result)
        if match == None:
            print "Invalid URL"
            return None
        else:
            groups = match.groups()
            long_lived_access_token = groups[0]
            print "Got long lived access token!: " + long_lived_access_token
            return long_lived_access_token


# Albums management
def getAllAlbums(token):
    '''  
    '''
    output = []
    graph = facebook.GraphAPI(token)
    user = graph.get_object("me")
    lastAfter="0"
     
    #Mientras que exista paging.next, itero
    while True:
        result = graph.get_connections(user["id"], "albums", limit="1", after=lastAfter)
        if result["data"] != []:
            #print result

            if not "count" in result["data"][0]: resultedNumPhotos=0
            else: resultedNumPhotos=result["data"][0]["count"]

            output.append({'name':result["data"][0]["name"],
                           'id':result["data"][0]["id"],
                           'numPhotos':resultedNumPhotos,
                          })
            if not "next" in result["paging"]:
                break
            else:
                lastAfter = result["paging"]["cursors"]["after"]
        else:
            break
    #print output
    return output


def getAlbumByName(token, albumName):
    '''  
    '''
    for album in getAllAlbums(token):
        if (album["name"] == albumName):
             return album
    return None


def isThereAlbum(token, albumName):
    ''' Returns boolean whether the album is already there 
    '''
    if getAlbumByName(token, albumName) == None:
        return False
    else:
        return True


def addAlbum(token, albumName, albumDesc=""):
    ''' Adds a new album 
    '''
    if not isThereAlbum(token, albumName):
        graph = facebook.GraphAPI(token)
        result = graph.put_object("me", "albums", message=albumDesc, name=albumName)
        #print result


def delAlbum(token, albumName):
    ''' Deletes an album NO FUNCIONA! 
    '''
    if isThereAlbum(token, albumName):
        graph = facebook.GraphAPI(token)
        result = graph.delete_object(getAlbumByName(token, albumName)["id"])
        print result




# Photo/Video management

def getAllObjects(token, albumName):
    '''  
    '''
    output = []
    if isThereAlbum(token, albumName):
        albumProps = getAlbumByName(token, albumName)
    
        graph = facebook.GraphAPI(token)
        lastAfter="0"

        #Mientras que exista paging.next, itero
        while True:
            result = graph.get_connections(albumProps["id"], "photos", limit="1", after=lastAfter)
            if result["data"] != []:
                #print result
                if not "name" in result["data"][0]: resultedName=""
                else: resultedName=result["data"][0]["name"]


                output.append({'name':resultedName,
                               'id':result["data"][0]["id"],
                              })
                if not "next" in result["paging"]:
                    break
                else:
                    lastAfter = result["paging"]["cursors"]["after"]
            else:
                break
    print "DEBUG: The objects retrieved were " + str(output)
    return output


def getObjectByName(token, albumName, objectName):
    '''  
    '''
    for objeto in getAllObjects(token, albumName):
        if (objeto["name"] == objectName):
             return objeto
    return None


def isThereObject(token, albumName, objectName):
    ''' Returns boolean whether the photo/video is already in the album
    '''
    if getObjectByName(token, albumName, objectName) == None:
        return False
    else:
        return True


def addPhoto(token, albumName, photoPath):
    ''' Adds a new photo to the selected album. This library must handle the restictions
        of the online service as number of photos per album, etc.
    '''
    if isThereAlbum(token, albumName):
        if not isThereObject(token, albumName, os.path.basename(photoPath)):
            graph = facebook.GraphAPI(token)
            result = graph.put_photo(open(photoPath), os.path.basename(photoPath), getAlbumByName(token, albumName)["id"])
            print result


def addVideo(token, albumName, videoPath):
    ''' Adds a new video to the selected album
        The aspect ratio of the video must be between 9x16 and 16x9, and the video cannot exceed 1024MB or 180 minutes in length.
    '''
    if isThereAlbum(token, albumName):
        if not isThereObject(token, albumName, os.path.basename(videoPath)):
            graph = facebook.GraphAPI(token)
            result = graph.put_video(open(videoPath), os.path.basename(videoPath), getAlbumByName(token, albumName)["id"])
            print result


def delObject(token, albumName, objectName):
    '''  
    '''
    if isThereAlbum(token, albumName):
        if isThereObject(token, albumName, objectName):
            graph = facebook.GraphAPI(token)
            result = graph.delete_object(getObjectByName(token, albumName, objectName)["id"])
            print result



#######################################################################################
#TODO:
# -Opciones de privacidad al subir albums, fotos y videos
# -MEtodos distintos para fotos y videos
# -Ver como linkar videos a albums
# -Subir a github el facebook.py updateado
#######################################################################################

# No Entry point
if __name__ == '__main__':
    try:
        token = "AAADcI4DIyXkBANP3M8UZCBrSDhZAP12iu5jIX2csoAEw8XjQhe0ZAFUGCJbgAXeZCGOLeGXQ83UGMQKsB1iDKJLtob8O3vHZAZBhRrMa0K6wZDZD" #goodvibesdude
        #token="AAADcI4DIyXkBAIpZCF34abKLsbs0mOjVUIIWVgo8w6pBa92zVy97AJ0MGLV49IZC2gLCHZBxReK3Vflg5wHnoa2EDWZAAUhm6PSHxqnZCgwZDZD" #debuti
        if not isTokenValid(token):
            token = getValidToken()

        #Test thereis methods
        print "Is there the album jokes? " + str(isThereAlbum(token, "jokes"))

        #Test add new album
        addAlbum(token, "jokes")
        print "The album details: " + str(getAlbumByName(token, "jokes"))

        #Test add new photo to album
        addPhoto(token, "jokes", os.path.join(realScriptDirectory, '..', 'test', 'albumsTest', 'album1', 'foto1.jpg'))

        #Test add new video to album
        addVideo(token, "jokes", os.path.join(realScriptDirectory, '..', 'test', 'albumsTest', 'album2', 'VID_20130115_032736.mp4'))
        
        #Test isthere methods
        print "Is there the photo foto1.jpg? " + str(isThereObject(token, "jokes", "foto1.jpg"))

        #Delete photo and video
        delObject(token, "jokes", "foto1.jpg")
        delObject(token, "jokes", "VID_20130115_032736.mp4")
   
        #Delete album
        #delAlbum(token, "jokes")

        pass
    
    except KeyboardInterrupt:
        print "Shutdown requested. Exiting"
    except SystemExit:
        pass
    except:
        logging.error("Unexpected error:" + traceback.format_exc())
        raise
