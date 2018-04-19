import codecs
import click
import os
import sys

OUTPUT_FOLDER = 'output'


class Segmentor:
    def __init__(self, inputFile, verbose):
        self.inputFileName = inputFile
        self.outfolder = os.path.join(os.path.dirname(self.inputFileName),
                                      OUTPUT_FOLDER)
        self.verbose = verbose
        self.__reset__()

    def __reset__(self):
        self.outputFilename = ''
        self.lines = []

    def convert(self):
        if self.verbose:
            click.echo('Info: Reading file {0}.'.format(self.inputFileName))
        with codecs.open(self.inputFileName, 'r', 'utf-8') as openedFile:
            for (i, line) in enumerate(openedFile):
                self.__parse(i, line.strip())

    def write2file(self):
        if not os.path.exists(self.outfolder):
            click.echo(
                'Info: Creating output folder {0}.'.format(self.outfolder))
            os.makedirs(self.outfolder)
        outfile_name = os.path.join(self.outfolder,
                                    self.outputFilename + ".atf")
        if self.verbose:
            click.echo('Info: Writing to file {0}.'.format(outfile_name))
        with codecs.open(outfile_name, 'w+', 'utf-8') as outputFile:
            outputFile.writelines('\n'.join(self.lines))

    def __parse(self, linenumber, line):
        tokenizedLine = line.split(" ")
        if len(line) == 0:
            pass
        elif line[0] == "&":
            if len(self.lines) > 0:
                self.write2file()
            self.__reset__()
            firstword = tokenizedLine[0].lstrip("&")
            self.outputFilename = firstword
        self.lines.append(line)


if __name__ == '__main__':
    try:
        segmentor = Segmentor(inputFile=sys.argv[1],
                              verbose=(sys.argv[2] == "True"))
        segmentor.convert()
    except IndexError:
        print("Input both atffile file source and verbose flag like "
              "'python segment.py cdli_atf_20180104.atf True")
