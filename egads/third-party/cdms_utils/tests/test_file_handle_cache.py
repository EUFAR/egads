# Import python modules
import os
import glob

# Import third-party software
import nose

from cdms_utils.file_handle_cache import FileHandleCache

openFileList = []

def openFileFunc(path, mode='r+'):
    global openFileList
    openFileList.append( (path, mode) )
    return MockFileHandle(path, mode)

class MockFileHandle(object):
    
    def __init__(self, name, mode):
        self.closed = False
        self.name = name
        self.mode = mode
        
    def close(self):
        self.closed = True
    
class TestFileHandleCache(object):
    
    def setUp(self):
        self.fhc = FileHandleCache()
        filePath1 = "/path/to/a/file.ext"
        filePath2 = "/path/to/another/file.ext"
        filePath3 = "file3"
        filePath4 = "/file/number/four"
        filePath5 = "/the/fifth/file/somename.txt"
        self.pathList = [filePath1, filePath2, filePath3, filePath4, filePath5]
        
    def tearDown(self):
        self.fhc = None
        self.pathList = None
        
    def testDefaultSizeLimit(self):
        assert(self.fhc.limit == 1000)
        
    def testOpensAFileIntoDictionary(self):
        self.fhc.openFile(openFileFunc, self.pathList[0])
        assert(len(self.fhc) == 1)
        cachedFile =self.fhc.d[self.pathList[0]]
        assert(cachedFile.__class__ == MockFileHandle)
        assert(cachedFile.name == self.pathList[0])
        assert(cachedFile.mode == 'r')
        
    def testClosesAFile(self):
        self.fhc.openFile(openFileFunc, self.pathList[0])
        cachedFile =self.fhc.d[self.pathList[0]]
        self.fhc.closeFile(self.pathList[0])
        assert(cachedFile.closed == True)
        assert(len(self.fhc) == 0)
        
    def testClosesAllFiles(self):
        fileHandles = []
        for path in self.pathList:
            self.fhc.openFile(openFileFunc, path)
            fileHandles.append(self.fhc.d[path])
            
        self.fhc.closeAll()
        
        for handle in fileHandles:
            assert(handle.closed == True)
            
    def testClosesFileAfterReachingLimit(self):
        self.fhc.limit = len(self.pathList) - 1
        fileHandles = []
        for path in self.pathList:
            self.fhc.openFile(openFileFunc, path)
            fileHandles.append(self.fhc.d[path])
       
        #check that the first file has been closed and deleted
        assert(fileHandles[0].closed == True)
        assert(fileHandles[0] not in self.fhc.d.values())
        
        #check that the rest are still open
        for handle in fileHandles[1:]:
            assert(handle.closed == False)
            assert(handle == self.fhc.d[handle.name])
    
    def testRaisesExceptionWhenClosingAFileNotInCache(self):
        #put a couple of files into the cache just to give it something to search
        self.fhc.openFile(openFileFunc, self.pathList[0])
        self.fhc.openFile(openFileFunc, self.pathList[1])
        
        nose.tools.assert_raises(Exception,
                                self.fhc.closeFile,
                                self.pathList[2])
        
        
        
# Magic to run tests if executed as a script
if __name__ == '__main__':

    nose.main(defaultTest='test_file_handle_cache')
        
    
