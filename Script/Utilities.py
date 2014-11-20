import string
import re

def isInsideTextLiteral(line, index):
    result = False
    startIndex = 0
    rez = 0
    while(True):
        rez = line.find('"', startIndex, index)
        if(rez == -1):
            break
        if(rez == 0 or line[rez - 1] != '\\'):
            rezult = not rezult
        startIndex = rez

def getIndentSize(line):
    for i in range(0, len(line) - 1):
        if line[i] not in string.whitespace:
            return i
    return -1
        
def findNextNonWhiteSpaceCharIndex(line, startIndex):
    template = re.compile("\S")
    rezults = template.finditer(line[startIndex:])

    for rezult in rezults:
        return startIndex + rezult.start()
    return -1
