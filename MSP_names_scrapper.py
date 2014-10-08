# Scrapper for the MSP name, surname, party and locality
# Should be one time use only, code reflect that
# @input : the html file, locally saved
# @ouput : a csv file with teh following format
#           name, surname, party, locality *new line*
# @assume : the file is "correctly" formed

# For regexp
import re

csv_file = open('msps.csv', 'w')
line_counter = -1

# Read the file into an array
with open('msp_name.txt', 'r') as file:
    content = file.readlines()

# Return a string without spaces or html tags
# Does not work with every html tag, but should do the trick here
# Remove everything with an & after that
def trim_html (string):
    return re.sub('<[^<]+?>', "", string).split("&", 1)[0].strip(' \t\n\r')

# Process the file
# Find the start of the name section
# Then, find the line containing msps/currentmsps
# The name and surname will be one line after that
# The party 5 and the locality 8
for line in content:
    if 'msps/currentmsps' in line:
        line_counter = 8
    # Name and surname line or party line
    if (line_counter == 7 or line_counter == 3):
        line_trimmed = trim_html(line)
        csv_file.write(line_trimmed)
        csv_file.write(", ")
    # Locality line
    if line_counter == 0:
        line_trimmed = trim_html(line)
        csv_file.write(line_trimmed)
        csv_file.write(", \n")
    line_counter -= 1

csv_file.close()
