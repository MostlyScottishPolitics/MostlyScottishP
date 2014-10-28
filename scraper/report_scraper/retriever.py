__author__ = 'pierre'

# Retrieve the data from parliamentary reports
# The concept is simple : find a (new) report, extract the html and give it to the scraper
# The harder part is finding correct URLs for reports
#
# URLs all begin by http://www.scottish.parliament.uk/parliamentarybusiness/28862.aspx
# Report then have an id number added after that
# like http://www.scottish.parliament.uk/parliamentarybusiness/28862.aspx?r=9566
#
# @input : none
# @output : an xml data file for each report found
# @ assume : URL scheme on the website will stay the same

# To get the HTML
import urllib2
# The scraper
import scraper
# For regular expressions
import re
# To store/load the dictionary as json
import json

# File where processed URLs are stored
f_processed_urls = "processed_urls.txt"
# Base URL
base_url = "http://www.scottish.parliament.uk/parliamentarybusiness/28862.aspx"


# Import the URLs already processed in the json file
def import_processed_urls(url_file):
    try:
        with open(url_file, "r") as f:
            try:
                json_data = json.load(f)
            except ValueError, e:
                dict_url = dict()
                scraper.log("Can't load json.")
                return dict_url
            else:
                return json_data
    except IOError, e:
        scraper.log("Can't open file.")
        dict_url = dict()
        return dict_url


# Store the dictionary of processed URLs as json
def export_processed_urls(url_file, dict_url):
    with open(url_file, "w+") as f:
        try:
            json.dump(dict_url, f)
        except ValueError, e:
            scraper.log("Can't dump json.")
            return -1
        else:
            return 0


# Get the latest report id
def get_latest_id():
    url = "http://www.scottish.parliament.uk/parliamentarybusiness/official-report.aspx"
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    for line in response:
        if base_url in line:
            # Keep only the url
            id_report = re.match(r'^.*"(.*)".*$', line).group(1)
            # Remove the base url to get only the id
            id_report = id_report.strip("http://www.scottish.parliament.uk/parliamentarybusiness/28862.aspx?r=")
            # Remove everything after #
            # There's some data like that sometimes
            id_report, sep, tail = id_report.partition('#')
            return id_report
    scraper.log("Latest report id not found.")
    return 0


# Download the html files
def get_html_files():
    write = False
    report_date = "2000_01_01"
    dict_files = dict()
    # Load the already processed URLs
    processed_urls = import_processed_urls(f_processed_urls)
    for i in range(5000, int(get_latest_id()) + 1):
        if str(i) not in processed_urls:
            url = base_url + "?r=" + str(i)
            # Test the page
            try:
                response = urllib2.urlopen(url)
                page = response.read()
            except urllib2.HTTPError, e:
                # Add it the list of already processed url
                processed_urls[i] = base_url + "?r=" + str(i)
                scraper.log(str(i) + " is not a valid URL.")
                continue
            else:
                # Check if it's a parliamentary report, ie what we want
                # Get the date too
                for line in page.split("\n"):
                    if ">Meeting of the Parliament" in line:
                        report_date = scraper.trim_html(line).replace("Meeting of the Parliament ", "")
                        report_date = scraper.datetime.datetime.strptime(report_date, '%d %B %Y').strftime('%Y_%m_%d')
                        write = True
                processed_urls[i] = base_url + "?r=" + str(i)
                # If not a parliamentary report
                if not write:
                    scraper.log(str(i) + " is not a parliamentary report. No data written.")
                    continue
                else:
                    scraper.log(str(i) + " is a parliamentary report.")
                    # Write the file
                    file_output = "html_" + report_date + ".html"
                    dict_files[i] = file_output
                    with open(file_output, "w+") as f:
                        f.write(page)
                        write = False
        else:
            scraper.log(str(i) + " already scrapped.")
    # Store the new URLs
    export_processed_urls(f_processed_urls, processed_urls)
    return dict_files


# Apply the scraper to each created files
def scrap_files(dict_files):
    for id_file, file in dict_files.iteritems():
        if "no data written" not in scraper.process_html(file, id_file):
            scraper.log("file " + file + " with id " + str(id_file) + " created.")
        else:
            scraper.log("Failed to create file " + file + " with id " + str(id_file) + ".")


scrap_files(get_html_files())