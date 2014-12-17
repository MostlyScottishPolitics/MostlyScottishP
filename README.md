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
To see the latest version go to https://mostlyscottishpolitics.herokuapp.com

To run the project locally:

* install requirements:
$ pip install -r requirements.txt
* scrape the data(will take around an hour the first time it's run)
$ pyhton manage.py scrape
* create a postgres database and add the details in scottviz/settings.py
* to create tables from the models run
$ pyhton manage.py syncdb
* populate the database with data from the scraper
$ pyhton manage.py populate_db
* to later on update the database with new data from the scraper 
$ pyhton manage.py update_db
* to collect the static input to be rendered run
$ python manage.py collectstatic
* and lastly to start the web app:
$ pyhton manage.py runserver

then open a browser and enter the following URL:

* http://127.0.0.1:8000
