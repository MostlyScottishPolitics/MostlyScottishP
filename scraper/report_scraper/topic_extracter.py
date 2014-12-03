__author__ = 'pierre'

import re

# Extract a topic from the text of a law
# @input : the text of the law
# @output : a topic among
#       Agriculture
#       Civil and Criminal Justice
#       Education
#       Environment
#       Health
#       Housing
#       Local Government
#       Planning
#       Police and fire services
#       Social work
#       Sports and the Arts
#       Transport



# Assign a score to each topic
# Each time a keyword is encountered, points are awarded for a certain topic
# Weighting based on me
# Yeah, I know...
def topic_score(array):
    agr_score = 0
    civ_score = 0
    ed_score = 0
    env_score = 0
    health_score = 0
    house_score = 0
    loc_score = 0
    plan_score = 0
    police_score = 0
    social_score = 0
    sport_score = 0
    trans_score = 0

    for word in array:
        if "agricult" in word:
            agr_score += 3
        if "aquacult" in word:
            agr_score += 3
        if "farm" in word:
            agr_score += 3
        if "fish" in word:
            agr_score += 2
        if "agriculture" in word:
            agr_score += 3
        if "crime" in word:
            civ_score += 3
        if "justice" in word:
            civ_score += 3
        if "tri" in word:
            civ_score += 3
        if "education" in word:
            ed_score += 3
        if "environment" in word:
            env_score += 3
        if "health" in word:
            health_score += 3
        if "obesity" in word:
            health_score += 3
        if "overweight" in word:
            health_score += 3
        if "house" in word:
            house_score += 3
        if "habitation" in word:
            house_score += 3
        if "energy" in word:
            house_score += 1
            env_score += 1
        if "government" in word:
            loc_score += 1
        if "parliament" in word:
            loc_score += 1
        if "scot" in word:
            loc_score += 1
        if "devolv" in word:
            loc_score += 1
        if "planning" in word:
            plan_score += 3
        if "police" in word:
            police_score += 3
        if "officer" in word:
            police_score += 2
        if "social" in word:
            social_score += 3
        if "sport" in word:
            sport_score += 3
            health_score += 1
        if "football" in word:
            sport_score += 3
        if "rugby" in word:
            sport_score += 3
        if "golf" in word:
            sport_score += 3
        if "swim" in word:
            sport_score += 3
            health_score += 1
        if "athlet" in word:
            sport_score += 2
        if "transport" in word:
            trans_score += 3
        if "bus" in word:
            trans_score += 3
        if "driv" in word:
            trans_score += 2
        if "road" in word:
            trans_score += 2
        if "traffic" in word:
            trans_score += 2
        if "car" in word:
            trans_score += 2
            env_score += 1
        if "subway" in word:
            trans_score += 3
        if "passenger" in word:
            trans_score += 2
        if "journey" in word:
            trans_score += 1
        if "airport" in word:
            trans_score += 3
        if "train" in word:
            trans_score += 3
        if "food" in word:
            health_score += 1
            agr_score += 1
        if "drink" in word:
            health_score += 1
        if "nature" in word:
            env_score += 1

    topic = "unknown"
    topic_value = 0
    if agr_score > 0 and agr_score > topic_value:
        topic = "Agriculture"
        topic_value = agr_score
    if civ_score > 0 and civ_score > topic_value:
        topic = "Civil and Criminal Justice"
        topic_value = civ_score
    if ed_score > 0 and ed_score > topic_value:
        topic = "Education"
        topic_value = ed_score
    if env_score > 0 and env_score > topic_value:
        topic = "Environment"
        topic_value = env_score
    if health_score > 0 and health_score > topic_value:
        topic = "Health"
        topic_value = health_score
    if house_score > 0 and house_score > topic_value:
        topic = "Housing"
        topic_value = house_score
    if loc_score > 0 and loc_score > topic_value:
        topic = "Local Government"
        topic_value = loc_score
    if plan_score > 0 and plan_score > topic_value:
        topic = "Planning"
        topic_value = plan_score
    if police_score > 0 and police_score > topic_value:
        topic = "Police and Fire Services"
        topic_value = police_score
    if social_score > 0 and social_score > topic_value:
        topic = "Social Work"
        topic_value = social_score
    if sport_score > 0 and sport_score > topic_value:
        topic = "Sports and the Arts"
        topic_value = sport_score
    if trans_score > 0 and trans_score > topic_value:
        topic = "Transport"
        topic_value = trans_score

    return topic


# Process :
#   -get the text
#   -break it into tokens
#   -remove stop words?
#   -stemming?
#   -try to match the more common words to a topic
#   -if that fails, returns "unknown" topic?
def get_topic_from_text(text):
    token_array = []

    # Tokenizer
    # A token is a word with a special character on each side (space, comma, ...)
    # Low accuracy definition, but should be enough
    token_array = token_array + re.findall(r"\w+",text)
    # To lowercase
    token_array = [x.lower() for x in token_array]

    # Stop-words removal
    # Open the stop-words file and load it into an array
    # Remove the token matching those from this array from the token array
    # Stop-words list courtesy of the Flair IR system
    try:
        with open("stopfile.txt", "r") as stop_file:
            stop_array = stop_file.readlines()
            stop_array = [s.strip('\n') for s in stop_array]
    except IOError, e:
        print("Can't open stopfile.txt")

    cleaned_token_array = [x for x in token_array if x not in stop_array]

    return topic_score(cleaned_token_array)


