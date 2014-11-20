import sys
import Globals
import Visitors
import zipfile
import os
import datetime
from threading import Thread

argc = len(sys.argv)
if argc == 3:
    dirPath = sys.argv[1]
    options = int(sys.argv[2])

    files = []
    inputDirPath = os.path.join(dirPath, Globals.inputDirName)
    for (root, dirnames, filenames) in os.walk(inputDirPath):
        for file in filenames:
            files.append(os.path.join(root, file))
        break              

    outputDir = os.path.join(dirPath, Globals.outputDirName)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        
    threads = []
    for filename in files:
        params = (filename, dirPath, options)
        thread = Thread(target = Globals.changeFile, args = params)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    outputDir = os.path.join(dirPath, Globals.outputDirName, )
    zipName = datetime.datetime.now().strftime(Globals.archiveTemplate)
    zipPath = os.path.join(dirPath, zipName)
    zipFile = zipfile.ZipFile(zipPath, 'w')
    for root, subdirs, files in os.walk(outputDir): 
        for filename in files:
            zipFile.write(os.path.join(root, filename), arcname = filename)
    zipFile.close()
    zippathFile = open(os.path.join(dirPath, Globals.zipPathFilename), 'w+')
    zippathFile.write(zipPath);
    zippathFile.close();
