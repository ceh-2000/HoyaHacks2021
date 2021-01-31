#TODO:
#  -figure out putting images into Firebase from Python - GOOD!
#  -figure out Flask API stuff... begin to get set up (peep RamHacks)
#  -figure out how to search HTML for mentions of meat

#FIREBASE STUFF:
if False:
    print('FIREBASE')
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
    from firebase_admin import storage

    #Use a service account
    cred = credentials.Certificate('hoyahacks2021.json')
    firebase_admin.initialize_app(cred, {'storageBucket' : 'hoyahacks2021.appspot.com'})

    db = firestore.client()

    #Adding data
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })

    #Read data
    users_ref = db.collection(u'users')
    docs = users_ref.stream()

    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

    #Sticking an image into Firestore
    fileName = 'dog.jpeg'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    blob.make_public()
    print("your file url", blob.public_url)

#HTML PARSING STUFF:
if False:
    print('HTML PARSING')
    from bs4 import BeautifulSoup
    import requests

    #Nab the HTML data
    site = requests.get('https://www.bonappetit.com/recipe/buttery-kimchi-chicken')
    soup = BeautifulSoup(site.text, 'html.parser')

    #Grab out the site text
    all_text_ish = soup.find_all('p')
    print(all_text_ish[0].text)

#ALTERNATE PLOTTING:
if False:
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.figure import Figure

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    sns.pointplot(x = ['Past Meats', 'New Meats'], y = [10, 10 + 5], ax = axis)
    axis.set_title('Your Meat Trajectory', **{'fontweight' : 'bold'})

    plt_fp = 'test.png'
    fig.savefig(plt_fp, dpi = 100)

if True:
    import matplotlib.pyplot as plt
    import seaborn as sns
    from matplotlib.figure import Figure
    from numpy import cumsum

    our_person = {'site_1' : 3, 'site_2' : 4, 'meat_ct' : 90}
    site_nums = [int(s.split('_')[1]) for s in our_person.keys() if s.split('_')[0] == 'site']

    time_trend = [our_person[s] for s in sorted(our_person) if s != 'meat_ct']
    time_trend = cumsum(time_trend)
    print(time_trend)
    x_axis = [i for i in range(1, len(time_trend) + 1)]
    print(x_axis)

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    sns.lineplot(x = x_axis, y = time_trend, ax = axis)
    axis.set_xticks(range(1, len(time_trend) + 1))
    axis.set_yticks(range(0, max(time_trend) + 1))

    plt_fp = 'meat_trend.png'
    fig.savefig(plt_fp, dpi = 200)
