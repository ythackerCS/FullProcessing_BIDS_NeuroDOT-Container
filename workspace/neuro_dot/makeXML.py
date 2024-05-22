from lxml.builder import ElementMaker
from lxml.etree import tostring as xmltostring
import datetime as dt
import os
import sys
import json
import random
import string
import argparse
# import requests
# import docopt
# import requests.packages.urllib3
# requests.packages.urllib3.disable_warnings()

# version = "1.0"
# args = docopt(__doc__, version=version)

# xnat_host = args.get('XNAT_HOST', 'http://xnat.org')
# sessionId = args['SESSION_ID']
# sessionLabel = args['SESSION_LABEL']
# scanId = args['SCAN_ID']
# maskFileUri = args['MASK_FILE_URI']
# project = args['PROJECT']
# # csvin = args['CSV_IN']
# xmlout = args['XML_OUT']

parser = argparse.ArgumentParser(description='Generate Manual Assessor XML file for notebooks')
parser.add_argument('scanId', help='Scan id')
parser.add_argument('sessionId', help='Session id')
parser.add_argument('sessionLabel', help='Session label')
parser.add_argument('project', help='Project')
parser.add_argument('xnat_user', help='XNAT Username')
args=parser.parse_args()


sessionId = args.sessionId
sessionLabel = args.sessionLabel
project = args.project
scanId = args.scanId
user=args.xnat_user.strip('\"')
pipeline = "Full-Processing"
outpath="/outputfiles/assessor.xml"
params = ""

# with open("/input/params.txt", "r") as f:
#     params = f.read()



now = dt.datetime.today()
isodate = now.strftime('%Y-%m-%d')
timestampforlabel = now.strftime('%Y%m%d%H%M%S')
timestamp = dt.datetime.now().isoformat()
assessorId = '{}_{}_{}_{}'.format(sessionLabel,scanId, pipeline,timestampforlabel)
assessorLabel = '{}_{}_{}_{}'.format(sessionLabel,scanId, pipeline,timestampforlabel)


nsdict = {'xnat':'http://nrg.wustl.edu/xnat',
          'xsi':'http://www.w3.org/2001/XMLSchema-instance',
          'fnirs': 'http://nrg.wustl.edu/fnirs'}
def ns(namespace, tag):
    return "{%s}%s" % (nsdict[namespace], tag)

def schemaLoc(namespace):
    return "{0} https://www.xnat.org/schemas/{1}/{1}.xsd".format(nsdict[namespace], namespace)

def randstring(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))



#######################################################
# BUILD ASSESSOR XML
# Building XML using lxml ElementMaker.
# For documentation, see http://lxml.de/tutorial.html#the-e-factory

print("Constructing assessor XML.")
E = ElementMaker(namespace=nsdict['fnirs'], nsmap=nsdict)
Exnat = ElementMaker(namespace=nsdict['xnat'], nsmap=nsdict)

assessorTitleAttributesDict = {
    'ID': assessorId,
    'project': project,
    'label': assessorLabel,
    ns('xsi','schemaLocation'): schemaLoc('fnirs')
}

assessorElementsList = [
    Exnat("date", isodate),
    Exnat("imageSession_ID", sessionId),
    E("pipelineRun", pipeline),
    E("pipelineRunDateTime", timestamp),
    E("userThatRan", user),
    E("scanUsed", scanId),
]

# assessorElementsList.extend([
#     E("comments", random.choice(["Looks good", "All good", "Good", "Bad", "None", "NA"])),
#     E("pass", random.choice(["1", "0", "Yes", "No"])),
#     E("payable", random.choice(["1", "0", "Yes", "No"])),
#     E("rescan", random.choice(["1", "0", "Yes", "No"]))
# ])

assessorXML = E('fnirsPipelineAssessorData', assessorTitleAttributesDict, *assessorElementsList)

print('Writing assessor XML to {}'.format(outpath))
# print(xmltostring(assessorXML, pretty_print=True))
with open(outpath, 'wb') as f:
    f.write(xmltostring(assessorXML, pretty_print=True, encoding='UTF-8', xml_declaration=True))

# length = 20
# print("Generating nonsense files in subdirectories of {}.".format(outdir))
# os.makedirs(os.path.join(outdir, 'dir0', 'dir1', 'dir2'))
# with open(os.path.join(outdir, 'dir0', 'file1.txt'), 'w') as f:
#     f.write(randstring(length)+"\n")
# with open(os.path.join(outdir, 'dir0', 'dir1', 'file2.txt'), 'w') as f:
#     f.write(randstring(length)+"\n")
# with open(os.path.join(outdir, 'dir0', 'dir1', 'dir2', 'file3.txt'), 'w') as f:
#     f.write(randstring(length)+"\n")