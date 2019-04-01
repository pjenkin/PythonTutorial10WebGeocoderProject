import pandas
from geopy import distance
from geopy.geocoders import Nominatim
import geopy
import numpy as np
np.set_printoptions(threshold=np.inf)       # print out all of numpy array

class WebGeocoder():

    uploaded_file = None        # property/class variable - _io.TextIOWrapper from file input upload
    dataframe = None
    reference_address = None

    def __init__(self):
        """ constructor for WebGeocoder """
        pass

    def calculate_distance_from_reference_location(self, address):
        """ take a location/address (e.g. 'San Farncisco') and add/populate a dataframe column """
        """ with km distances from that location """
        try:
            print('in calculate_distance_from_reference_location')
            self.set_reference_address(address)
            reference_latitude, reference_longitude = self.get_reference_address_location()    # tuple of lat,lng
            reference_location = (reference_latitude, reference_longitude)
            # NB pandas won't allow assignation of tuples to columns  https://stackoverflow.com/a/34811984

            # awkward using tuples with a dataframe - iterating for the mo - could do this maybe with a lambda function
            for index, row in self.dataframe.iterrows():       # https://stackoverflow.com/a/16476974
                target_location = (row['latitude'], row['longitude'])
                reference_distance = distance.distance(reference_location, target_location).kilometers
                self.dataframe.loc[index, 'reference_distance'] = reference_distance
                # index and loc within iterrows loop https://stackoverflow.com/a/25478896

            with pandas.option_context('display.max_rows', None, 'display.max_columns', None):
                print(self.dataframe)       # diagnostic - print whole dataframe - https://stackoverflow.com/a/30691921

            print('added reference_distance data')
        except Exception as exception:
            print(exception)

    def geocode_dataframe(self):
        """ Use address column of dataframe to try to add columns with Lat/Lng """
        if not isinstance(self.dataframe, pandas.DataFrame):                # https://stackoverflow.com/a/14809149
            raise Exception('Dataframe not yet initialised: import CSV to proceed')
        if 'address' not in self.dataframe.columns and 'Address' not in self.dataframe.columns:
            print('Look out!')
            print(self.dataframe)
            raise Exception('No Address or address column in CSV')
        self.dataframe.columns = map(str.lower, self.dataframe.columns)
        # series/column names to lower case - https://stackoverflow.com/a/36362607

        nom = Nominatim(user_agent='pnj-python-web-geocoder')
        # user-agent string as app name as per Nominatim instructions
        geopy.geocoders.options.default_user_agent = "pnj-python-web-geocoder"
        self.dataframe['Latitude'], self.dataframe['Longitude'] = zip(*self.dataframe['address'].apply(nom.geocode).apply(lambda record: (record.latitude, record.longitude) ))
        # lambda assignation of lat/lng in geocoded dataframe - https://stackoverflow.com/a/31414616
        # unpacking lat/lng tuple using zip and * https://stackoverflow.com/a/43009150

        self.dataframe.columns = map(str.title, self.dataframe.columns)
        # set to initial - really should restore to whatever was previous case (TODO)

    def download_csv_from_dataframe(self):
        """ obtain CSV file from dataframe's data """
        try:
            return self.dataframe.to_csv(index=False)
        except Exception as exception:
            print(exception)
            return exception

    def get_dataframe(self):
        """ get this WebGeocoder instance's dataframe """
        return self.dataframe


    def get_html_from_dataframe(self):
        """ get an HTML representation of this WebGeocoder instance's dataframe """
        try:
            return self.dataframe.to_html(classes='geocoded')
        except Exception as exception:
            print(str(exception))
            return exception

    def get_reference_address(self):
        """ get the address currently used as reference address by the WebGeocoder instance """
        return self.reference_address

    def get_reference_address_location(self):
        """ get Lat/Lng coordinates for the address currently used as reference address by the WebGeocoder instance """
        from geopy.geocoders import Nominatim as nom        # https://geopy.readthedocs.io/en/stable/
        geolocator = nom(user_agent='pnj-python-web-geocoder')
        address, (latitude, longitude) = geolocator.geocode(self.get_reference_address())
        return (latitude, longitude)                     # return just the lat & lng, in a tuple
        # i.e. coordinates

    def get_uploaded_file(self):
        """ get the file which has been uploaded by user """
        return self.uploaded_file

    def get_uploaded_filename(self):
        """ get the name of the file which has been uploaded by user """
        try:
            print('Name of file uploaded: ' + self.uploaded_file.filename)
            return self.uploaded_file.filename
        except:
            print('Name unavailable as this upload is not of a requests.file type')
        return

    def process_csv_to_dataframe(self, file):
        """ populate the WebGeocoder's dataframe using CSV file """
        self.dataframe = pandas.read_csv(file)
        print(self.dataframe)
        return

    def set_reference_address(self, address):
        """ set the address currently to be used as reference address by the WebGeocoder instance """
        self.reference_address = address

    def upload_csv(self, file):
        """ assign a CSV file to the dataframe of this WebGeocoder instance """
        try:
            print('Name of file uploaded: ' + file.filename)
        except AttributeError:
            print('This upload is not of a requests.file type')

        if file.filename == '':
            raise Exception('No file uploaded')
        # I don't know why the try...except in '\download' seems disabled,
        # but this will catch any non-existent filenames uploaded

        self.uploaded_file = file
        try:
            dataframe = pandas.read_csv(file)
            self.dataframe = dataframe
            print(dataframe)
        except Exception as exception:
            print('Error in CSV import' + str(exception))
        return

