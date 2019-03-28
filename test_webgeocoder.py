import unittest
from webgeocoder import WebGeocoder
# from flask_testing import TestCase
from flask import Flask
import pandas
from io import TextIOWrapper as _TextIOWrapper, BytesIO       # file/IO forming https://stackoverflow.com/a/44764457
from app import app         # for testing the Flask app    https://damyanon.net/post/flask-series-testing/

# https://docs.python.org/3/library/unittest.html
# https://pythonhosted.org/Flask-Testing/


# enable name attribute/property on mock'd file  https://github.com/python/typeshed/issues/598#issuecomment-253018502
class TextIOWrapper(_TextIOWrapper):        # subclass/inherit from alias'd real TextIOWrapper; tag on a name attribute
    name = ''


class WebGeocoderDataTestCase(unittest.TestCase):


    def setUp(self):
        self.webgeocoder = WebGeocoder()
        self.app = app.test_client()



    # def tearDown(self):
    #     self.webgeocoder.dispose()      # no dispose method yet


    def test_server_is_up_and_running(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        print('got to end of server test')


    # NB python -m unittest webgeocoder_tests
    def test_downloaded_filename(self):
        """test that downloaded filename from WebGeocoder is correct"""

        # arrange - (i) set dataframe, and (ii) filename of webgeocoder (non-private members)
        # act - (ii)  download a CSV, (iv) record CSV's filename (if poss)
        # assert - (v) that filenames (ii) and (iv) are equal


        # arrange - (i) set dataframe, and (ii) filename of webgeocoder (non-private members)
        self.webgeocoder = WebGeocoder()

        # https://pbpython.com/pandas-list-dict.html
        test_data = [('ID', [1, 2, 3]),
            ('name', ['First x', 'Second x', 'Third x']),
            ('Value_A', [10, 20, 30]),
            ('Value_B', [12, 24, 36]),
            ('Value_C', [8, 14, 96])
            ]
        dataframe = pandas.DataFrame.from_items(test_data)
        self.webgeocoder.dataframe = dataframe
        output = BytesIO()      # TextIOWrapper as per file input upload - https://stackoverflow.com/a/44764457
        file = TextIOWrapper(output, encoding='cp1252', line_buffering=True)
        file.write('\nSome dummy text not actually used.\n')
        test_file_name = 'test_file.csv'
        file.name = test_file_name
        self.webgeocoder.uploaded_file = file   # set mock-uploaded file to appropriate object
        # self.webgeocoder.uploaded_file.filename = test_file_name

        # act - (ii)  download a CSV, (iv) record CSV's filename (if poss)
        downloaded_file = self.webgeocoder.download_csv_from_dataframe()
        downloaded_filename = downloaded_file.headers['Content-Disposition'].split('=')[-1]     # see sample data
        print(downloaded_filename)
        print(test_file_name)

        # sample data: <Response 587 bytes [200 OK]>
        # attachment; filename=geocoded_supermarkets_upper_case_Address.csv

        # assert names of download and upload are equal
        self.assertEqual(downloaded_filename, test_file_name)





    def test_uploaded_filename(self):
        """test file upload name is correct"""

        # arrange - (i) set up a file (actually io.TextIOWrapper) with name
        # act - (ii) upload (iii)  record CSV's filename (if poss)
        # assert - (iv) that filenames (i) and (iii) (of uploaded file) are equal

        # possibly should not use upload_csv , or maybe should...?

        # arrange - (i) set dataframe, and (ii) filename of webgeocoder (non-private members)
        self.webgeocoder = WebGeocoder()

        # https://pbpython.com/pandas-list-dict.html
        # test_data = [('ID', [1, 2, 3]),
        #              ('name', ['First x', 'Second x', 'Third x']),
        #              ('Value_A', [10, 20, 30]),
        #              ('Value_B', [12, 24, 36]),
        #              ('Value_C', [8, 14, 96])
        #              ]
        # dataframe = pandas.DataFrame.from_items(test_data)
        # self.webgeocoder.dataframe = dataframe
        test_file_name = 'test_file.csv'
        output = BytesIO()  # TextIOWrapper as per file input upload - https://stackoverflow.com/a/44764457
        file = TextIOWrapper(output, encoding='cp1252', line_buffering=True)
        file.write('\nSome dummy text not actually used.\n')
        self.webgeocoder.uploaded_file = file  # set mock-uploaded file to appropriate object
        self.webgeocoder.uploaded_file.filename = test_file_name



        # act -  record CSV's filename (if poss)
        # downloaded_file = self.webgeocoder.download_csv_from_dataframe()
        # downloaded_filename = downloaded_file.headers['Content-Disposition'].split('=')[-1]  # see sample data
        self.webgeocoder.upload_csv(file)       # upload file
        uploaded_filename = self.webgeocoder.get_uploaded_filename()


        # assert - (iv) that filenames (i) and (iii) (of uploaded file) are equal
        self.assertEqual(uploaded_filename, test_file_name)
        print('got here')

    #     # arrange - instantiate a file
    #     # act - pass to GeoWebcoder's upload method
    #     # assert file's
    #
    #     webgeocoder = WebGeocoder()
    #
    #     test_file_name = 'test-file.txt'
    #
    #     test_file = open(test_file_name, 'w')
    #     test_file.write('Hello, here is a line of text text.')
    #     test_file.close()
    #     print(test_file)
    #     with open(test_file_name, 'r') as test_file:
    #         # x for exclusive file formation - opens or makes if non-existent https://stackoverflow.com/a/43081892
    #         uploaded_file_name = webgeocoder.upload(test_file)
    #
    #     print(uploaded_file_name)
    #     print(webgeocoder.get_uploaded_filename())
    #
    #     assert webgeocoder.get_uploaded_filename() == test_file_name
    #     # end of test

    # def test_uploaded_file_contents(self):
    #     """test file upload name is correct"""
    #     # arrange - instantiate a file
    #     # act - pass to GeoWebcoder's upload method
    #     # assert file's
    #
    #     webgeocoder = WebGeocoder()
    #
    #     test_file_name = 'test-file.txt'
    #     test_string = 'Hello, here is a line of test text.'
    #
    #     test_file = open(test_file_name, 'w')
    #     test_file.write(test_string)
    #     test_file.close()
    #     print(test_file)
    #     with open(test_file_name, 'r') as test_file:
    #         # x for exclusive file formation - opens or makes if non-existent https://stackoverflow.com/a/43081892
    #         uploaded_file_name = webgeocoder.upload(test_file)
    #
    #     print(uploaded_file_name)
    #     print(webgeocoder.get_uploaded_filename())
    #
    #     assert webgeocoder.get_uploaded_filename() == test_file_name
    #     # end of test


# # Flask tests should be in separate file
# class SimpleTest(TestCase):
#     def create_app(self):
#         app = Flask(__name__)
#         app.config['TESTING'] = True
#         return app
#
#     def test_server_is_running_ok(self):
#         response = urllib2.urlopen(self.get_server_url())
#         self.assertEqual(response.code, 200)


def webgeocoder_data_suite():
    suite = unittest.TestSuite()
    suite.addTest(WebGeocoderDataTestCase('test_downloaded_filename'))
    return suite

if __name__ == '__main__':
    runner = unittest.TestRunner()
    runner.run(webgeocoder_data_suite())
