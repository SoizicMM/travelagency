from flask import Flask, render_template, request, url_for, redirect, session

#Imports
import pymongo
import os
import bcrypt

# Pour gérer les ObjectId
from bson.objectid import ObjectId

#Création de l'application
app = Flask("Travel Agency")

#Connection à la bdd
mongo = pymongo.MongoClient(os.getenv("MONGO_KEY"))

#Crookie de la session utilisateur
app.secret_key = os.getenv("COOKIES_KEY")

@app.route('/')
def index():
  return render_template("index.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
  #Si on essaye de se connecter
  if request.method == 'POST':
    db_users = mongo.db.users
    user = db_users.find_one({'name': request.form['utilisateur']})
    #Si l'utilisateur est trouvé dans la bdd
    if user:
      #Si le mot de passe correspond à celui enregistré dans la bdd
      if bcrypt.checkpw(request.form['mot_de_passe'].encode('utf-8'), user['password']):
        #On connecte l'utilisateur
        session['user'] = request.form['utilisateur']
        #On retourne à l'accueil
        return redirect(url_for('index'))
      else:
        return render_template("login.html", erreur="Le mot de passe n'est pas bon")
    else:
      return render_template("login.html", erreur="Cet utilisateur n'existe pas")
  else:
    return render_template("login.html")


@app.route('/logout')
def logout():
  session.clear()
  return redirect(url_for("index"))
  

#Route pour créer un compte
@app.route('/register', methods=['POST','GET'])
def register():
  #Si on essaye de créer un compte
  if request.method == 'POST':
    #On crée la variable qui contient la bdd des utilisateurs
    db_users = mongo.db.users
    #On vérifie si l'uilisateur n'xiste pas
    if (db_users.find_one({'name':request.form['utilisateur']})):
      return render_template('register.html', erreur="Cet utilisateur existe déjà")
    else:
      #On compare le mot de passe et la vérification du mot de passe
      if (request.form['mot_de_passe'] == request.form['verif_mot_de_passe']):
        #On crypte le mot de passe
        mdp_crypt = bcrypt.hashpw(request.form['mot_de_passe'].encode('utf-8'),bcrypt.gensalt())
        #On enregistre l'utilisateur dans la bdd
        db_users.insert_one({
        'name': request.form['utilisateur'],
        'password': mdp_crypt
        })
        #On connecte l'utilisateur
        session['user'] = request.form['utilisateur']
        #On le ramène à la page d'accueil
        return redirect(url_for('index'))
      else:
        return render_template('register.html', erreur="Les mots de passse sont différents")
  else:
    return render_template("register.html")


@app.route('/continent')
def continent():
  return render_template("continent.html")

# Toutes les destinations
@app.route('/destination')
def destination():
  db_destination = mongo.db.destination
  destination = db_destination.find({})
  return render_template("destination.html", destination=destination)

# Destination par continent 
@app.route('/europe')
def europe():
  db_destination = mongo.db.destination
  destination = db_destination.find({"continent": "Europe"})
  return render_template("destination.html", destination=destination)

@app.route('/amerique')
def amerique():
  db_destination = mongo.db.destination
  destination = db_destination.find({"continent": "Amérique"})
  return render_template("destination.html", destination=destination)

@app.route('/asie')
def asie():
  db_destination = mongo.db.destination
  destination = db_destination.find({"continent": "Asie"})
  return render_template("destination.html", destination=destination)

@app.route('/afrique')
def afrique():
  db_destination = mongo.db.destination
  destination = db_destination.find({"continent": "Afrique"})
  return render_template("destination.html", destination=destination)

@app.route('/oceanie')
def oceanie():
  db_destination = mongo.db.destination
  destination = db_destination.find({"continent": "Océanie"})
  return render_template("destination.html", destination=destination)

# Route d'une seule ville 
@app.route("/ville/<id_post>")
def ville(id_post):
  db_destination = mongo.db.destination
  destination = db_destination.find_one({"_id": ObjectId(id_post)})
  return render_template("ville.html", destination=destination)

@app.route('/shop')
def shop():
  if 'user' in session :
    return render_template("shop.html")
  else:
    return render_template("login.html")
 
  
@app.route('/Validation')
def validation():
    return render_template("validation.html")

@app.route('/profil')
def profil():
    return render_template("profil.html")

##############
### ADMIN ####
##############

@app.route('/admin/back_lieux')
def admin_lieux():
  db_lieux = mongo.db.destination
  lieux = db_lieux.find({})
  return render_template('admin/back_lieux.html', lieux=lieux)


@app.route('/recherche')
def recherche():
    return render_template("recherche.html")

@app.route('/erreur')
def erreur():
  # declencher volontairement une erreur 404
  return render_template("erreur.html"), 404


# gestionnaire erreur 404
# On utilise le décorateur errorhandler()
@app.errorhandler(404)
def page_not_found(error):
  return render_template("erreur.html"), 404



app.run(host='0.0.0.0', port=81)
