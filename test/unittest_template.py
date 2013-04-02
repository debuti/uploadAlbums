#!/usr/bin/env python
###############################################################################################
#  Author:
_author = '<a href="mailto:debuti@gmail.com">Borja Garcia</a>'
# Program:
_name = 'PACKAGE test'
# Descrip:
_description = '''PACKAGE Test'''
# Version:
_version = '0.0.0'
#    Date: 
_date = 'YYYY-MM-DD:HH:mm:ss'
# License: This script doesn't require any license since it's not intended to be redistributed.
#          In such case, unless stated otherwise, the purpose of the author is to follow GPLv3.
# History: 0.0.0 (YYYY-MM-DD:HH:mm:ss)
#            -Initial release
###############################################################################################


import unittest
import sys, os
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "src")))
import PACKAGE

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        ''' This code is executed before each test
        '''
        ##Crea una secuencia de numeros en este objeto
        ##self.seq = range(10)
        #print "Hi setUp"

    def tearDown(self):
        ''' This code is executed after each test
        '''
        #print "Hi tearDown"

# Examples
    def testpwd(self):
        ''' Test for pwd method
        '''
        #Types and variables for this test
        
        # Call software under test
        firstTest = shellutils.pwd()
        
        # Verify results
        self.assertEqual(firstTest, shellutils.runBash("pwd"))

    def testls(self):
        ''' Test for ls method
        '''
        #Types and variables for this test
        
        # Call software under test
        firstTest = shellutils.ls()
        
        # Verify results
        self.assertEqual(firstTest, shellutils.runBash("ls --almost-all").split("\n"))
# /Examples

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
    unittest.TextTestRunner(verbosity=3).run(suite)
