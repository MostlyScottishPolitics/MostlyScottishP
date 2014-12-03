__author__ = 'pierre'

# Scrapper for the parliament reports
# Ad-hoc implementation
# @input : the html file
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
import time

# Law class, contains the data for a law
import law
# To extract the topic from the text of the law
import topic_extracter


# For log messages
def log(message):
    with open("scraper.log", "a+") as log_file:
        date = time.strftime("%Y-%m-%d %H:%M:%S : ")
        message = date + message + '\n'
        log_file.write(message)


# Process the line with the type, id, name, proposer, topic
def process_id_line(line1, current_law):
    name_read = False
    # Remove the html
    line1 = trim_html(line1)
    # Split the sentence with commas
    split_array = line1.split(",")
    for element in split_array:
        # Split the piece of sentence into words
        words = element.split(" ")
        # Piece of sentence with the type and id
        if "that" in element:
            # Second word is type
            try:
                # Malformed data with no type
                # Assumed amendment
                if "S4" in words[2]:
                    current_law.law_type = "amendment"
                else:
                    current_law.law_type = words[2]
            except Exception:
                log("Can't get the type.")
            # Third word is id
            try:
                # Malformed data with no type
                if "S4" in words[2]:
                    current_law.law_id = words[2]
                else:
                    current_law.law_id = words[3]
            except Exception:
                log("Can't get the id.")
        # Piece of sentence with surname and name
        elif "in the name of" in element and "in" in words[1]:
            # If the law is an amendment, we only need the first surname/name
            # The second ones are those for the original bill, which we don't need here
            if not name_read:
                # Fifth word is surname, sixth name
                try:
                    if "Dr" in words[5]:
                        current_law.law_presenter_surname = words[6]
                    else:
                        current_law.law_presenter_surname = words[5]
                except Exception:
                    log("Can't get the surname.")
                try:
                    if "Dr" in words[5]:
                        current_law.law_presenter_name = words[7]
                    else:
                        current_law.law_presenter_name = words[6]
                except Exception:
                    log("Can't get the name.")
                name_read = True
        # Piece of sentence with topic
        elif "on" in element:
            # The whole piece, minus " on "
            current_law.law_topic = element[4:]


# Process the lines which contains lists of msps
def process_msps_line(line, node, current_law):
    line = trim_html(line)
    # Remove title of msps
    line = line.replace("Dr ", "")
    if "for" in node:
        current_law.law_for.append(line.replace(",", "", 1))
    elif "against" in node:
        current_law.law_against.append(line.replace(",", "", 1))
    elif "abstention" in node:
        current_law.law_abstention.append(line.replace(",", "", 1))


# Process the lines which contains lists of msps
# Version for the old format
def process_old_msp(line, current_law):
    # Remove the debut of the string, depends on for/against/...
    # Could be cleaner
    line = line.strip("<div class='content'>There will be a division.<br /><br />")
    # Remove title of msps
    line = line.replace("Dr ", "")
    split = line.split("<br />")
    level = 0
    for element in split:
        if "For" in element:
            level = 1
        if "Against" in element:
            level = 2
        if "Abstention" in element:
            level = 3
        # For
        if level == 1:
            # Element with a msp
            if "(" in element:
                current_law.law_for.append(element.replace(",", "", 1))
        # Against
        if level == 2:
            # Element with a msp
            if "(" in element:
                current_law.law_against.append(element.replace(",", "", 1))
        # Abstention
        if level == 3:
            # Element with a msp
            if "(" in element:
                current_law.law_abstention.append(element.replace(",", "", 1))


# Return a string without spaces or html tags
# Does not work with every html tag, but should do the trick here
# Remove everything with an & after that
def trim_html(string):
    return re.sub('<[^<]+?>', "", string).split("&", 1)[0].strip(' \t\n\r')


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


def process_html(filename, id_file):

    # Variables declaration
    worth_reading = False
    read_for_msp = False
    read_against_msp = False
    read_abstention_msp = False
    record_data = False
    agreed = False
    write = False
    report_date = "01 January 2000"
    old_format = False
    # Create a new law instance
    current_law = law.Law()
    # Create the xml base structure
    root = ET.Element("root")

    # Read the file into an array
    with codecs.open(filename, 'r', 'utf-8') as file_input:
        content = file_input.readlines()

    # Process the file
    for line in content:
        # Out of the interesting section
        if not worth_reading:
            # Get the date of the report
            if ">Meeting of the Parliament" in line:
                report_date = trim_html(line).replace("Meeting of the Parliament ", "")
            # First interesting line
            if "#ScotParlOR Decision Time" in line:
                worth_reading = True
        else:
            # End of interesting section
            if 'div class="Debate"' in line and "result of the division" not in line:
                worth_reading = False
            elif 'Meeting&nbsp;closed' in line:
                worth_reading = False
            else:
                # Line with the type, id, name, proposer, topic
                if "question is, that " in line:
                    # Write previous law if there is one
                    # If it is the first, record_data is false, so no write
                    # Write xml nodes only if data is of interest
                    if record_data:
                        current_law.data_to_xml_node(root)
                        # We have something to write
                        write = True
                        # Set it back to false
                        record_data = False
                    process_id_line(line, current_law)
                    # Add the date
                    # Got it at the beginning of the document
                    current_law.law_date = report_date

                # Line before the list of MSPs for the law
                # For the old version of reports (id < 9522)
                # Contains for, against and abstention in the same line, thus only need to be detected once
                elif ">For<br />" in line:
                    # There is a vote, data is of interest
                    record_data = True
                    process_old_msp(line, current_law)
                    old_format = True

                # Line before the list of MSPs for the law
                # For the new version of reports (id > 9521)
                elif ">For</span>" in line:
                    read_for_msp = True
                    # There is a vote, data is of interest
                    record_data = True
                # The lines after >For<
                elif read_for_msp:
                    process_msps_line(line, "for", current_law)
                    # Last line of the for list
                    if "</span>" in line:
                        read_for_msp = False
                # Line before the list of MSPs against the law
                elif ">Against<" in line:
                    read_against_msp = True
                # The lines after >Against<
                elif read_against_msp:
                    process_msps_line(line, "against", current_law)
                    # Last line of the for list
                    if "</span>" in line:
                        read_against_msp = False
                # Line before the list of MSPs abstaining
                elif ">Abstentions<" in line:
                    read_abstention_msp = True
                # The lines after >Against<
                elif read_abstention_msp:
                    process_msps_line(line, "abstention", current_law)
                    # Last line of the for list
                    if "</span>" in line:
                        read_abstention_msp = False

                # Result of the vote
                # Since we have the full details of the vote, we could calculate it
                # Simpler to get the text after that though
                # For new format
                elif "agreed to" in line and ("amended" in line or "Motion" in line or "Amendment" in line) and not old_format:
                    split_array = trim_html(line).split(" ")
                    try:
                        current_law.law_agreed = split_array[len(split_array) - 2]
                    except Exception:
                        log("Can't get the agreement on the law.")
                    if "disagreed" not in line and ("amended" in line or "Motion" in line or "Amendment" in line):
                        agreed = True
                # Text voted
                # Value of the text is the next line
                elif agreed:
                    # If there is actually a text
                    if "The Presiding Officer:" not in line:
                        current_law.law_text = trim_html(line)
                        # Topic category
                        current_law.law_category = topic_extracter.get_topic_from_text(trim_html(line))
                    agreed = False

                # Result of the vote
                # For old format
                elif "The result of the division is" in line and old_format:
                    # Find agreement or not
                    if "disagreed" in line:
                        current_law.law_agreed = "disagreed"
                    else:
                        current_law.law_agreed = "agreed"
                    # Find the text if there is one
                    split = line.split("<br /><br />")
                    # It is the element after the agreed text
                    # If there is no text, it's a </div>
                    i = 0
                    for element in split:
                        try:
                            if "agreed" in element and "</div>" not in split[i + 1]:
                                current_law.law_text = split[i + 1]
                                # Topic category
                                current_law.law_category = topic_extracter.get_topic_from_text(split[i + 1])
                            i += 1
                        except Exception:
                            log("Can't get the text of the law.")


    # Write xml nodes only if data is of interest
    # Flush last value
    if record_data:
        if current_law.is_correct():
            current_law.data_to_xml_node(root)
        else:
            log("Invalid data in law. No data written.")

    if not write:
        log("No file created because there is no vote data in scraped file " + str(id_file) + ", no data written.")
        return "no data written"
    else:
        indent(root)
        tree = ET.ElementTree(root)
        report_date = datetime.datetime.strptime(report_date, '%d %B %Y').strftime('%Y_%m_%d')
        file_name = "data_" + report_date + ".xml"
        try:
            tree.write(file_name, "utf-8")
        except IOError, e:
            log("Error when writing XML file" + str(id_file) + ".")
        else:
            log("XML file created " + str(id_file) + ", data written.")
        # Return date of document if success
        return report_date