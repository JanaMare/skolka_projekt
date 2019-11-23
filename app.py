from flask import Flask, render_template, request
from databaza import get_activities
from databaza import skolky_mesto
from databaza import tabulka_skolky_detail
import databaza 
import os
from flask import Flask, render_template, request, redirect
#from flask_mail import Mail, Message
#from form import ContactForm
#from wtforms import PasswordField
#from flask_wtf import FlaskForm, CsrfProtect
#mail = Mail()

app = Flask(__name__)

#priprava na kontaktny formular
#csrf = CsrfProtect()
#SECRET_KEY = os.urandom(32)
#app.config['SECRET_KEY'] = SECRET_KEY
#csrf.init_app(app)

#app.config['MAIL_SERVER']='smtp.seznam.cz'
#app.config['MAIL_PORT'] = 465


#app.config['MAIL_USERNAME'] = 'specialniskolky@gmail.com'
#app.config['MAIL_PASSWORD'] = '################'

#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USE_SSL'] = False

#mail.init_app(app)

#@app.route('/kontakt', methods=['POST', 'GET'])
#def kontakt():
    #form = ContactForm()
    #if form.validate_on_submit():        
       # print('-------------------------')
        #print(request.form['name'])
        #print(request.form['email'])
        #print(request.form['subject'])
        #print(request.form['message'])       
        #print('-------------------------')
        #send_message(request.form)
        #return redirect('/success')    

    #return render_template('kontakt.html', form=form)

#@app.route('/success')
#def success():
    #return render_template('index.html')

#def send_message(message):
    #print(message.get('name'))

    #msg = Message(message.get('subject'), sender = message.get('email'),
           # recipients = ['id1@gmail.com'],
            #body= message.get('message')
    #)  
    #mail.send(msg)

@app.route('/')
def home():
    #print(get_activities
    return render_template('index.html')

@app.route('/ranapece/')
def ranapece():
   tab_ranna_pece = databaza.tab_ranna_pece()
   return render_template("ranapece.html", tab_ranna_pece=tab_ranna_pece)
    


@app.route('/skolky/')
def skolky():
    return render_template('skolky.html', city=databaza.skolky_mesto())

@app.route('/odlehcovaci_pece/')
def odlehcovaci_pece():
    tab_odlehcovaci = databaza.tab_odlehcovaci()
    return render_template('odlehcovaci_pece.html', tab_odlehcovaci=tab_odlehcovaci)

#skolky, vyhladavanie.. vyhladava podla name tag v html
@app.route('/skolky/', methods=['POST'])
def skolky_post():
 if request.method == 'POST':
    nazev= request.form.get("nazev")
    mesto= request.form.get("city")
    ulice= request.form.get("ulice")
    mail= request.form.get("mail")
    web= request.form.get("web")
    kontakt= request.form.get("kontakt")
    postizeni = []


    if "mentalni" in request.form:
      postizeni.append("mentalni")
      postizeni.append("mentálně")
      postizeni.append("mentalnim")
      postizeni.append("mentálním postižením")
      postizeni.append("mentalne")
      postizeni.append("downuv syndrom")

    if "zrakove" in request.form:
      postizeni.append("zrakovým")
      postizeni.append("zrakove postizeni")
      postizeni.append("zrakove")
      postizeni.append("smyslově")
      postizeni.append("logopedicke zrakove")
      postizeni.append("smyslove postizeni")
      postizeni.append("smyslove")
      postizeni.append("dualni senzoricke")
    if "sluchove" in request.form:
      postizeni.append("sluchove")
      postizeni.append("smyslově")
      postizeni.append("sluchove postizení")
      postizeni.append("sluchovým")
      postizeni.append("smyslove postizeni")
      postizeni.append("smyslove")
      postizeni.append("dualni senzoricke")

    if "recove" in request.form:
      postizeni.append("logopedicke")
      postizeni.append("logopedicke zrakove")
      postizeni.append("komunikacne")
      postizeni.append("kom")
      postizeni.append("vady reči")
      postizeni.append("vady reci")
      postizeni.append("komunikacni")
      postizeni.append("recove")
      
    if "telesne" in request.form:
      postizeni.append("telesne")
      postizeni.append("tele")
      postizeni.append("telesne kombinovane")
      postizeni.append("tělesne")
      postizeni.append("teslenim")
      postizeni.append("tělesným")
      postizeni.append("pohybove") 

    if "kombinovane" in request.form:
      postizeni.append("kombinovane")
      postizeni.append("s vice vadami")
      postizeni.append("kobminovane")
      postizeni.append("vice vad")
      postizeni.append("s vice vadami")
      postizeni.append("telesne kombinovane")

    if "autistickeho" in request.form:
      postizeni.append("autistismus")
      postizeni.append("kombinovaným postižením a děti s poruchami autistického spektra")
      postizeni.append("autismem")
      postizeni.append("autisticke")
      postizeni.append("autistickeho spektra")
      postizeni.append("autisticke")
      postizeni.append("poruchy autistickeho spektra")

    if "poruchauceni" in request.form:
      postizeni.append("porucha uceni") 
      postizeni.append("adhd")
      postizeni.append("snizenim rozumovymi schopnostami")
      postizeni.append("hyperaktivita")
 

    expectation_table = databaza.skolky_vyhladavanie(nazev, postizeni, mesto, ulice)
    lngs = [ x["lng"] for x in expectation_table ]
    lats = [ x["lat"] for x in expectation_table ]
    center = [(max(lngs)-min(lngs))/2 + min(lngs),(max(lats)-min(lats))/2 + min(lats)]
 return render_template("skolky_search.html", center = center,
    expectation_table=expectation_table)

#zobrazenie detailu jednotlivej skolky
@app.route('/skolky_detail/')
def skolkydetail():
  return render_template("skolky_detail.html")
 
@app.route('/skolky_detail/<id_skolky>', methods=['GET'])
def skolky_detail(id_skolky):
    skolky_detail=databaza.tabulka_skolky_detail(id_skolky,)
   # lngs = [ y["lng"] for y in skolky_detail ] #pridala jsem souradnice
   # lats = [ y["lat"] for y in skolky_detail ]
   # center = [(max(lngs)-min(lngs))/2 + min(lngs),(max(lats)-min(lats))/2 + min(lats)]
    return render_template("skolky_detail.html",
    id_skolky=skolky_detail, skolky_detail=skolky_detail,
    )

#error handelers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def pagenot_found(e):
    return render_template("500.html")

#@csfr.error_handler
#def csrf_error(reason):
    #return render_template('csfr_error.html', reason=reason)

if __name__ == '__main__':
    app.run(debug=True)
