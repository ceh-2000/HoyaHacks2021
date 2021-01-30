#TODO:
#  -figure out putting images into Firebase from Python - GOOD!
#  -figure out Flask API stuff... begin to get set up (peep RamHacks)
#  -figure out how to search HTML for mentions of meat

#FIREBASE STUFF:
if True:
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
