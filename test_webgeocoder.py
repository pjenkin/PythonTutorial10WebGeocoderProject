import unittest
from webgeocoder import WebGeocoder
# from flask_testing import TestCase
from flask import Flask
import pandas
from io import TextIOWrapper as _TextIOWrapper, BytesIO, StringIO       # file/IO forming https://stackoverflow.com/a/44764457
from app import app         # for testing the Flask app    https://damyanon.net/post/flask-series-testing/
import re                   # regular expressions

# https://docs.python.org/3/library/unittest.html
# https://pythonhosted.org/Flask-Testing/


# enable name attribute/property on mock'd file  https://github.com/python/typeshed/issues/598#issuecomment-253018502
class TextIOWrapper(_TextIOWrapper):        # subclass/inherit from alias'd real TextIOWrapper; tag on a name attribute
    name = ''
    filename = ''


class WebGeocoderDataTestCase(unittest.TestCase):


    def setUp(self):
        self.webgeocoder = WebGeocoder()
        self.app = app.test_client()



    # def tearDown(self):
    #     self.webgeocoder.dispose()      # no dispose method yet


    def test_server_is_up_and_running(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        print(str.upper('got to end of server test'))



    # NB python -m unittest webgeocoder_tests
    def test_downloaded_filename(self):
        """test that downloaded filename from WebGeocoder is correct"""

        # arrange - (i) set dataframe, and (ii) filename of webgeocoder (non-private members)
        # act - (ii)  download a CSV, (iv) record CSV's filename (if poss)
        # assert - (v) that filenames (ii) and (iv) are equal
        # NB uses HTTP to actually POST and then request by download a file from Flask server


        # arrange - (i) set dataframe, and (ii) filename of webgeocoder (non-private members)
        self.webgeocoder = WebGeocoder()

        csv_string = '''ID,address,People
        1,44 Mead Crescent Southampton, 4
        2, 67 Trevingey Road, 3
        3, 66 Mount Pleasant Road Camborne,2'''
        test_file_name = 'test_file.csv'
        # https://stackoverflow.com/a/33071581
        str_bytes = bytes(csv_string, 'utf-8')

        data = {'name':'some name'}
        data['file_name']=(BytesIO(str_bytes), test_file_name)
        # https: // stackoverflow.com / a / 35712344

        self.app.post('/', data=data, content_type='multipart/form-data')
        # POST to index, using bytes of CSV-like content


        # TODO:  tidy up without completely losing interesting bits


        # act - (ii)  download a CSV, (iv) record CSV's filename (if poss)


        downloaded_file = self.app.get('/download')
        # regex to capture any characters after 'filename=' https://stackoverflow.com/a/31805472

        downloaded_filename = re.findall('filename=(.+)', downloaded_file.headers['Content-Disposition'])[0]

        # assert names of download and upload (with 'geocoded_' prefix) are equal - could remove string
        self.assertEqual(downloaded_filename, 'geocoded_' + test_file_name)
        print(str.upper('This is the end of test_downloaded_filename which may or may not be working'))





    def test_uploaded_filename(self):
        """test file upload name is correct"""

        # arrange - (i) set up a file (actually io.TextIOWrapper) with name
        # act - (ii) upload (iii)  record CSV's filename (if poss)
        # assert - (iv) that filenames (i) and (iii) (of uploaded file) are equal
        # NB does not use HTTP, file simulated upload only to WebGeocoder instance object

        # possibly should not use upload_csv , or maybe should...?

        # arrange - (i) set dataframe, and (ii) filename of webgeocoder (non-private members)
        self.webgeocoder = WebGeocoder()

        test_file_name = 'test_file.csv'
        output = BytesIO()  # TextIOWrapper as per file input upload - https://stackoverflow.com/a/44764457
        file = TextIOWrapper(output, encoding='cp1252', line_buffering=True)
        file.write('\nSome dummy text not actually used.\n')
        self.webgeocoder.uploaded_file = file  # set mock-uploaded file to appropriate object
        self.webgeocoder.uploaded_file.filename = test_file_name

        print('***filename:  ' + self.webgeocoder.uploaded_file.filename)
        print('***filename:  ' + self.webgeocoder.get_uploaded_filename())

        # act -  record CSV's filename (if poss)
        # downloaded_file = self.webgeocoder.download_csv_from_dataframe()
        # downloaded_filename = downloaded_file.headers['Content-Disposition'].split('=')[-1]  # see sample data
        self.webgeocoder.upload_csv(file)       # upload file
        uploaded_filename = self.webgeocoder.get_uploaded_filename()


        # assert - (iv) that filenames (i) and (iii) (of uploaded file) are equal
        self.assertEqual(uploaded_filename, test_file_name)
        print(str.upper('got here after assertion that uploaded filename is the same as test filename'))



def webgeocoder_data_suite():
    suite = unittest.TestSuite()
    suite.addTest(WebGeocoderDataTestCase('test_downloaded_filename'))
    return suite

if __name__ == '__main__':
    runner = unittest.TestRunner()
    runner.run(webgeocoder_data_suite())
