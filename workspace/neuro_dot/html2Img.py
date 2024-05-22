import imgkit
import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description='Generate Manual Assessor XML file for notebooks')
parser.add_argument('htmlinputFile', help='Scan id')
parser.add_argument('outputFile', help='Session id')
args=parser.parse_args()

htmlinputFile = args.htmlinputFile
outputFile = args.outputFile

options ={
    'zoom':1.0, 
    'quality': 100,
    'format': 'jpg',
    'encoding': "UTF-8"}
imgkit.from_file(htmlinputFile, outputFile, options=options)

os.remove(htmlinputFile)