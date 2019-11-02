from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ranapece/')
def about():
    return render_template('ranapece.html')

@app.route('/skolky/')
def skolky():
    return render_template('skolky.html')
   
@app.route('/vyhledavani/')
def vyhledavani():
    return render_template('vyhledavani.html')


if __name__ == '__main__':
    app.run(debug=True)