import string
import Utilities
import re

class CodeChanger:
    def visit(self, line):
        pass

class LineLengthChanger(CodeChanger):
    def visit(self, line):
        resultLine = ''
        length = len(line.rstrip())
        if(length > 80):
            indentSize = Utilities.getIndentSize(line)
            template = re.compile(",|\(")
            rezults = template.finditer(line)
            for rezult in rezults:
                index = rezult.start()
                if(length - index < 80):
                   if not(Utilities.isInsideTextLiteral(line, index)):
                       resultLine += line[:index + 1]
                       resultLine += "\n" + (" " * (indentSize + 4))
                       resultLine += line[index + 1:]
                       break
        else:
            resultLine = line
        return resultLine
    

class TabsChanger(CodeChanger):
    def visit(self, line):
        resultLine = ''
        for i in range(0, len(line)):
            if line[i] in string.whitespace:
                if line[i] == '\t':
                    resultLine += (' ' * 4)
                else:
                    resultLine += line[i]
            else:
                resultLine += line[i:]
                break
        return resultLine
            

class BracersChanger(CodeChanger):
    def visit(self, line):
        resultLine = ''
        lastIndex = 0
        template = re.compile("{|}")
        rezults = template.finditer(line)
        indentSize = Utilities.getIndentSize(line)
        firstChar = Utilities.findNextNonWhiteSpaceCharIndex(line, 0)
        for rezult in rezults:
            index = rezult.start()
            if not(Utilities.isInsideTextLiteral(line, index) or index == firstChar):
                resultLine += line[lastIndex:index]
                resultLine += '\n'
                if(line[index] == '{'):
                    resultLine += ' ' * indentSize
                    indentSize += 4 
                else:
                    indentSize -= 4           
                    resultLine += ' ' * indentSize
                resultLine += line[index]
                resultLine += '\n'
                lastIndex = Utilities.findNextNonWhiteSpaceCharIndex(line, index + 1 )
                if(lastIndex != -1):
                    resultLine += ' ' * indentSize
        if(lastIndex != -1):
            resultLine += line[lastIndex:]
        return resultLine
    
class OperatorsIndentsChanger(CodeChanger):
    def visit(self, line):
        opTemplate = re.compile("([^\s\+-\/*=\|&])(\+=|-=|\+|-|\*|\/|==|<=|>=|!=|\|\||&&|\||&|=)([^\s\+-\/*=\|&])")
        sepTemplate = re.compile("(\S)(,)(\S)")
        rezultLine = re.sub(opTemplate, "\g<1> \g<2> \g<3>", line)
        rezultLine = re.sub(opTemplate, "\g<1> \g<2> \g<3>", rezultLine)
        rezultLine = re.sub(sepTemplate, "\g<1>\g<2> \g<3>", rezultLine)
        return rezultLine

class MultilineCommentsChanger(CodeChanger): 
    def __init__(self):
        self.isCommentStarted = False
    
    def visit(self, line):
        resultLine = ''
        indentIndex = Utilities.findNextNonWhiteSpaceCharIndex(line, 0)
        if(self.isCommentStarted == True):
            commentEndIndex = line.find("*/")
            resultLine += line[:indentIndex]
            resultLine += "//"
            if(commentEndIndex != -1):
                resultLine += line[indentIndex:commentEndIndex]
                resultLine += line[commentEndIndex + 2:]
                self.isCommentStarted = False
            else:
                resultLine += line[indentIndex:]
        else:
            commentStartIndex = line.rfind("/*")
            commentEndIndex = line.rfind("*/")
            if(commentStartIndex != -1 and commentEndIndex < commentStartIndex):
                resultLine += line[:indentIndex]
                resultLine += line[indentIndex:commentStartIndex]
                resultLine += "//"
                resultLine += line[commentStartIndex + 2:]
                self.isCommentStarted = True
            else:
                resultLine = line
        return resultLine

class SinglelineConditionsChanger(CodeChanger):
    def visit(self, line):
        resultLine = ''
        shortTeplate = re.compile("(.*if\(.*\S+.*\))(.*\S+.*)")
        shortRez = re.match(shortTeplate, line)
        if(shortRez):
            indentSize = Utilities.getIndentSize(line)
            longTemplate = re.compile("(.*if\(.*\S+.*\))(.*\S+.*)(else)(.*\S.*)")
            longRez = re.match(longTemplate, line)
            if(longRez):
                resultLine += longRez.group(1) + '\n'
                resultLine += ' ' * (indentSize + 4)
                resultLine += longRez.group(2).strip() + '\n'
                resultLine += ' ' * indentSize
                resultLine += longRez.group(3).strip() + '\n'
                resultLine += ' ' * (indentSize + 4)
                resultLine += longRez.group(4).strip() + '\n'
            else:
                resultLine += shortRez.group(1) + '\n'
                resultLine += ' ' * (indentSize + 4)
                resultLine += shortRez.group(2).strip() + '\n' 
        else:
            resultLine = line
        return resultLine

class SinglelineOperatorsChanger(CodeChanger):
    def visit(self, line):
        resultLine = ''
        lastIndex = 0
        template = re.compile(";")
        rezults = template.finditer(line)
        indentSize = Utilities.getIndentSize(line)
        for rezult in rezults:
            index = rezult.start()
            if not (Utilities.isInsideTextLiteral(line, index)):
                resultLine += ' ' * indentSize
                resultLine += (line[lastIndex:index + 1].lstrip())
                lastIndex = Utilities.findNextNonWhiteSpaceCharIndex(line, index + 1)
                if(lastIndex != -1):
                    resultLine += '\n'
        if(lastIndex != -1):
            resultLine += line[lastIndex:]
        return resultLine
