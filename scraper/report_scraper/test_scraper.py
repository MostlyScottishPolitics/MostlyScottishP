#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import unittest
import scraper
import topic_extracter


class TestScraper(unittest.TestCase):

    # Malformed line raise exception
    def test_process_id_line_no_line(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a malformed line
        malformed_line = ""
        self.assertRaises(Exception, scraper.process_id_line(malformed_line, n_law))

    # Malformed line raise exception
    def test_process_id_line_malformed_line(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a malformed line
        malformed_line = "that the thing blah blah2 blah3 foo bar"
        self.assertRaises(Exception, scraper.process_id_line(malformed_line, n_law))

    # Correct line put the correct data in the correct node
    # For the new style of input
    def test_process_id_line_correct_line_new_style(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a malformed line
        correct_line = '<p style="text-align:justify;text-indent:10pt;margin-top:0pt;margin-bottom:6pt;"><span class="Contribution">The first question is, that amendment S4M-11763.3, in the name of Margaret Burgess, which seeks to amend motion S4M-11763, in the name of Mary Fee, on private sector rent reform, be agreed to. Are we agreed?</span></p>'
        # Run the function
        scraper.process_id_line(correct_line, n_law)
        self.assertEqual(n_law.law_type, "amendment")
        self.assertEqual(n_law.law_id, "S4M-11763.3")
        self.assertEqual(n_law.law_presenter_surname, "Margaret")
        self.assertEqual(n_law.law_presenter_name, "Burgess")
        self.assertEqual(n_law.law_topic, "private sector rent reform")

    # Correct line put the correct data in the correct node
    # For the doctor style of input
    def test_process_id_line_correct_line_doctor_style(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a malformed line
        correct_line = '<p style="text-align:justify;text-indent:10pt;margin-top:0pt;margin-bottom:6pt;"><span class="Contribution">The first question is, that amendment S4M-11763.3, in the name of Dr Margaret Burgess, which seeks to amend motion S4M-11763, in the name of Mary Fee, on private sector rent reform, be agreed to. Are we agreed?</span></p>'
        # Run the function
        scraper.process_id_line(correct_line, n_law)
        self.assertEqual(n_law.law_type, "amendment")
        self.assertEqual(n_law.law_id, "S4M-11763.3")
        self.assertEqual(n_law.law_presenter_surname, "Margaret")
        self.assertEqual(n_law.law_presenter_name, "Burgess")
        self.assertEqual(n_law.law_topic, "private sector rent reform")

    # Correct line put the correct data in the correct node
    # For the no type style of input
    def test_process_id_line_correct_line_no_type_style(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a malformed line
        correct_line = '<p style="text-align:justify;text-indent:10pt;margin-top:0pt;margin-bottom:6pt;"><span class="Contribution">The first question is, that S4M-11763.3, in the name of Dr Margaret Burgess, which seeks to amend motion S4M-11763, in the name of Mary Fee, on private sector rent reform, be agreed to. Are we agreed?</span></p>'
        # Run the function
        scraper.process_id_line(correct_line, n_law)
        self.assertEqual(n_law.law_type, "amendment")
        self.assertEqual(n_law.law_id, "S4M-11763.3")
        self.assertEqual(n_law.law_presenter_surname, "Margaret")
        self.assertEqual(n_law.law_presenter_name, "Burgess")
        self.assertEqual(n_law.law_topic, "private sector rent reform")

    # Test no data for empty line
    # For node
    def test_process_msps_line_node_for_no_line(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "for"
        # Create a malformed line
        line = ""
        scraper.process_msps_line(line, node, n_law)
        self.assertEqual(n_law.law_for, [""])
        self.assertEqual(n_law.law_against, [])
        self.assertEqual(n_law.law_abstention, [])

    # Test no data for empty line
    # Against node
    def test_process_msps_line_node_against_no_line(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "against"
        # Create a malformed line
        line = ""
        scraper.process_msps_line(line, node, n_law)
        self.assertEqual(n_law.law_for, [])
        self.assertEqual(n_law.law_against, [""])
        self.assertEqual(n_law.law_abstention, [])

    # Test no data for empty line
    # Abstention node
    def test_process_msps_line_node_abstention_no_line(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "abstention"
        # Create a malformed line
        line = ""
        scraper.process_msps_line(line, node, n_law)
        self.assertEqual(n_law.law_for, [])
        self.assertEqual(n_law.law_against, [])
        self.assertEqual(n_law.law_abstention, [""])

    # Test correct data for empty line
    # For node
    def test_process_msps_line_node_for_correct_line(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "for"
        # Create a malformed line
        line = '<p style="margin-top:0pt;margin-bottom:6pt;"><span class="Poem">Adam, George (Paisley) (SNP) <br />'
        scraper.process_msps_line(line, node, n_law)
        self.assertEqual(n_law.law_for, ["Adam George (Paisley) (SNP)"])
        self.assertEqual(n_law.law_against, [])
        self.assertEqual(n_law.law_abstention, [])

    # Test correct data for empty line
    # Against node
    def test_process_msps_line_node_against_correct_line(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "against"
        # Create a malformed line
        line = '<p style="margin-top:0pt;margin-bottom:6pt;"><span class="Poem">Adam, George (Paisley) (SNP) <br />'
        scraper.process_msps_line(line, node, n_law)
        self.assertEqual(n_law.law_for, [])
        self.assertEqual(n_law.law_against, ["Adam George (Paisley) (SNP)"])
        self.assertEqual(n_law.law_abstention, [])

    # Test correct data for empty line
    # Abstention node
    def test_process_msps_line_node_abstention_correct_line(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "abstention"
        # Create a malformed line
        line = '<p style="margin-top:0pt;margin-bottom:6pt;"><span class="Poem">Adam, George (Paisley) (SNP) <br />'
        scraper.process_msps_line(line, node, n_law)
        self.assertEqual(n_law.law_for, [])
        self.assertEqual(n_law.law_against, [])
        self.assertEqual(n_law.law_abstention, ["Adam George (Paisley) (SNP)"])

    # Test correct data for new line
    # For node
    def test_process_msps_line_node_for_two_correct_lines(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "for"
        # Create a malformed line
        line = '<p style="margin-top:0pt;margin-bottom:6pt;"><span class="Poem">Adam, George (Paisley) (SNP) <br />'
        line2 = 'Adamson, Clare (Central Scotland) (SNP) <br />'
        scraper.process_msps_line(line, node, n_law)
        scraper.process_msps_line(line2, node, n_law)
        self.assertEqual(n_law.law_for, ["Adam George (Paisley) (SNP)", "Adamson Clare (Central Scotland) (SNP)"])
        self.assertEqual(n_law.law_against, [])
        self.assertEqual(n_law.law_abstention, [])

    # Test correct data for new line
    # Against node
    def test_process_msps_line_node_against_two_correct_lines(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "against"
        # Create a malformed line
        line = '<p style="margin-top:0pt;margin-bottom:6pt;"><span class="Poem">Adam, George (Paisley) (SNP) <br />'
        line2 = 'Adamson, Clare (Central Scotland) (SNP) <br />'
        scraper.process_msps_line(line, node, n_law)
        scraper.process_msps_line(line2, node, n_law)
        self.assertEqual(n_law.law_for, [])
        self.assertEqual(n_law.law_against, ["Adam George (Paisley) (SNP)", "Adamson Clare (Central Scotland) (SNP)"])
        self.assertEqual(n_law.law_abstention, [])

    # Test correct data for new line
    # Abstention node
    def test_process_msps_line_node_abstention_two_correct_lines(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "abstention"
        # Create a malformed line
        line = '<p style="margin-top:0pt;margin-bottom:6pt;"><span class="Poem">Adam, George (Paisley) (SNP) <br />'
        line2 = 'Adamson, Clare (Central Scotland) (SNP) <br />'
        scraper.process_msps_line(line, node, n_law)
        scraper.process_msps_line(line2, node, n_law)
        self.assertEqual(n_law.law_for, [])
        self.assertEqual(n_law.law_against, [])
        self.assertEqual(n_law.law_abstention, ["Adam George (Paisley) (SNP)", "Adamson Clare (Central Scotland) (SNP)"])

    # Test correct data for new line
    # Abstention node
    # With doctor
    def test_process_msps_line_node_abstention_with_doctor_two_correct_lines(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Create a node
        node = "abstention"
        # Create a malformed line
        line = '<p style="margin-top:0pt;margin-bottom:6pt;"><span class="Poem">Adam, George (Paisley) (SNP) <br />'
        line2 = 'Simpson, Dr Richard (Mid Scotland and Fife) (Lab) <br />'
        scraper.process_msps_line(line, node, n_law)
        scraper.process_msps_line(line2, node, n_law)
        self.assertEqual(n_law.law_for, [])
        self.assertEqual(n_law.law_against, [])
        self.assertEqual(n_law.law_abstention, ["Adam George (Paisley) (SNP)", "Simpson Richard (Mid Scotland and Fife) (Lab)"])

    # Test adding msps for the old style
    # No data on line
    def test_process_old_msps_line_no_data(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Malformed line
        line = ""
        scraper.process_old_msp(line, n_law)
        self.assertEqual(n_law.law_for, [])
        self.assertEqual(n_law.law_against, [])
        self.assertEqual(n_law.law_abstention, [])

    # Test adding msps for the old style
    # Correct data on line
    def test_process_old_msps_line_correct_data(self):
        # Create a new node for law
        n_law = scraper.law.Law()
        # Correct line
        line = '''<div class='content'>There will be a division.<br /><br />For<br /><br />Adam, Brian (Aberdeen North) (SNP)<br /><br />Allan, Alasdair (Western Isles) (SNP)<br /><br />Against<br /><br />Aitken, Bill (Glasgow) (Con)<br /><br />Baker, Claire (Mid Scotland and Fife) (Lab)<br /><br />Munro, John Farquhar (Ross, Skye and Inverness West) (LD)<br /><br />Abstentions<br /><br />MacDonald, Margo (Lothians) (Ind)<br /><br /></div></li><li><a name='Cont_1187928'></a><span id='scrolltoCid_1187928'></span><a href="http://www.scottish.parliament.uk/msps/currentmsps/Alex-Fergusson-MSP.aspx" alt="Fergusson, Alex - Scottish Conservative and Unionist Party - Galloway and West Dumfries" class="or_speaker">The Presiding Officer: </a><span class="SocialArea">'''
        scraper.process_old_msp(line, n_law)
        self.assertEqual(n_law.law_for, ["Adam Brian (Aberdeen North) (SNP)",
                                         "Allan Alasdair (Western Isles) (SNP)"
                                         ])
        self.assertEqual(n_law.law_against, ["Aitken Bill (Glasgow) (Con)",
                                             "Baker Claire (Mid Scotland and Fife) (Lab)",
                                             "Munro John Farquhar (Ross, Skye and Inverness West) (LD)"])
        self.assertEqual(n_law.law_abstention, ["MacDonald Margo (Lothians) (Ind)"])

    # Test trimming html tags
    # It does not work on every possible case by design, because they don't appear here
    def test_trim_html_no_value(self):
        line = ""
        self.assertEqual(scraper.trim_html(line), "")

    # Test trimming html tags
    # It does not work on every possible case by design, because they don't appear here
    def test_trim_html_html_value(self):
        line = '''<a id="copy_social_1766767" href="javascript:void(0);" data-clipboard-text="http://www.scottish.parliament.uk/parliamentarybusiness/28862.aspx?r=9666&i=87804&c=1766767" tooltip="Copy this URL to link directly to this part of the report">Copy Link</a>'''
        self.assertEqual(scraper.trim_html(line), "Copy Link")

    # Test the main function
    # Way too complicated to test it all, so only the most important things
    # Too many side effects, I need to code better!
    # Poor branch predictor also
    # Hasta siempre el functional programming, viva el OCaml

    # File input does not exist
    def test_process_html_no_file_input(self):
        self.assertRaises(EnvironmentError, scraper.process_html("nope.txt", 0))

    # Non-sensical file input
    def test_process_html_nonsensical_file_input(self):
        self.assertRaises(Exception, scraper.process_html("test_scraper.py", 0))

    # Test the topic classifier
    def test_topic_classifier_no_input(self):
        self.assertEqual(topic_extracter.get_topic_from_text(""), "unknown")

    def test_topic_classifier_random_input(self):
        self.assertEqual(topic_extracter.get_topic_from_text("fyraebti gatir gatihnb agbinh ïreg trs"), "unknown")

    def test_topic_classifier_correct_input(self):
        self.assertEqual(topic_extracter.get_topic_from_text("Health scotland government hospital fish food cow sport"), "Health")

if __name__ == '__main__':
    unittest.main()