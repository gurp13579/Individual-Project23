from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {"apiKey": "AIzaSyC_c8g-vEBZQdvj_AXFU2amnDWdGcRGBCQ",
  "authDomain": "website-ca3d1.firebaseapp.com",
  "projectId": "website-ca3d1",
  "storageBucket": "website-ca3d1.appspot.com",
  "messagingSenderId": "794055245089",
  "appId": "1:794055245089:web:a77feb3f6d787ca3681260",
  "databaseURL": "https://website-ca3d1-default-rtdb.europe-west1.firebasedatabase.app/"};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")
    else:
        try:
            email = request.form['email']
            password = request.form['password']
            number = request.form['number']
            login_session['user'] = auth.sign_in_with_email_and_password(email,password,number)
            return redirect(url_for('home.html'))
        except:
            print("password or email is wrong")
            return render_template('home.html')
    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        email = request.form['email']
        password = request.form['password']
        number = request.form['number']
        username = request.form['username']
        fullname = request.form['fullname']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            UID = login_session['user']['localId']
            user = {'email':email,"password":password,"number":number,'username':username,'fullname':fullname}
            db.child('User').child(UID).set(user)
            return redirect(url_for('signin'))
        except:
            print("email already exists")
            return render_template('signup.html')

@app.route('/suggestions', methods=['GET','POST'])
def suggest():
    if request.method == 'GET':
        return render_template('suggestions.html')
    else:
        suggest = {'product':request.form['product'],'picture':request.form['picture']}
        db.child('suggestionstoday').push(suggest)
        return redirect(url_for("show_suggestions"))

@app.route('/suggestionstoday', methods=['GET','POST'])
def show_suggestions():
    return render_template('suggestionstoday.html', d = db.child("suggestionstoday").get().val())

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')




#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)