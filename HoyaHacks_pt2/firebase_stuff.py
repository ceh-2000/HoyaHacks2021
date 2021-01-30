import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

 
import seaborn as sns
import matplotlib.pyplot as plt

#YOU WILL GET: parsed text to search for "meat" occurences

#Set up DB stuff
cred = credentials.Certificate('hoyahacks2021.json')
firebase_admin.initialize_app(cred, {'storageBucket' : 'hoyahacks2021.appspot.com'})
db = firestore.client()

#Parse through text
TEXT = 'Mix yogurt, garlic, ginger, gochugaru, fish sauce, salt, and pepper in a medium bowl. Cut chicken thighs crosswise into thirds and add to bowl. Massage yogurt mixture into chicken until well coated. Cover and chill at least 1 hour and up to 3 hours.</p>, <p>Meanwhile, place soybeans in a medium saucepan and pour in 2 cups cold water; bring to a boil. Immediately drain soybeans and rinse under cold running water. Return to pot, pour in 1 cup cold water, and bring to a boil again. Immediately remove from heat and let cool slightly. Transfer soybeans and water to a blender and blend until a thick purée forms. (It’s okay if the soybeans are a bit chunky still; they’ll soften in the braise.) Set aside.</p>, <p>Heat oil in a large Dutch oven over medium-high. Working in 2 batches, remove chicken from marinade, letting any marinade that wants to cling stay on, and cook, stirring occasionally, until browned all over, 5–7 minutes per batch. Using a slotted spoon, transfer chicken to a plate as you go, leaving all the crunchy bits and oil in pot. Set any remaining marinade aside.</p>, <p>Reduce heat to medium-high. Combine onion, kimchi, tomato paste, and reserved marinade in same pot and cook, stirring and scraping up browned bits constantly to prevent burning, until onion is softened and tomato paste darkens slightly and begins to stick to bottom of pot, about 10 minutes. Return chicken, along with any juices collected on plate, to pot and stir in broth, butter, and reserved soybean purée. Bring to a simmer and cook until chicken is just cooked through, 10–15 minutes.</p>, <p>Divide rice among bowls and ladle chicken mixture over. Top with scallions and chile. Serve with pickles alongside if desired.'

meat_words = ['chicken', 'beef', 'ham', 'meat', 'pork', 'salami', 'turkey',
              'steak', 'sausage']
new_meats = sum([TEXT.count(m) for m in meat_words])
print(new_meats)

#Make a plot w/seaborn
#  TODO: make more interesting... save + write more data and make several visualizations!
users_ref = db.collection(u'users')
docs = users_ref.stream()
past_meats = 0

for doc in docs:
    if doc.id == 'our_person':
        past_meats = doc.to_dict()['meat_ct']
# print(past_meats)

ax = sns.pointplot(x = ['Past Meats', 'New Meats'], y = [past_meats, past_meats + new_meats])
ax.set_title('Your Meat Trajectory', **{'fontweight' : 'bold'})

plt_fp = 'test.png'
plt.savefig(plt_fp, dpi = 100)

#Push the plot into firebase + get URL
bucket = storage.bucket()
blob = bucket.blob(plt_fp)
blob.upload_from_filename(plt_fp)

blob.make_public()
plt_url = blob.public_url
print(plt_url)

#Push data to firebase
doc_ref = db.collection(u'users').document(u'our_person')
doc_ref.set({'meat_ct' : past_meats + new_meats})
