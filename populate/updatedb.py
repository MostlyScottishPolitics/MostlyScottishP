__author__ = '2168879m'

from computable import *

if __name__ == '__main__':
    """
    makes the calls to compute analytics
    comment out anything that you don't need/want executed (but populate_basics calls this, not the individual functions)
    change any function def in computable.py or any static data in data.py to get other statistics
    you can add your own functions here (but I would recommend to do it in computable.py)  and put the calls here.
    """
    get_lama_her_csv()
    print "_lama_got_her_csv_"

    populate_data_parties()
    print "_parties_info_"

    compute_rebellious_votes()
    print "_rebelious_votes_"

    compute_division_turnout()
    print "_division_turnout_"

    compute_msp_turnout()
    print "_msp_turnout_"

    compute_division_rebels()
    print "_division_rebels_"

    compute_msp_rebellions()
    print "_msp_rebellions_"

    compute_type_for_divisions()
    print "_type_for_divisions_"

    compute_parents_for_divisions()
    print "_parents_for_divisions_"

    populate_topics()
    print "_topics_ready_for_scatter_"

    compute_topics()
    print "_topics_"

    populate_analytics()
    print "_analytics_"

    print "_done_"