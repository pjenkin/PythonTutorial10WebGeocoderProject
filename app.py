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
    upload_file = request.files['file_name']
    webgeocoder.upload(upload_file)
    return render_template('success-table.html')



global webgeocoder
webgeocoder = WebGeocoder()


if __name__ == '__main__':
    app.run(debug=True)
    ''' if this app were run by name, eg, to do SQLAlchemy model instantiation,
     then __main__ would not be the instance name '''

