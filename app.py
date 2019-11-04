from flask import Flask, render_template, request
from databaza import get_activities
import databaza

app = Flask(__name__)

@app.route('/')
def home():
    #print(get_activities())
    return render_template('index.html')

@app.route('/ranapece/')
def ranapece():
    return render_template('ranapece.html')

@app.route('/skolky/')
def skolky():
    return render_template('skolky.html')

@app.route('/skolky', methods=['POST'])
def search_post():
  if request.method == 'POST':
    id = request.form.get("id")
    id_skolky= request.form.get("id_skolky")
    nazev= request.form.get("nazev")
    typ_postizeni= request.form.get("typ_postizeni")
    expectation_table = databaza.skolky_vyhladavanie(id, id_skolky, nazev, typ_postizeni)
    print(expectation_table)
    return render_template("skolky_search.html",
    expectation_table=expectation_table
    )
   
@app.route('/takulka_skolky')
def tabulka_skolky ():
    expectation_table = databaza.tabulka_skolky()
    print(expectation_table)
    return render_template("tabulka_skolky.html",
    expectation_table=expectation_table,
    )

if __name__ == '__main__':
    app.run(debug=True)
