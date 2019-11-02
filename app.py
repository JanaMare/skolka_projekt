from flask import Flask, render_template
from databaza import get_activities
import databaza
app = Flask(__name__)
@app.route('/')
def home():
    print(get_activities())
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/skolky/')
def skolky():
    return render_template('skolky.html')
   
@app.route('/vyhledavani/')
def vyhledavani():
    return render_template('vyhledavani.html')

@app.route('/takulka_skolky')
def tabulka_skolky ():
    expectation_table = databaza.tabulka_skolky()
    print(expectation_table)
    return render_template("tabulka_skolky.html",
    expectation_table=expectation_table,
    )

if __name__ == '__main__':
    app.run(debug=True)
