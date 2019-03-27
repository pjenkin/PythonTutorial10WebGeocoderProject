from flask import Flask, render_template

app = Flask(__name__)


class WebGeocoder():

    def __init__(self):
        """ constructor for WebGeocoder """
        if __name__ == '__main__':
            app.run(debug=True)
            ''' if this app were run by name, eg, to do SQLAlchemy model instantiation,
             then __main__ would not be the instance name '''

    def upload(self):
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success_table', methods=['POSTs'])
def success_table():
    return render_template('success-table.html')


webgeocoder = WebGeocoder()




