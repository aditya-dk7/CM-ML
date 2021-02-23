import pyrebase, sys
from datetime import datetime 
from APIkeyAndConfig import firebaseConfig, email, password
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()
user = auth.sign_in_with_email_and_password(email,password)
userIDGet = str(user['localId'])
dateTimeCurrent = str(datetime.now())
imageFileName = sys.argv[1]
results_for_storage = storage.child(userIDGet).child(dateTimeCurrent).put(imageFileName, user['idToken'])
#print(results_for_storage)
md5hashForImage = str(results_for_storage['md5Hash'])
nameImage = str(results_for_storage['name'])
data = {
    "nameImage": nameImage,
    "md5Hash": md5hashForImage
}
results = db.child("users").child(userIDGet).push(data, user["idToken"])
