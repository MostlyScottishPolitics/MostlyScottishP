__author__ = 'pierre'

# Scrapper for the parliament reports
# Ad-hoc implementation
# @input : the html file, locally saved
# @output : a xml file
# @assume : the input file is "correctly" formed

# For xml
import xml.etree.cElementTree as ET
# For regular expressions
import re
# For unicode
import codecs
# For date
import datetime
# For cli arguments
import sys

# Law class, contains the data for a law
import law

# Check the user-supplied arguments
if len(sys.argv) != 2:
    print "usage : scraper <filename>"
    sys.exit(1)

# Create the xml base structure
root = ET.Element("root")

# Variables declaration
worthReading = False
readForMSP = False
readAgainstMSP = False
readAbstentionMSP = False
recordData = False
agreed = False
report_date = "01 January 2000"
newLaw = law.Law()


# Process the line with the type, id, name, proposer, topic
def process_id_line(line1):
    name_read = False
    # Remove the html
    line1 = trim_html(line1)
    split_array = line1.split(",")
    for element in split_array:
        # Split the piece of sentence into words
        words = element.split(" ")
        # Piece of sentence with the type and id
        if "that" in element:
            # Second word is type
            newLaw.law_type = words[2]
            # Third word is id
            newLaw.law_id = words[3]
        # Piece of sentence with surname and name
        elif "in the name of" in element:
            # If the law is an amendment, we only need the first surname/name
            # The second ones are those for the original bill, which we don't need here
            if not name_read:
                # Fifth word is surname, sixth name
                newLaw.law_presenter_surname = words[5]
                newLaw.law_presenter_name = words[6]
                name_read = True
        # Piece of sentence with topic
        elif "on" in element:
            # The whole piece, minus on
            newLaw.law_topic = element.replace(" on ", "")


# Process the lines which contains lists of msps
def process_msps_line(line2, node):
    line2 = trim_html(line2)
    if "for" in node:
        newLaw.law_for.append(line2.replace(",", "", 1))
    elif "against" in node:
        newLaw.law_against.append(line2.replace(",", "", 1))
    elif "abstention" in node:
        newLaw.law_abstention.append(line2.replace(",", "", 1))


# Return a string without spaces or html tags
# Does not work with every html tag, but should do the trick here
# Remove everything with an & after that
def trim_html (string):
    return re.sub('<[^<]+?>', "", string).split("&", 1)[0].strip(' \t\n\r')




# Read the file into an array
with codecs.open(sys.argv[1], 'r', 'utf-8') as file:
    content = file.readlines()

# Process the file
for line in content:
    # Out of the interesting section
    if not worthReading:
        # Get the date of the report
        if ">Meeting of the Parliament" in line:
            report_date = trim_html(line).replace("Meeting of the Parliament ", "")
        # First interesting line
        if "#ScotParlOR Decision Time" in line:
            worthReading = True
    else:
        # End of interesting section
        if 'div class="Debate"' in line:
            worthReading = False
        elif 'Meeting&nbsp;closed' in line:
            worthReading = False
        else:
            # Line with the type, id, name, proposer, topic
            if "question is, that " in line:
                # Write previous law if there is one
                # If it is the first, recordData is false, so no write
                # Write xml nodes only if data is of interest
                if recordData:
                    newLaw.data_to_xml_node(root)
                    # Set it back to false
                    recordData = False
                process_id_line(line)
                # Add the date
                # Got it at the beginning of the document
                newLaw.law_date = report_date
            # Line before the list of MSPs for the law
            elif ">For<" in line:
                readForMSP = True
                # There is a vote, data is of interest
                recordData = True
            # The lines after >For<
            elif readForMSP:
                process_msps_line(line, "for")
                # Last line of the for list
                if "</span>" in line:
                    readForMSP = False
            # Line before the list of MSPs against the law
            elif ">Against<" in line:
                readAgainstMSP = True
            # The lines after >Against<
            elif readAgainstMSP:
                process_msps_line(line, "against")
                # Last line of the for list
                if "</span>" in line:
                    readAgainstMSP = False
            # Line before the list of MSPs abstaining
            elif ">Abstentions<" in line:
                readAbstentionMSP = True
            # The lines after >Against<
            elif readAbstentionMSP:
                process_msps_line(line, "abstention")
                # Last line of the for list
                if "</span>" in line:
                    readAbstentionMSP = False
            # Result of the vote
            # Since we have the full details of the vote, we could calculate it
            # Simpler to get the text after that though
            elif "agreed to" in line and ("amended" in line or "Motion" in line or "Amendment in file"):
                split_array = trim_html(line).split(" ")
                newLaw.law_agreed = split_array[len(split_array) - 2]
                if not "disagreed" in line and ("amended" in line or "Motion" in line):
                    agreed = True
            # Text voted
            # Value of the text is the next line
            elif agreed:
                newLaw.law_text = trim_html(line)
                agreed = False


# Write xml nodes only if data is of interest
# Flush last value
if recordData:
    newLaw.data_to_xml_node(root)


# Prettify the xml output
# http://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
# From user ade
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

indent(root)
tree = ET.ElementTree(root)
report_date = datetime.datetime.strptime(report_date, '%d %B %Y').strftime('%d_%m_%Y')
file_name = "data_" + report_date + ".xml"
tree.write(file_name, "utf-8")