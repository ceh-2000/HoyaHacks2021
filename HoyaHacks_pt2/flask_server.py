from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

import seaborn as sns
import matplotlib.pyplot as plt

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
            past_meats = doc.to_dict()['meat_ct']

    #Push data to firebase
    doc_ref = db.collection(u'users').document(u'our_person')
    doc_ref.set({'meat_ct' : past_meats + new_meats})

    #Building a roast for the meat viewer
    template_roasts = ['Should you really be looking at a page with %s meat mentions??',
                       'You know, there are %s mentions of meat on this page...',
                       'I get it, we can\'t ALL be strong willed. %s meat mentions is a lot though.',
                       'MEAT ALERT: THERE ARE %s MENTIONS OF MEAT HERE!!!',
                       'Look I get it. You\'re weak. But %s mentions of meat? Really?']

    roast = None
    if new_meats > 0:
        roast = choice(template_roasts) % new_meats

    #Building the dict to pass back
    pass_back = {'meat_ct' : past_meats + new_meats,
                 'user' : 'our_person',
                 'new_meats' : new_meats,
                 'contains_meat' : True,
                 'roast' : roast}

    return pass_back

#TODO: fix the breaking + make better plots to send back!
@app.route('/plots', methods = ['GET'])
def make_plots():
    if False:
        #Get meat count data
        users_ref = db.collection(u'users')
        docs = users_ref.stream()
        meat_ct = 0

        for doc in docs:
            if doc.id == 'our_person':
                meat_ct = doc.to_dict()['meat_ct']

        #Make a plot w/seaborn - DOESN'T CURRENTLY PLOT ANYTHING MEANINGFUL, just a test!
        #  TODO: try agin to see if it's still broken!
        ax = sns.pointplot(x = ['Past Meats', 'New Meats'], y = [meat_ct, meat_ct + 5])
        ax.set_title('Your Meat Trajectory', **{'fontweight' : 'bold'})

        plt_fp = 'test.png'
        plt.savefig(plt_fp, dpi = 100)

        #Push the plot into firebase + get URL
        bucket = storage.bucket()
        blob = bucket.blob(plt_fp)
        blob.upload_from_filename(plt_fp)

        blob.make_public()
        plt_url = blob.public_url
    return {'welcome' : 'hello'}

if __name__ == '__main__':
    app.run(debug = True)
