README
------

MSPs regularly vote on issues affecting Scottish law. This can potentially
provide a fascinating dataset for visualisation (such as has been done for
the Westminster parliament, e.g.http://sirogers.files.wordpress.com/2011/07/2005plain.pdf).

The data are currently fairly inaccessible. This project will involve building
a web application that can regularly scrape the latest data, save it in a database
and allow users to apply different visualisation algorithms on the fly, displaying
the results in an interactive manner.

The project will provide experience in implementing visualisation algorithms from
within machine learning, as well as the graphical experience required in rendering
the results. If desired, the project could be extended to incorporate textual
analysis of the matters being voted on.
--------------------------------------------------------------------------------

Running locally:

in the SPviz-app directory run:

* pyhton manage.py runserver

then open a browser and enter the following URL:

* http://127.0.0.1:8000
