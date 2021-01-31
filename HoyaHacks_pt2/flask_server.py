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

from random import choice, randint
from numpy import cumsum

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
#  -CO2 emissions reduction becuase of the meat that you didn't eat
#  -Money savings
#    -400g a day ==> 0.133 kilos a meal
#    -1 kilo = 44.6 car miles of CO2 emission on avg
#    ->Count the meals
@app.route('/plots', methods = ['GET'])
def make_plots():
    #Get meat count data
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    meat_ct = 0

    for doc in docs:
        if doc.id == 'our_person':
            our_person = doc.to_dict()

    #Meat trends over time
    time_trend = [our_person[s] for s in sorted(our_person) if s != 'meat_ct']
    time_trend = cumsum(time_trend)
    x_axis = [i for i in range(1, len(time_trend) + 1)]

    sns.set_style('whitegrid')

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    sns.lineplot(x = x_axis, y = time_trend, ax = axis, color = '#9c4c4c', linewidth = 3)
    axis.set_title('Your Meat Trend', **{'fontweight' : 'bold', 'size' : 20})
    axis.set_xticks(range(1, len(time_trend) + 1))
    axis.set_yticks(range(0, max(time_trend) + 1, 5))
    axis.set_xlabel('Site Count', labelpad = 20)
    axis.set_ylabel('Cumulative Meat Count', labelpad = 20)
    axis.grid(False, axis = 'x')
    axis.spines['right'].set_visible(False)
    axis.spines['left'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.spines['bottom'].set_visible(False)

    plt_fp1 = 'meat_trend' + str(randint(0, 1000)) + '.png'
    fig.tight_layout()
    fig.savefig(plt_fp1, dpi = 200)

    #CO2 reduction plot
    had_meat = sum([our_person[s] > 0 for s in sorted(our_person) if s != 'meat_ct'])
    ttl_meals = len(time_trend)
    meat_eater = 0.133 * 44.6 * ttl_meals
    our_person = 0.133 * 44.6 * had_meat

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.stem(['You'], [our_person], basefmt = ' ', linefmt = 'g', markerfmt = 'go')
    axis.stem(['Meat Eater'], [meat_eater], basefmt = ' ', linefmt = 'r', markerfmt = 'ro')
    axis.set_title('Carbon Emissions Reduction', **{'fontweight' : 'bold', 'size' : 20})
    axis.set_ylabel('CO2 Emissions (car miles)', labelpad = 20)
    axis.grid(False, axis = 'x')
    axis.spines['right'].set_visible(False)
    axis.spines['left'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.margins(x = 0.5)

    plt_fp2 = 'C02_savings' + str(randint(0, 1000)) + '.png'
    fig.savefig(plt_fp2, dpi = 200)

    #Push the plot into firebase + get URL
    urls = []
    bucket = storage.bucket()
    for fp in [plt_fp1, plt_fp2]:
        blob = bucket.blob(fp)
        blob.upload_from_filename(fp)

        blob.make_public()
        urls.append(blob.public_url)

    return {'urls' : [urls]}

if __name__ == '__main__':
    app.run(debug = True)
