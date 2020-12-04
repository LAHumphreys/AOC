import os


def GetFilePath(testModuleFile, relPath):
    dir = os.path.dirname(os.path.abspath(testModuleFile))
    return os.path.join(dir, relPath)
