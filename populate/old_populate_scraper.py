# -*- coding: utf-8 -*-
# works fine, but not great for frameworky, updaty stuff
import csv
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Spviz.scottviz.scottviz.settings")
from dateutil import parser
from decimal import *
from xml.dom import minidom
from Spviz.scottviz.scottviz_app.models import *

# images from http://www.scottish.parliament.uk/msps/53234.aspx, need to include licence
# TO DO: more manual urls??  or photos from Pierre
msp_img_urls = {
'Brian Adam' : "http://upload.wikimedia.org/wikipedia/commons/a/a3/BrianAdamMSP20070509.jpg",
'George Adam' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853219542.jpg",
'Clare Adamson' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/ClareAdamsonMSP20110507.JPG",
'Alasdair Allan' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/AlasdairAllanMSP20120530.jpg",
'Christian Allard' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/ChristianAllardMSP_20130515.jpg",
'Jackie Baillie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853239417.jpg",
'Claire Baker' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/ClaireBakerMSP20110825.jpg",
'Richard Baker' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853241871.jpg",
'Jayne Baxter' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JayneBaxterMSP20121211.jpg",
'Claudia Beamish' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853242760.jpg",
'Colin Beattie' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/ColinBeattieMSP20110509.JPG",
'Marco Biagi' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/MarcoBiagiMSP20110509.JPG",
'Neil Bibby' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/NeilBibbyMSP20110510.JPG",
'Sarah Boyack' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/SarahBoyackMSP20120529.jpg",
'Chic Brodie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853248470.jpg",
'Gavin Brown' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853249293.jpg",
'Keith Brown' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853250168.jpg",
'Cameron Buchanan' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/CameronBuchananMSP20140129.jpg",
'Margaret Burgess' : "http://www.scottish.parliament.uk/images/MSP%20Photos/BurgessMargaretIG.jpg",
'Aileen Campbell' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/AileenCampbellMSP20110510.JPG",
'Roderick Campbell' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/RoderickCampbellMSP20131016.jpg",
'Jackson Carlaw' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JacksonCarlawMSP20110509.JPG",
'Malcolm Chisholm' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853233410.jpg",
'Willie Coffey' : "http://www.scottish.parliament.uk/images/WillieCoffeyMSP20120523.jpg",
'Angela Constance' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853259652.jpg",
'Bruce Crawford' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853260503.jpg",
'Roseanna Cunningham' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/RoseannaCunningham20110615.jpg",
'Ruth Davidson' : "http://www.scottish.parliament.uk/images/RuthDavidsonMSP20120529.jpg",
'Graeme Dey' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853220957.jpg",
'Nigel Don' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853221226.jpg",
'Bob Doris' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853222113.jpg",
'James Dornan' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JamesDornanMSP20110507.JPG",
'Kezia Dugdale' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853226958.jpg",
'Helen Eadie' : "http://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/HelenEadieMSP20070509.jpg/85px-HelenEadieMSP20070509.jpg",
'Jim Eadie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853227726.jpg",
'Annabelle Ewing' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853231910.jpg",
'Fergus Ewing' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853232448.jpg",
'Linda Fabiani' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853240611.jpg",
'Mary Fee' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853240870.jpg",
'Patricia Ferguson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853242528.jpg",
'Alex Fergusson' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/AlexFergussonMSP20110511.jpg",
'Neil Findlay' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853244349.jpg",
'John Finnie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853245791.jpg",
'Joe FitzPatrick' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853249335.jpg",
'Murdo Fraser' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853250520.jpg",
'Kenneth Gibson' : "http://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/KennethGibsonMSP20110507.JPG/85px-KennethGibsonMSP20110507.JPG",
'Rob Gibson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853255175.jpg",
'Annabel Goldie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853257110.jpg",
'Christine Grahame' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/ChristineGrahameMSP20110510.JPG",
'Rhoda Grant' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853216633.jpg",
'Iain Gray' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853225741.jpg",
'Mark Griffin' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853262248.jpg",
'Patrick Harvie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853480137.jpg",
'Hugh Henry' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853480588.jpg",
'Jamie Hepburn' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853481923.jpg",
'Cara Hilton' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/Cara_Hilton_MSP.jpg",
'Jim Hume' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JimHumeMSP20110510.JPG",
'Fiona Hyslop' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853484194.jpg",
'Adam Ingram' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853485554.jpg",
'Alex Johnstone' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/AlexJohnstoneMSP20110509.JPG",
'Alison Johnstone' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/AlisonJohnstoneMSP20120119.jpg",
'Colin Keir' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853499797.jpg",
'James Kelly' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JamesKelly20140520.jpg",
'Bill Kidd' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders/BillKiddMSP20070509.jpg",
'Johann Lamont' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853504141.jpg",
'John Lamont' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853504882.jpg",
'Richard Lochhead' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853506741.jpg",
'Richard Lyle' : "http://upload.wikimedia.org/wikipedia/commons/thumb/6/60/RichardLyleMSP20120127.jpg/85px-RichardLyleMSP20120127.jpg",
'Kenny MacAskill' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853507149.jpg",
'Lewis Macdonald' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/LewisMacdonaldMSP20110510.JPG",
'Angus MacDonald' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853507900.jpg",
'Gordon MacDonald' : "http://www.scottish.parliament.uk/images/MSP%20Photos/GordonMacDonaldMSP.jpg",
'Margo MacDonald' : "http://upload.wikimedia.org/wikipedia/commons/thumb/7/79/MargoMacDonaldMSP20111121.jpg/85px-MargoMacDonaldMSP20111121.jpg",
'Ken Macintosh' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853527816.jpg",
'Derek Mackay' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/DerekMacKayMSP20110509.JPG",
'Mike MacKenzie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853509411.jpg",
'Hanzala Malik' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/HanzalaMalikMSP20110601.jpg",
'Jenny Marra' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853514522.jpg",
'Paul Martin' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/PaulMartinMSP20110511.JPG",
'Tricia Marwick' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders/TriciaMarwickMSP.jpg",
'John Mason' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JohnMasonMSP20110509.JPG",
'Michael Matheson' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/MichaelMathesonMSP20110507.JPG",
'Stewart Maxwell' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853518144.jpg",
'Joan McAlpine' : "http://www.scottish.parliament.uk/images/JoanMcAlpineMSP20120529.jpg",
'Liam McArthur' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/LiamMcArthurMSP20110510.JPG",
'Margaret McCulloch' : "http://www.scottish.parliament.uk/images/MSP%20Photos/McCullochMargaret.jpg",
'Mark McDonald': "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853521925.jpg",
'Margaret McDougall' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853521965.jpg",
'Jamie McGrigor' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853522127.jpg",
'Alison McInnes' : "http://www.scottish.parliament.uk/images/MSP%20Photos/AlisonMcinnes_20130522.jpg",
'Christina McKelvie' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/ChristinaMcKelvieMSP20110510.JPG",
'Aileen McLeod' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/AileenMcLeodMSP.jpg",
'Fiona McLeod' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853524252.jpg",
'David McLetchie' : "http://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/DavidMcLetchieMSP20110509.JPG/85px-DavidMcLetchieMSP20110509.JPG",
'Michael McMahon' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853525411.jpg",
'Siobhan McMahon' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853525209.jpg",
'Stuart McMillan' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853525711.jpg",
'Duncan McNeil' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/duncan-mcneilMSP02072013.jpg",
'Anne McTaggart' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/Anne-McTaggart20140319.jpg",
'Nanette Milne' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/NanetteMilneMSP20110509.JPG",
'Margaret Mitchell' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/MargaretMitchellMSP20140403.jpg",
'Elaine Murray': "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853530243.jpg",
'Alex Neil' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853531419.jpg",
'John Park' : "http://upload.wikimedia.org/wikipedia/commons/thumb/0/02/John-Park-MSP.jpg/85px-John-Park-MSP.jpg",
'Gil Paterson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853534583.jpg",
'Graeme Pearson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853536823.jpg",
'John Pentland' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JohnPentlandMSP20110508.JPG",
'Willie Rennie' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853537139.jpg",
'Dennis Robertson' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/dennisRobertson20120627.jpg",
'Shona Robison' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/ShonaRobisonMSP20110511.jpg",
'Alex Rowley' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/AlexRowleyMSP20140129.jpg",
'Michael Russell': "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853541633.jpg",
'Alex Salmond' : "http://www.scottish.parliament.uk/images/MSP%20Photos/SalmondAlexIG.jpg",
'Mary Scanlon' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853619775.jpg",
'John Scott' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853619194.jpg",
'Tavish Scott' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853620466.jpg",
'Richard Simpson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853629298.jpg",
'Drew Smith' : "http://www.scottish.parliament.uk/images/MSP%20Photos/SmithDrewIG.jpg",
'Elaine Smith' : "http://www.scottish.parliament.uk/images/ElaineSmithMSP20120524.jpg",
'Liz Smith' : "http://www.scottish.parliament.uk/images/MSP%20Photos/SmithLizIG.jpg",
'Stewart Stevenson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853634458.jpg",
'David Stewart' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853635694.jpg",
'Kevin Stewart' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853636994.jpg",
'Nicola Sturgeon' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853640645.jpg",
'John Swinney' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JohnSwinneyMSP20110510.JPG",
'Dave Thompson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_11405270866.jpg",
'David Torrance' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/DavidTorranceMSP20111207.jpg",
'Jean Urquhart' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/JeanUrquhartMSP20110510.JPG",
'Bill Walker' : "http://upload.wikimedia.org/wikipedia/commons/thumb/1/13/BillWalkerMSP20110720.jpg/85px-BillWalkerMSP20110720.jpg",
'Maureen Watt' : "http://www.scottish.parliament.uk/images/MSPs%20and%20office%20holders%20Session%204/MaureenWatt20110507.JPG",
'Paul Wheelhouse' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853652552.jpg",
'Sandra White' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853653523.jpg",
'John Wilson' : "http://www.scottish.parliament.uk/images/MSP%20Photos/JohnWilsonMSP.jpg",
'Humza Yousaf' : "http://www.scottish.parliament.uk/images/MSP%20Photos/scottishparliament_9853621795.jpg"
}

# cabinet here http://en.wikipedia.org/wiki/Scottish_Government#Ministers
# TO DO: more jobs
# TO TO: think how to have a history of jobs
jobs = [
['Brian','Adam','Minister for Parliamentary Business and Chief Whip',parser.parse('25 May 2011'),parser.parse('6 September 2012')],
['Alasdair', 'Allan', 'Minister for Learning, Science and Scotland\'s Languages', parser.parse('7 December 2011'),parser.parse('5 May 2016')],
['Claire','Baker','Deputy Convener of the Scottish Parliament Education and Culture Committee',parser.parse('14 June 2011'), parser.parse('5 May 2016')],
['Marco','Biagi','Minister for Local Government and Community Empowerment',parser.parse('5 May 2011'),parser.parse('5 May 2016')],
['Gavin','Brown','Convener of the Scottish Parliament Economy, Energy and Tourism Committee',parser.parse('8 June 2011'),parser.parse('5 May 2016')],
['Keith','Brown','Cabinet Secretary for Infrastructure, Investment and Cities',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Keith','Brown','Minister for Transport and Veterans',parser.parse('11 December 2010'),parser.parse('21 November 2014')],
['Margaret','Burgess','Minister for Housing and Welfare',parser.parse('5 September 2012'),parser.parse('5 May 2016')],
['Aileen','Campbell','Minister for Children and Young People',parser.parse('7 December 2011'),parser.parse('5 May 2016')],
['Aileen','Campbell','Minister for Local Government and Planning',parser.parse('25 May 2011'),parser.parse('7 December 2011')],
['Jackson','Carlaw','Deputy Leader of the Scottish Conservatives',parser.parse('10 November 2011'),parser.parse('5 May 2016')],
['Angela', 'Constance', 'Minister for Youth Employment', parser.parse('7 December 2011'),parser.parse('22 April 2014')],
['Angela', 'Constance', 'Cabinet Secretary for Education and Lifelong Learning', parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Angela', 'Constance', 'Cabinet Secretary for Training, Youth and Women\'s Employment', parser.parse('22 April 2014'),parser.parse('21 November 2014')],
['Angela', 'Constance', 'Minister for Children and Young People', parser.parse('25 May 2011'),parser.parse('7 December 2011')],
['Angela', 'Constance', 'Minister for Skills and Lifelong Learning', parser.parse('12 December 2010'),parser.parse('25 May 2011')],
['Bruce','Crawford','Cabinet Secretary for Parliament and Government Strategy',parser.parse('19 May 2011'),parser.parse('5 September 2012')],
['Roseanna','Cunningham','Cabinet Secretary for Fair Work, Skills and Training',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Roseanna','Cunningham','Minister for Community Safety and Legal Affairs',parser.parse('25 May 2011'),parser.parse('21 November 2014')],
['Ruth','Davidson','Leader of the Scottish Conservatives',parser.parse('4 November 2011'),parser.parse('5 May 2016')],
['Nigel','Don','Convener of the Scottish Parliament Subordinate Legislation Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Bob','Doris','Deputy Convener of the Scottish Parliament Health and Sport Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['James','Dornan','Deputy Convener of the Scottish Parliament Subordinate Legislation Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Helen','Eadie','Deputy Convener of the Scottish Parliament Standards, Procedures and Public Appointments Committee',parser.parse('14 June 2011 '),parser.parse('9 November 2013')],
['Annabelle','Ewing','Deputy Convener of the Scottish Parliament Rural Affairs, Climate Change and Environment Committee',parser.parse('15 June 2011'),parser.parse('21 November 2014')],
['Fergus','Ewing','Minister for Energy, Enterprise and Tourism',parser.parse('20 May 2011'), parser.parse('5 May 2016')],
['Linda','Fabiani','Convener of the Scottish Parliament Scotland Bill Committee',parser.parse('21 June 2011'),parser.parse('5 May 2016')],
['Mary','Fee','Convener of the Scottish Parliament Equal Opportunities Committee',parser.parse('10 January 2012'),parser.parse('5 May 2016')],
['Joe','FitzPatrick','Minister for Parliamentary business',parser.parse('5 September 2012'),parser.parse('5 May 2016')],
['Murdo','Fraser','Deputy Convener of the Scottish Parliament Public Audit Committee',parser.parse('20 June 2007'),parser.parse('5 May 2016')],
['Kenneth','Gibson','Convener of the Scottish Parliament Finance Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Rob','Gibson','Convener of the Scottish Parliament Rural Affairs, Environment and Climate Change Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Christine','Grahame','Convener of the Scottish Parliament Justice Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Hugh','Henry','Convener of the Scottish Parliament Public Audit Committee',parser.parse('26 September 2007'),parser.parse('5 May 2016')],
['Jamie','Hepburn','Minister for Sport and Health Improvement',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Fiona','Hyslop','Cabinet Secretary for Culture, Europe and External Affairs',parser.parse(''),parser.parse('5 May 2016')],
['James','Kelly','Shadow Cabinet Secretary for Infrastructure, Investment and Cities Strategy',parser.parse('28 June 2013'),parser.parse('5 May 2016')],
['James','Kelly','Labour Chief Whip',parser.parse('10 January 2012'),parser.parse('28 June 2013')],
['James','Kelly','Deputy Convener of the Scottish Parliament Scotland Bill Committee',parser.parse('21 June 2011'),parser.parse('5 May 2016')],
['James','Kelly','Deputy Convener of the Scottish Parliament Justice Committee',parser.parse('14 June 2011'),parser.parse('10 January 2012')],
['Johann','Lamont','Leader of the Scottish Labour Party',parser.parse('17 December 2011'),parser.parse('24 October 2014')],
['Richard','Lochhead','Cabinet Secretary for Rural Affairs, Food and Environment',parser.parse('17 May 2007'),parser.parse('5 May 2016')],
['Kenny','MacAskill','Cabinet Secretary for Justice',parser.parse('17 May 2007'),parser.parse('21 November 2014')],
['Derek','Mackay','Minister for Transport and Islands',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Derek','Mackay','Minister for Local Government and Planning',parser.parse('7 December 2011'),parser.parse(' 21 November 2014')],
['Hanzala','Malik','Deputy Convener of the Scottish Parliament European and External Relations Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Tricia','Marwick','4th Presiding Officer of the Scottish Parliament',parser.parse('11 May 2011'),parser.parse('5 May 2016')],
['John','Mason','Deputy Convener of the Scottish Parliament Finance Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Michael','Matheson','Cabinet Secretary for Justice',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Michael','Matheson','Minister for Public Health',parser.parse('20 May 2011'),parser.parse('21 November 2014')],
['Stewart','Maxwell','Convener of the Scottish Parliament Education and Culture Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Joan','McAlpine','Parliamentary Liaison Officer to the First Minister of Scotland',parser.parse('5 May 2011'),parser.parse('5 May 2016')],
['Christina','McKelvie','Convener of the Scottish Parliament European and External Relations Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Duncan','McNeil','Convener of the Scottish Parliament Health and Sport Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Alex','Neil','Cabinet Secretary for Social Justice, Communities and Pensioners\' Rights',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Alex','Neil','Cabinet Secretary for Health and Wellbeing',parser.parse('5 September 2012'),parser.parse('21 November 2014')],
['Willie','Rennie','Leader of the Scottish Liberal Democrats',parser.parse('17 May 2011'),parser.parse('5 May 2016')],
['Shona','Robison','Cabinet Secretary for Health, Wellbeing and Sport',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Shona','Robison','Cabinet Secretary for Commonwealth Games, Sport, Equalities and Pensioners\ Rights',parser.parse('22 April 2014'),parser.parse('1 November 2014')],
['Michael','Russell','Cabinet Secretary for Education and Lifelong Learning',parser.parse('1 December 2009'),parser.parse('21 November 2014')],
['Alex', 'Salmond', 'First Minister', parser.parse('16 May 2007'), parser.parse('20 November 2014')],
['Alex', 'Salmond', 'Leader of the Scottish National Party', parser.parse('3 September 2004'), parser.parse('14 November 2014')],
['John', 'Scott', 'Deputy Presiding Officer', parser.parse('11 May 2011'), parser.parse('5 May 2016')],
['Elaine', 'Smith', 'Deputy Presiding Officer', parser.parse('11 May 2011'), parser.parse('5 May 2016')],
['Stewart','Stevenson','Minister for Environment and Climate Change',parser.parse('25 May 2011 '),parser.parse('6 September 2012')],
['David','Stewart','Convener of the Scottish Parliament Public Petitions Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Kevin','Stewart','Convener of the Scottish Parliament Local Government and Regeneration Committee',parser.parse('1 November 2012'),parser.parse('5 May 2016')],
['Nicola', 'Sturgeon', 'First Minister', parser.parse('20 November 2014'), parser.parse('5 May 2016')],
['Nicola', 'Sturgeon', 'Leader of the Scottish National Party', parser.parse('14 November 2014'), parser.parse('5 May 2016')],
['Nicola', 'Sturgeon', 'Deputy First Minister of Scotland', parser.parse('17 May 2007'), parser.parse(' 19 November 201')],
['Nicola', 'Sturgeon', 'Cabinet Secretary for Infrastructure, Investment and Cities', parser.parse('5 September 2012'), parser.parse('19 November 2014')],
['John', 'Swinney', 'Cabinet Secretary for Finance, Constitution and Economy', parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['John', 'Swinney', 'Deputy First Minister of Scotland', parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['John', 'Swinney', 'Cabinet Secretary for Finance, Constitution and Economy', parser.parse('17 May 2007'),parser.parse('5 May 2016')],
['Dave','Thompson','Convener of the Scottish Parliament Standards, Procedures and Public Appointments Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['Maureen','Watt','Minister for Public Health',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Maureen','Watt','Minister for Public Health',parser.parse('21 November 2014'),parser.parse('5 May 2016')],
['Maureen','Watt','Convener of the Scottish Parliament Infrastructure and Capital Investment Committee',parser.parse('15 June 2011'),parser.parse('5 May 2016')],
['Sandra','White','Deputy Convener of the Scottish Parliament Public Petitions Committee',parser.parse('14 June 2011'),parser.parse('5 May 2016')],
['John','Wilson','Deputy Convener of the Scottish Parliament Economy, Energy and Tourism Committee',parser.parse('8 June 201'),parser.parse('5 May 2016')],
['Humza','Yousaf','Minister for Europe and International Development',parser.parse('6 September 2012'),parser.parse('5 May 2016')],
['Humza','Yousaf','Parliamentary Liaison Officer to the First Minister of Scotland',parser.parse('6 May 2011 '),parser.parse('6 September 2012')]
]

def delete_data():
    Constituency.objects.all().delete()
    MSP.objects.all().delete()
    Vote.objects.all().delete()
    Division.objects.all().delete()
    Party.objects.all().delete()
    SPsession.objects.all().delete()
    Job.objects.all().delete()


def populate_constituency():
    with open('../scottviz/static/test_data/districts.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            id = int(float(line[0]))
            parent = int(float(line[1]))
            name = line[2].strip(" \"\'\r\n")

            if parent == 0:
                c = Constituency(id=id, parent=None, name=name)
                c.save()

            else:
                pere = Constituency.objects.get(id=parent)
                c = Constituency(id=id, parent=pere, name=name)
                c.save()


def populate_msps():
    with open('../scraper/msp_scraper/msps.csv', mode='r') as infile:
        reader = csv.reader(infile)
        i = 0
        for row in reader:
            i += 1
            row = row[0].split(';')
            p = Party.objects.get_or_create(name=row[2].strip())[0]
            p.save()
            c = Constituency.objects.get(name=row[3].strip())
            m = MSP(firstname=row[1].strip(), lastname=row[0], constituency=c, party=p, foreignid=i, status=MSP.MEMBER,         # basic data, sufficient to run visualisations & website
                    member_startdate = parser.parse('5 May 2011').date(), member_enddate = parser.parse('5 May 2016').date(),   # (as they should allow nulls for other fields)
                    party_startdate = parser.parse('5 May 2011').date(), party_enddate = parser.parse('5 May 2016').date())     # default ranges, will be overwritten for the few msps that move about
            m.save()

# no longer members, but were in this session
def add_other_msps():
    m = MSP(firstname='Brian', lastname='Adam', constituency=Constituency.objects.get(name='Aberdeen Donside'),
            member_startdate=parser.parse('5 May 2011'), member_enddate=parser.parse(' 25 April 2013'),
            party=Party.objects.get(name='Scottish National Party'),
            party_startdate=parser.parse('5 May 2011'), party_enddate=parser.parse('25 April 2013'),
            status=MSP.DECEASED, foreignid=129,)
    m.save()
    m = MSP(firstname='Helen', lastname='Eadie', constituency=Constituency.objects.get(name='Cowdenbeath'),
            member_startdate=parser.parse('5 May 2011'), member_enddate=parser.parse('9 November 2013'),
            party=Party.objects.get(name='Scottish Labour'),
            party_startdate=parser.parse('5 May 2011'), party_enddate=parser.parse('9 November 2013'),
            status=MSP.DECEASED, foreignid=130)
    m.save()
    m = MSP(firstname='Margo', lastname='MacDonald', constituency=Constituency.objects.get(name='Lothian'),
            member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('4 April 2014'),
            party=Party.objects.get(name='Independent'),
            party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('4 April 2014'),
            status=MSP.DECEASED, foreignid=131)
    m.save()
    m = MSP(firstname='David', lastname='McLetchie', constituency=Constituency.objects.get(name='Lothian'),
            member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('12 August 2013'),
            party=Party.objects.get(name='Scottish Conservative and Unionist Party'),
            party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('12 August 2013'),
            status=MSP.DECEASED, foreignid=132)
    m.save()
    m = MSP(firstname='John', lastname='Park', constituency=Constituency.objects.get(name='Mid Scotland and Fife'),
            member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse('9 November 2012'),
            party=Party.objects.get(name='Scottish Labour'),
            party_startdate = parser.parse('5 May 2011'), party_enddate = parser.parse('7 September 2013'),
            status=MSP.RESIGNED, foreignid=133)
    m.save()
    m = MSP(firstname='Bill', lastname='Walker', constituency=Constituency.objects.get(name='Dunfermline'),
            member_startdate = parser.parse('5 May 2011'), member_enddate = parser.parse(' 9 September 2013'),
            party=Party.objects.get(name='Independent'),
            party_startdate = parser.parse('3 March 2012'), party_enddate = parser.parse(' 9 September 2013'),
            status=MSP.RESIGNED, foreignid=134)
    m.save()

# Should populate with data for msps that move about
def update_transient_msps():
    m = MSP.objects.get(lastname='Allard',firstname ='Christian')
    m.member_startdate = parser.parse('15 May 2013')
    m.save()
    m = MSP.objects.get(lastname='Buchanan',firstname ='Cameron')
    m.member_startdate = parser.parse('4 September 2013')
    m.save()

def msp_photos():
    msps = MSP.objects.all()
    for msp in msps:
        name = str(msp)
        if name in msp_img_urls.keys():
            msp.img = msp_img_urls[name]
            msp.save()

def msp_jobs():
    i=0
    for job in jobs:
        i+=1
        j = Job(job_foreignid=i,name=job[2],msp=MSP.objects.get(firstname=job[0], lastname=job[1]),job_startdate=job[3],job_enddate=job[4])
        j.save()

def populate_votes(files):
    # naive skip files before 06 May 2011, using a switch: currentsession
    # change encouraged
    currentsession = False
    for f in files:
        doc = minidom.parse(f)
        date = doc.getElementsByTagName("date")[0].firstChild.data
        dt = parser.parse(date).date()

        if date == '02 June 2011':
            currentsession = True

        if currentsession:
            laws = doc.getElementsByTagName("law")

            for law in laws:
                motionid = law.getElementsByTagName("id")[0].firstChild.data
                topic_raw = law.getElementsByTagName("topic")[0].firstChild.data
                topic = str(topic_raw.encode('ascii','replace'))
                text_raw = law.getElementsByTagName("text")
                if text_raw == [] :
                    text='n/a'
                else:
                    text_less_raw = text_raw[0].firstChild.data
                    text = str(text_less_raw.encode('ascii','replace'))
                yup = law.getElementsByTagName("agreed")[0].firstChild

                if yup:
                    if yup.data == "agreed":
                        d = Division(parent=None, motionid=motionid, topic=topic, motiontext=text, result=1, date=dt)
                        d.save()
                    else:
                        d = Division(parent=None, motionid=motionid, topic=topic, motiontext=text, result=2, date=dt)
                        d.save()
                else:
                    # TO DO: see if agreeed or disagreed from votes
                    d = Division(parent=None, motionid=motionid, date=dt)
                    d.save()

                if len(law.getElementsByTagName("for")):
                    forMSPs = law.getElementsByTagName("for")[0].getElementsByTagName("msp")
                    for msp in forMSPs:
                        firstname = msp.getElementsByTagName("name")[0].firstChild
                        lastname = msp.getElementsByTagName("surname")[0].firstChild
                        if firstname and lastname:
                            firstname = str(firstname.data)
                            lastname = str(lastname.data)
                            d = Division.objects.get(motionid=motionid)
                            if lastname == 'Mackenzie':
                                lastname =  'MacKenzie'
                            if lastname == 'GIBson':
                                lastname =  'Gibson'
                            if lastname != 'Copy':
                                msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                                v = Vote(msp=msp, division=d, vote=Vote.YES)
                                v.save()

                if len(law.getElementsByTagName("against")):
                    againstMSPs = law.getElementsByTagName("against")[0].getElementsByTagName("msp")
                    for msp in againstMSPs:
                        firstname = msp.getElementsByTagName("name")[0].firstChild
                        lastname = msp.getElementsByTagName("surname")[0].firstChild
                        if firstname and lastname:
                            firstname = str(firstname.data)
                            lastname = str(lastname.data)
                            d = Division.objects.get(motionid=motionid)
                            if lastname == 'Mackenzie':
                                lastname =  'MacKenzie'
                            if lastname == 'GIBson':
                                lastname =  'Gibson'
                            if lastname !='Copy':
                                msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                                v = Vote(msp=msp, division=d, vote=Vote.NO)
                                v.save()

                if len(law.getElementsByTagName("abstain")):
                    abstainMSPs = law.getElementsByTagName("abstain")[0].getElementsByTagName("msp")
                    for msp in abstainMSPs:
                        firstname = msp.getElementsByTagName("name")[0].firstChild
                        lastname = msp.getElementsByTagName("surname")[0].firstChild
                        if firstname and lastname:
                            firstname = str(firstname.data)
                            lastname = str(lastname.data)
                            d = Division.objects.get(motionid=motionid)
                            #if lastname not in ['Allan', 'Simpson', 'Mackenzie', 'Copy', 'GIBson']:
                            msp = MSP.objects.get(lastname=lastname, firstname=firstname)
                            v = Vote(msp=msp, division=d, vote=Vote.ABSTAIN)
                            v.save()

def rebellious_votes():

    divisions = Division.objects.all()

    query = Party.objects.exclude(name__exact='Independent')
    parties = query.exclude(name__exact='No Party Affiliation')
    allparties = Party.objects.all()
    independentparties = allparties.exclude(parties)

    # That means taking into account the dates between which he was a member -- for the latest party??
    # exclude independent
    for party in independentparties:
        party_msps = MSP.objects.filter(party = party)
        this_votes = [vote for vote in Vote.objects.all() if vote.msp in party_msps]
        for vote in this_votes:
            vote.rebellious = False
            vote.save()

    # Check if a vote for msps in not independent parties is rebellious
    for party in parties:
        party_msps = MSP.objects.filter(party = party)
        threshold = (len(party_msps))/2
        for division in divisions:
#            print division
            division_votes = Vote.objects.filter(division = division)
            relevant_votes = [vote for vote in division_votes if vote.msp in party_msps]
            votes = [0, 0, 0, 0, 0]
            votes[1] = len([vote for vote in Vote.objects.filter(division = division, vote = Vote.YES) if vote.msp in party_msps])
            votes[2] = len([vote for vote in Vote.objects.filter(division = division, vote = Vote.NO) if vote.msp in party_msps])
            votes[3] = len([vote for vote in Vote.objects.filter(division = division, vote = Vote.ABSTAIN) if vote.msp in party_msps])
            votes[4] = len([vote for vote in Vote.objects.filter(division = division, vote = Vote.ABSENT) if vote.msp in party_msps])
            max = 4
            if votes[1]>threshold:
                max = 1
            elif votes[2]>threshold:
                max = 2
            elif votes[3]>threshold:
                max = 3
            if max == 2 or max == 3:
                this_votes = [vote for vote in Vote.objects.filter(division = division, vote = Vote.YES) if vote.msp in party_msps]
                for vote in this_votes:
                    vote.rebellious = True
                    if max == 2:
                        vote.party_vote = Vote.NO
                    else:
                        vote.party_vote = Vote.ABSTAIN
                    vote.save()
            if max == 1 or max == 3:
                this_votes = [vote for vote in Vote.objects.filter(division = division, vote = Vote.NO) if vote.msp in party_msps]
                for vote in this_votes:
                    vote.rebellious = True
                    if max == 1:
                        vote.party_vote = Vote.YES
                    else:
                        vote.party_vote = Vote.ABSTAIN
                    vote.save()
            if max == 1 or max == 2:
                this_votes = [vote for vote in Vote.objects.filter(division = division, vote = Vote.ABSTAIN) if vote.msp in party_msps]
                for vote in this_votes:
                    vote.rebellious = True
                    if max == 1:
                        vote.party_vote = Vote.YES
                    else:
                        vote.party_vote = Vote.NO
                    vote.save()



def compute_turnout():
    divisions = Division.objects.all()
    msps = MSP.objects.all()

    # Get all the absent votes to compute turnout
    for division in divisions:
        votes_divison = Vote.objects.filter(division=division)
        msps_absent = set(msps)
        for vote in votes_divison:
            msps_absent = [msp for msp in msps_absent if msp!= vote.msp]
        for msp in msps_absent:
            v = Vote(msp = msp, division = division, vote = Vote.ABSENT)
            v.save()
        division.turnout =  Decimal(129 - len(msps_absent)) * 100 /Decimal(129)
        division.save()

def compute_rebels():
    divisions = Division.objects.all()
    msps = MSP.objects.all()

    # rebels for each division
    for division in divisions:
        division.rebels = len(Vote.objects.filter(division = division, rebellious = True))
        division.save()

    # compute presence and rebellions
    # TO DO : instead of len(divisions) consider the actual set of divisions where he could have been present
    for msp in msps:
        votes_present = len(divisions) - len(Vote.objects.filter(msp=msp, vote=Vote.ABSENT))
        if votes_present > 0 :
            msp.rebellions = Decimal(len(Vote.objects.filter(msp=msp, rebellious=True))) * 100 / Decimal(votes_present)
        msp.presence = votes_present * 100 / Decimal(len(divisions))
        msp.save()

# Might be useful to change such that we get the files only for a specific interval, based on begin-end dates
# this change can be of use for different sessions of parliament or simply for updating?
# For now, I can check for dates for this session while parsing the sml files. But it would be much more efficient to do it here
def get_files(d):
    return [os.path.join(d, f) for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))]


if __name__ == '__main__':
    delete_data()
    populate_constituency()
    print "_const_"
    populate_msps()
    print "_msps_"
    add_other_msps()
    print "_other_"
    update_transient_msps()
    print "_update_"
    msp_photos()
    print "_photos_"
    msp_jobs()
    print "_jobs_"
    print "And now we wait"
    populate_votes(get_files('../scraper/report_scraper/new_data/'))
    print "_votes_"
    rebellious_votes()
    print "_rebellious_votes_"
    compute_turnout()
    print "_turnout_"
    compute_rebels()
    print "_rebels_"
    print "_done_"
