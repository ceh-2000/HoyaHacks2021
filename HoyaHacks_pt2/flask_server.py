from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from web_scraping import get_meats

from random import choice

app = FlaskAPI(__name__)

#Set up DB stuff
cred = credentials.Certificate('hoyahacks2021.json')
firebase_admin.initialize_app(cred, {'storageBucket' : 'hoyahacks2021.appspot.com'})
db = firestore.client()

#Default API endpoint for debugging
@app.route('/', methods = ['GET'])
def home():
    return {'welcome' : 'home'}

#Process the request from chrome extension
@app.route('/meats/<path:input_url>', methods = ['GET'])
def is_meat(input_url):
    #Scrape the passed URL for meats
    new_meats = get_meats(input_url)

    #Grab past meats
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    past_meats = 0

    for doc in docs:
        if doc.id == 'our_person':
            our_person = doc.to_dict()

    past_meats = our_person['meat_ct']
    next_site_num = max([int(s.split('_')[1]) for s in our_person.keys() if s.split('_')[0] == 'site']) + 1

    #Building up dictionary for user
    our_person['site_' + str(next_site_num)] = new_meats
    our_person['meat_ct'] = past_meats + new_meats

    #Push data to firebase
    doc_ref = db.collection(u'users').document(u'our_person')
    doc_ref.set(our_person)

    #Building a roast for the meat viewer
    template_roasts = ['Should you really be looking at a page with %s meat mentions??',
                       'You know, there are %s mentions of meat on this page...',
                       'I get it, we can\'t ALL be strong willed. %s meat mentions is a lot though.',
                       'MEAT ALERT: THERE ARE %s MENTIONS OF MEAT HERE!!!',
                       'Look I get it. You\'re weak. But %s mentions of meat? Really??']

    roast = None
    if new_meats > 0:
        roast = choice(template_roasts) % new_meats

    #Building the dict to pass back
    pass_back = {'meat_ct' : past_meats + new_meats,
                 'user' : 'our_person',
                 'new_meats' : new_meats,
                 'contains_meat' : new_meats > 0,
                 'roast' : roast}

    return pass_back

#PLOTS:
#  -Meat trends over time
#  -CO2 emissions reduction becuase of the meat that you didn't eat
#  -Money savings
#TODO: make this a normal function (not an endpoint) and trigger when new meat is found!
@app.route('/plots', methods = ['GET'])
def make_plots():
    #Get meat count data
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    meat_ct = 0

    for doc in docs:
        if doc.id == 'our_person':
            our_person = doc.to_dict()

    #TEST PLOT
    # fig = Figure()
    # axis = fig.add_subplot(1, 1, 1)
    # sns.pointplot(x = ['Past Meats', 'New Meats'], y = [meat_ct, meat_ct + 5], ax = axis)
    #
    # plt_fp = 'test.png'
    # fig.savefig(plt_fp, dpi = 100)

    #Meat trends over time


    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    #Push the plot into firebase + get URL
    bucket = storage.bucket()
    blob = bucket.blob(plt_fp)
    blob.upload_from_filename(plt_fp)

    blob.make_public()
    plt_url = blob.public_url

    return {'urls' : [plt_url]}

if __name__ == '__main__':
    app.run(debug = True)
