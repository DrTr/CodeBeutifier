from Visitors import *
import os

visitorsDict = { 
                 1: TabsChanger,
                 2: BracersChanger,
                 4: OperatorsIndentsChanger,
                 8: MultilineCommentsChanger,
                 16: SinglelineConditionsChanger,
                 32: SinglelineOperatorsChanger,               
                 64: LineLengthChanger,
                 }

outputDirName = "output"
inputDirName = "input"
archiveTemplate = "CB_%y_%m_%d__%H_%M_%S.zip"
zipPathFilename = "zipPath.cfg"

def getFileVisitors(options):
    visitors = []

    for key in sorted(visitorsDict):
        if options & key != 0:
            visitors.append(visitorsDict[key]())
    return visitors
    
def changeFile(filename, rootDir, options):
    inputFile = open(filename, 'r')
    basename = os.path.basename(filename)
    outputFile = open(os.path.join(rootDir, outputDirName, basename), 'w+')
    visitors = getFileVisitors(options)
    for line in inputFile:
        linesToCheck = []
        linesToCheck.append(line)
        for visitor in visitors:
            tmpList = []
            for line in linesToCheck:
                if line == '':
                    lines = ['']
                else:
                    changedLine = visitor.visit(line)
                    if(changedLine != '\n'):
                        lines = changedLine.split("\n")
                        if lines[-1] == '':
                            del lines[-1]
                    else:
                        lines = ['']
                tmpList = tmpList + lines
            linesToCheck = tmpList
        for line in linesToCheck:
            outputFile.write(line + '\n')
    inputFile.close()
    outputFile.close()
    
