import pandas
from geopy.geocoders import Nominatim

class WebGeocoder():

    uploaded_file = None        # property/class variable
    dataframe = None

    def __init__(self):
        """ constructor for WebGeocoder """

    def geocode_dataframe(self):
        if not isinstance(self.dataframe, pandas.DataFrame):                # https://stackoverflow.com/a/14809149
            raise Exception('Dataframe not yet initialised: import CSV to proceed')
        if 'address' not in self.dataframe.columns and 'Address' not in self.dataframe.columns:
            raise Exception('No Address or address column in CSV')
        self.dataframe.columns = map(str.lower, self.dataframe.columns)
        # series/column names to lower case - https://stackoverflow.com/a/36362607

        nom = Nominatim()
        self.dataframe['Latitude'], self.dataframe['Longitude'] = zip(*self.dataframe['address'].apply(nom.geocode).apply(lambda record: (record.latitude, record.longitude) ))
        # lambda assignation of lat/lng in geocoded dataframe - https://stackoverflow.com/a/31414616
        # unpacking lat/lng tuple using zip and * https://stackoverflow.com/a/43009150

        self.dataframe.columns = map(str.title, self.dataframe.columns)
        # set to initial - really should restore to whatever was previous case (TODO)

    def download_csv_from_dataframe(self):
        try:
            return self.dataframe.to_csv(index=False)
        except Exception as exception:
            print(exception)
            return exception

    def get_html_from_dataframe(self):
        try:
            return self.dataframe.to_html(classes='geocoded')
        except Exception as exception:
            print(str(exception))
            return exception

    def get_uploaded_file(self):
        return self.uploaded_file

    def get_uploaded_filename(self):
        try:
            print('Name of file uploaded: ' + self.uploaded_file.filename)
            return self.uploaded_file.filename
        except:
            print('Name unavailable as this upload is not of a requests.file type')
        return

    def process_csv_to_dataframe(self, file):
        self.dataframe = pandas.read_csv(file)
        print(self.dataframe)
        return

    # def upload(self, file):
    #     try:
    #         print('Name of file uploaded: ' + file.filename)
    #     except AttributeError:
    #         print('This upload is not of a requests.file type')
    #     self.uploaded_file = file
    #     print('Name of file now uploaded: ' + self.uploaded_file.filename)
    #     return

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
        return
