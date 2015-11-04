#!/usr/bin/python

import sys
import xml.etree.cElementTree as ET
# (cElementTree is way faster than the python-native version)

xmlFile = sys.argv[1]
searchString = sys.argv[2]
path = []

if len(sys.argv) < 3:
    # such good UX wow
    print "Usage: $ python " + sys.argv[0] + " <file.xml> \"Search String\""
    sys.exit()

print "searching for everything that redirects to: " + searchString

# iterparse allows us to throw away tags after we're done parsing them,
# rather than putting a huge (>6gb) file in memory like a plebian
for event, elem in ET.iterparse(xmlFile, events=("start", "end")):

    if event == "start":
        # as we descend down a tag hierarchy, store elements so we can
        # refer back to our parent nodes when we need to
        path.append(elem)

    elif event == "end": # then we parse the tag

        if elem.tag == "abstract":
            if elem.text and "#REDIRECT" in elem.text:

                # get elemet text, remove the in-string flag we used to find it,
                # and strip leading whitespace
                redirectText = elem.text.replace("#REDIRECT","").lstrip()

                if searchString.lower() == redirectText.lower(): 

                    if path[1].find('title').text:
                        # then we're redirecting to the page our search is querying
                        title = path[1].find('title').text.replace("Wikipedia:" ,"").lstrip()
                        print title

        if elem.tag == "doc":
            # we're leaving a doc, so clear it and its children
            elem.clear()

        path.pop() # we're done, so remove it from the path
