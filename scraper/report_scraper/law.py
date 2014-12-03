__author__ = 'pierre'

import xml.etree.cElementTree as ET
import re
import time


# For log messages
def log(message):
    with open("scraper.log", "a+") as log_file:
        date = time.strftime("%Y-%m-%d %H:%M:%S : ")
        message = date + message + '\n'
        log_file.write(message)

class Law(object):
    law_type = ""
    law_id = ""
    law_date = ""
    law_presenter_name = ""
    law_presenter_surname = ""
    law_presenter_party = ""
    law_presenter_constituency = ""
    law_topic = ""
    law_category = ""
    law_text = ""
    law_agreed = False
    law_for = []
    law_against = []
    law_abstention = []

    # The class "constructor" - It's actually an initializer
    def __init__(self):
        self.law_type = ""
        self.law_id = ""
        self.law_presenter_name = ""
        self.law_presenter_surname = ""
        self.law_topic = ""
        self.law_category = ""
        self.law_text = ""
        self.law_agreed = ""
        self.law_for = []
        self.law_against = []
        self.law_abstention = []

    def add_to_msp_node(self, msp_node, msps):
        # Split for space, but not when they are between parentheses
        split_array = re.split(r"\s+(?=[^()]*(?:\(|$))", msps)
        try:
            surname_node = ET.SubElement(msp_node, "surname")
            surname_node.text = split_array[0]
        except Exception:
            # log("Can't add surname to node.")
            return
        try:
            name_node = ET.SubElement(msp_node, "name")
            name_node.text = split_array[1]
        except Exception:
            #log("Can't add name to node.")
            return
        try:
            party_node = ET.SubElement(msp_node, "party")
            party_node.text = split_array[3].replace("(", "").replace(")", "")
        except Exception:
            #log("Can't add party to node.")
            return
        try:
            constituency_node = ET.SubElement(msp_node, "constituency")
            constituency_node.text = split_array[2].replace("(", "").replace(")", "")
        except Exception:
            #log("Can't add constituency to node.")
            return

    # Check if there is enough data in the law to make it worthwhile
    def is_correct(self):
        if (self.law_type == ""
                or self.law_id == ""
                or self.law_agreed == ""
                or self.law_presenter_name == ""
                or self.law_presenter_surname == ""):
            return False
        else:
            return True

    def data_to_xml_node(self, parent_node):
        law_node = ET.SubElement(parent_node, "law")

        type_node = ET.SubElement(law_node, "type")
        type_node.text = self.law_type

        id_node = ET.SubElement(law_node, "id")
        id_node.text = self.law_id

        date_node = ET.SubElement(law_node, "date")
        date_node.text = self.law_date

        surname_node = ET.SubElement(law_node, "surname")
        surname_node.text = self.law_presenter_surname

        name_node = ET.SubElement(law_node, "name")
        name_node.text = self.law_presenter_name

        topic_node = ET.SubElement(law_node, "topic")
        topic_node.text = self.law_topic

        if self.law_category:
            category_node = ET.SubElement(law_node, "category")
            category_node.text = self.law_category

        if self.law_text:
            text_node = ET.SubElement(law_node, "text")
            text_node.text = self.law_text

        agreed_node = ET.SubElement(law_node, "agreed")
        agreed_node.text = self.law_agreed

        for_node = ET.SubElement(law_node, "for")
        for msps in self.law_for:
            msp_node = ET.SubElement(for_node, "msp")
            self.add_to_msp_node(msp_node, msps)

        against_node = ET.SubElement(law_node, "against")
        for msps in self.law_against:
            msp_node = ET.SubElement(against_node, "msp")
            self.add_to_msp_node(msp_node, msps)

        if self.law_abstention:
            abstention_node = ET.SubElement(law_node, "abstention")
            for msps in self.law_abstention:
                msp_node = ET.SubElement(abstention_node, "msp")
                self.add_to_msp_node(msp_node, msps)

        # Reinitialise data after creating the node for next data
        self.law_type = ""
        self.law_id = ""
        self.law_date = ""
        self.law_presenter_name = ""
        self.law_presenter_surname = ""
        self.law_topic = ""
        self.law_category = ""
        self.law_text = ""
        self.law_agreed = ""
        self.law_for = []
        self.law_against = []
        self.law_abstention = []