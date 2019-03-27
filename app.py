from flask import Flask, render_template, request, flash
from webgeocoder import WebGeocoder

app = Flask(__name__)


# class WebGeocoder():
#
#     def __init__(self):
#         """ constructor for WebGeocoder """
#         if __name__ == '__main__':
#             app.run(debug=True)
#             ''' if this app were run by name, eg, to do SQLAlchemy model instantiation,
#              then __main__ would not be the instance name '''
#
#     def upload(self, file):
#         # flash(file.filename)
#         print(file.filename)
#         pass



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success_table', methods=['POST'])
def success_table():
    try:
        upload_file = request.files['file_name']
    except Exception as exception:
        return render_template('success-table.html', result_html=str(exception))
    # webgeocoder.upload(upload_file)
    try:
        webgeocoder.upload_csv(upload_file)
    except Exception as exception:
        return render_template('success-table.html', result_html=str(exception))
    # print(webgeocoder.html_from_dataframe())
    try:
        webgeocoder.geocode_dataframe()
    except Exception as exception:
        return render_template('success-table.html', result_html=str(exception))
    try:
        result_html = webgeocoder.html_from_dataframe()
        print(result_html)
        return render_template('success-table.html', result_html=result_html)
    except Exception as exception:
        return render_template('success-table.html', result_html=str(exception))
    # print(webgeocoder.html_from_dataframe())
    # print('should have printed result_html')




    # TODO: find out correct exception types in each case and add a catch accordingly

global webgeocoder
webgeocoder = WebGeocoder()


if __name__ == '__main__':
    app.run(debug=True)
    ''' if this app were run by name, eg, to do SQLAlchemy model instantiation,
     then __main__ would not be the instance name '''

