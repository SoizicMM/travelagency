from flask import Flask, render_template, request, url_for, redirect, session

#Imports
import pymongo
import os
import bcrypt

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


@app.route('/destination')
def destination():
  return render_template("destination.html")

@app.route('/shop')
def shop():
  return render_template("shop.html")
 
  
@app.route('/Validation')
def validation():
    return render_template("validation.html")


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
