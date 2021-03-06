'''
Created on Jun 23, 2011

:authors: urbanus
'''
from toolbox.IBEnc import IBEnc
from toolbox.pairinggroup import *
import imp, inspect, os, re
import unittest
from schemes.ibenc_bb03 import IBE_BB04
from schemes.ibenc_bf01 import IBE_BonehFranklin
import all_unittests

#def suite():
#    suite = unittest.TestSuite()
#    ibe_names = ['ibe_bb03', 'ibe_bf03']
#    ibe_classes = collectSubClasses(IBEnc, ibe_names)
#    
#   for c in ibe_classes:
#        print("Testing ", c)
#        suite.addTest(Test("testEncDec").testclass=c)
#        
#    return suite

def autoDiscoverSchemes():
    '''Dynamically add a test method for each class'''
    ibe_names   = all_unittests.find_modules()
    ibe_classes = all_unittests.collectSubClasses(IBEnc, ibe_names)
    
    for c in ibe_classes:
        name = "test" + c.__name__
        M = "test message"
        group = PairingGroup('../param/d224.param', 1024)
        func = lambda *args, **kwargs : Test.myCorrectnessTest(c, group, M)
        setattr(Test, name, func)

#TODO: for ABE Enc interface tests
# * Different schemes operate on different groups. 
#   there needs to be a way for the testing framework to discover what group to use
# 
# * Different schemes have different domains (ie. expect strings or group elements)
#
# * Multiple instantiations of PairingGroup results in segmentation faults

class Test(unittest.TestCase):    
    def testIBE_bb03(self):
        group = PairingGroup('MNT224', 1024)
        M = group.random(GT)
        self.myCorrectnessTest(IBE_BB04, group, M)
    
    def testIBE_Franklin(self):
        group = PairingGroup('MNT224', 1024)
        M = "hello world!!"
        self.myCorrectnessTest(IBE_BonehFranklin, group, M)
    
    #@unittest.skip('automated discovery')
    def testAllIBEnc(self):
        ibe_names = all_unittests.find_modules()
        ibe_classes = all_unittests.collectSubClasses(IBEnc, ibe_names)
        
        group = PairingGroup('MNT224', 1024)
        for c in ibe_classes:
            print("Testing ", c)
            M = "test message"
            Test.myCorrectnessTest(c, group, M)
    
    @classmethod
    def myCorrectnessTest(self, scheme, group, M):
        '''Verifies that decrypt(encrypt(m)) == m'''
        # initialize the element object so that object references have global scope
        print(str(scheme))
        if re.match(".*adapt*.", str(scheme)):
            ibe = scheme(IBE_BB04(group), group)
        else:
            ibe = scheme(group)
        
        (params, mk) = ibe.setup()
    
        # represents public identity
        kID = group.random(ZR)
        key = ibe.extract(mk, kID)
    
        cipher = ibe.encrypt(params, kID, M)

        m = ibe.decrypt(params, key, cipher)
        self.assertTrue(m == M, "Decryption did not equal original message")        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    if os.access("schemes/", os.R_OK):
        os.chdir('schemes/')
    elif os.access("../schemes/", os.R_OK):
        os.chdir('../schemes/')
    #autoDiscoverSchemes()
    unittest.main()
