from flask import Flask, render_template, request, send_file, make_response
from webgeocoder import WebGeocoder
import werkzeug   # TODO - is this needed?

app = Flask(__name__)


@app.route('/download')
def download():
    """ download csv from dataframe"""
    print('In download')
    geocoded_filename = 'geocoded_' + webgeocoder.get_uploaded_filename()
    print(geocoded_filename)
    response = make_response(webgeocoder.download_csv_from_dataframe())
    response.headers['Content-Disposition'] = 'attachment; filename=' + geocoded_filename
    response.headers['Content-Type'] = 'text/csv'
    print(response)
    return response
    # Flask download CSV from pandas dataframe - https://stackoverflow.com/a/38635222

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_success_table():

    try:
        upload_file = request.files['file_name']
    except Exception as exception:
        print(exception)
        return render_template('index.html', result_html=str(exception))
    # webgeocoder.upload(upload_file)
    try:
        webgeocoder.upload_csv(upload_file)
    except Exception as exception:
        print(exception)
        return render_template('index.html', result_html=str(exception))
    try:
        webgeocoder.geocode_dataframe()
    except Exception as exception:
        print(exception)
        return render_template('index.html', result_html=str(exception))
    try:
        result_html = webgeocoder.get_html_from_dataframe()
        print(result_html)
        return render_template('index.html', result_html=result_html, btn='download.html', file_name=webgeocoder.get_uploaded_filename())
    except Exception as exception:
        print(exception)
        return render_template('index.html', result_html=str(exception))
    # return statements do not seem to be return'ing out of function, in this sequence of try...except
    # - catch/raise errors elsewhere eg in WebGeocoder

@app.route('/map')
def map():
    return render_template('map.html')

    # TODO: find out correct exception types in each case and add a catch accordingly

global webgeocoder
webgeocoder = WebGeocoder()


if __name__ == '__main__':
    app.run(debug=True)
    ''' if this app were run by name, eg, to do SQLAlchemy model instantiation,
     then __main__ would not be the instance name '''

