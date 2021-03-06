__author__ = 'laura'

import re

from django.db.models import Q

#parse the query to a nice string
def parse(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    norm=re.compile(r'\s{2,}').sub):
    return [norm(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

#get query the models will be queried against
#query is built using Q objects to allow for inexact results
def get_query(query_string, search_fields):
    query = None
    terms = parse(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query