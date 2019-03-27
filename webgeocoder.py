import pandas
from geopy.geocoders import Nominatim

class WebGeocoder():

    uploaded_file = None        # property/class variable
    dataframe = None

    def __init__(self):
        """ constructor for WebGeocoder """

    def upload(self, file):
        try:
            print('Name of file uploaded: ' + file.filename)
        except AttributeError:
            print('This upload is not of a requests.file type')
        self.uploaded_file = file

    def upload_csv(self, file):
        try:
            print('Name of file uploaded: ' + file.filename)
        except AttributeError:
            print('This upload is not of a requests.file type')
        self.uploaded_file = file
        try:
            dataframe = pandas.read_csv(file)
            self.dataframe = dataframe
            print(dataframe)
        except Exception as exception:
            print('Error in CSV import' + str(exception))

