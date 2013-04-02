#!/usr/bin/env python
###############################################################################################
#  Author: 
__author__ = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program: 
__program__ = 'uploadAlbums'
# Package:
__package__ = ''
# Descrip: 
__description__ = '''Uploads the personal photo repository to several online photo websites'''
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
import imp

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
    
#import thepyutilities.shellutils as shellutils


# Usage function, logs, utils and check input
def openLog(mode, desiredLevel):
    '''This function is for initialize the logging job
    '''
    def openScreenLog(formatter, desiredLevel):
        logging.basicConfig(level = desiredLevel, format = formatter)
       
    def openScreenAndFileLog(fileName, formatter, desiredLevel):
        logger = logging.getLogger('')
        logger.setLevel(desiredLevel)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(fileName)
        fh.setLevel(desiredLevel)
        fh.setFormatter(formatter)
        # add the handler to logger
        logger.addHandler(fh)

    def openScreenAndRotatingFileLog(fileName, formatter, desiredLevel, maxBytes):
        logger = logging.getLogger('')
        logger.setLevel(desiredLevel)
        # create file handler which logs even debug messages
        fh = logging.handlers.RotatingFileHandler(fileName, maxBytes)
        fh.setLevel(desiredLevel)
        fh.setFormatter(formatter)
        # add the handler to logger
        logger.addHandler(fh)

    format = "%(asctime)-15s - %(levelname)-6s - %(message)s"
    formatter = logging.Formatter(format)
    # Clean up root logger
    for handler in logging.getLogger('').handlers:
        logging.getLogger('').removeHandler(handler)
    openScreenLog(format, desiredLevel)
    
    if mode == "File" or mode == "RollingFile":
        if not os.path.isdir(logDirectory):
            shellutils.mkdir(logDirectory)
  
        if mode == "File":
            openScreenAndFileLog(logPath, formatter, desiredLevel)
    
        elif mode == "RollingFile":
            openScreenAndRotatingFileLog(logPath, formatter, desiredLevel, LOG_MAX_BYTES)

def closeLog():
    '''This function is for shutdown the logging job
    '''
    logging.shutdown()


def checkInput():
    '''This function is for treat the user command line parameters.
    '''
    # Create instance of OptionParser Module, included in Standard Library
    p = optparse.OptionParser(description=__description__,
                              prog=__program__,
                              version=__version__,
                              usage='''%prog [options]''') 
    # Define the options. Do not use -h nor -v, the are reserved to help and version automaticly
    p.add_option('--file','-f', action="store", type="string", dest="filename", help='The configuration file')

    # Parse the commandline
    options, arguments = p.parse_args()

    # Decide what to do
    if options.filename is None:
        p.print_help()
        sys.exit(-1)
    else:
        if not (os.path.exists(options.filename) and os.path.isfile(options.filename)):
            print "File not found"
            sys.exit(-1)
        else:
            propertiesFilename = options.filename
            return [propertiesFilename]



# Helper functions
def readConfig(propertiesPath):
    '''This procedure returns the program properties file
    '''
    config = ConfigParser.RawConfigParser()
    config.read(propertiesPath)
    return config

    
def saveConfig(config, propertiesPath):
    '''This procedure returns the program properties file
    '''
    configfile = open(propertiesPath, 'wb')
    config.write(configfile)
    configfile.close()

def getLocalAlbums(albumsPath):
    '''
    '''
    


# Main function
def core(propertiesFilename):
    '''This is the core, all program logic is performed here
    '''
    properties = readConfig(propertiesFilename)

    name = properties.get('General', 'name')
    if name == "":
        logging.error("You should supply a name")
        sys.exit(-2)

    service = properties.get('General', 'service')
    if service == "":
        logging.error("You should supply a valid service")
        sys.exit(-2)

    visibility = properties.get('General', 'visibility')
    if name == "":
        logging.error("You should supply a valid visibility")
        sys.exit(-2)

    token = properties.get('General', 'token')

    #TODO: Test if path is absolute or relative. now i assume its relative
    albumsPath = properties.get('General', 'path')
    albumsPath = os.path.join(os.path.dirname(propertiesFilename), albumsPath)
    if not (os.path.exists(albumsPath) and os.path.isdir(albumsPath)):
        logging.error("You should supply a existing albums path")
        sys.exit(-2)

    # OK so readed settings are
    logging.debug("name: " + name)
    logging.debug("token: " + token)
    logging.debug("albumsPath: " + albumsPath)
    logging.debug("service: " + service)
    logging.debug("visibility: " + visibility)

    (file, pathname, description) = imp.find_module(__program__+"."+service)
    serviceModule = imp.load_module(__program__+"."+service, file, pathname, description)
    
    # Verify valid token
    if not serviceModule.isTokenValid(token):
        token = serviceModule.getValidToken()
        logging.debug("Adquired new token: " + token)
        properties.set('General', 'token', token)
        saveConfig(properties, propertiesFilename)

    # Main loop
    for album in  getLocalAlbums(albumsPath):
        if not serviceModule.isThereAlbum(album["name"]):
            serviceModule.addAlbum(token, albumName, albumDesc=""):


    # DO STUFF HERE
#Cojer las properties del archivo de config: nombre, path, tipo (fb, picasa, etc), authkey, visibility
#Cargar el modulo que sea (fb, google,..) - verificar authkey y permisos de fbcmd o de googlecl
#Recorrer el path buscando directorios q sean albums
#  Si no existe
#    hacer album fbcmd ADDALBUM title desc location privacy
#    cargar todas las fotos fbcmd ADDPIC filename albumId basename.jpg
#  Si ya existe
#    comprobar para cada foto si hay alguna con el caption igual
#    si no existe ninguna con el caption igual se sube fbcmd ADDPIC filename albumId basename.jpg
#TODO: COMO SUBO VIDEOS?

    saveConfig(properties, propertiesFilename)
    

def main():
    '''This is the main procedure, is detached to provide compatibility with the updater
    '''
    openLog(LOG_MODE, LOG_LEVEL)
    [propertiesFilename] = checkInput()
    core(propertiesFilename)
    closeLog()


# Entry point
if __name__ == '__main__':
    try:
        main()
    
    except KeyboardInterrupt:
        print "Shutdown requested. Exiting"
    except SystemExit:
        pass
    except:
        logging.error("Unexpected error:" + traceback.format_exc())
        raise
