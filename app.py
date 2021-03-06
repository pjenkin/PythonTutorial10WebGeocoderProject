from flask import Flask, render_template, request, send_file, make_response
from webgeocoder import WebGeocoder
import werkzeug   # TODO - is this needed for safe strings in filenames?
# from flask import session
# from flask_socketio import SocketIO, emit
# from flask.ext.login import current_user, logout_user

app = Flask(__name__)

@app.route('/atlas')
def atlas():
    import folium
    import pandas

    # I have not written the code in an MVC way here
    map_html = ''

    dataframe = webgeocoder.get_dataframe()
    if isinstance(dataframe, pandas.DataFrame):  # https://stackoverflow.com/a/14809149
        dataframe.columns = map(str.lower, dataframe.columns)
    else:
        map_html = '<p>Sorry, no geographical data to map yet. (Try uploading a CSV file with addresses.)</p>'

    if map_html == '':
        if 'latitude' not in dataframe.columns or 'longitude' not in dataframe.columns:
            map_html = '<p>Sorry, no geographical data to map yet. (Try uploading a CSV file with addresses.)</p>'
        else:
            # atlas = folium.Map(location=[51, -4], zoom_start=7, tiles='mapquestopen', attr='http://open.mapquest.co.uk/')
            atlas = folium.Map(location=[51, -4], zoom_start=7, tiles='openstreetmap', attr='http://wiki.openstreetmap.org/wiki/Tiles')
            # atlas = folium.Map(location=[51, -4], zoom_start=7, tiles='Mapbox bright')
            # tiles attribution - https://stackoverflow.com/a/52172546

            csv_feature_group = folium.FeatureGroup('Uploaded CSV Markers')
            csv_feature_group.add_to(atlas)

            popup_html = """
            <strong>Name</strong>: %s<br>
            <strong>Employees</strong>: %s<br>
            """


            # TODO: for every column which isn't lat/lng, record value in a dictionary & use on marker
            for index, row in dataframe.iterrows():
                if 'name' in row:
                    name = row['name']
                if 'employees' in row:
                    employees = row['employees']
                if 'url' in row:
                    url = row['employees']

                popup_iframe = folium.IFrame(html=popup_html % (name, employees), width=120, height=120)
                folium.CircleMarker(location=[row['latitude'], row['longitude']], popup=folium.Popup(popup_iframe),
                                    color='red', radius=6, fill=True, opacity=0.8).add_to(csv_feature_group)
                # TODO - could adjust radius and colour as per number of employees

                atlas.fit_bounds(csv_feature_group.get_bounds())        # fit map to markers


            layer_control = folium.LayerControl().add_to(atlas)

            map_html = atlas._repr_html_()
            # ._repr_html_()  to render map HTML in iframe   -  .get_root().render() to render whole page in HTML
            # - https://github.com/python-visualization/folium/issues/781#issuecomment-347907408
    print('rendering map?')
    print(map_html)

    inline_disability_flag_property = 'style="pointer-events:auto;color: #444;font-style:normal;opacity:1;"'
    # all pages safely navigable once data has been loaded - could use global constant

    # return render_template('atlas.html', map_html=map_html)
    return render_template('atlas.html', map_html=map_html,
                           inline_disability_flag_property=inline_disability_flag_property)


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
    import pandas
    from bokeh.plotting import figure, show, output_file
    # from bokeh.models.annotations import Title
    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.models import ColumnDataSource, LabelSet

    # I have not written the code in an MVC way here - mostly Model code below
    # this could do with being in a function(s) of its own

    error_html = ''

    dataframe = webgeocoder.get_dataframe()
    if isinstance(dataframe, pandas.DataFrame):  # https://stackoverflow.com/a/14809149
        dataframe.columns = map(str.lower, dataframe.columns)
    else:
        error_html = '<p>Sorry, no uploaded data to chart yet. (Try uploading a CSV file with addresses.)</p>'

    if error_html == '':
        if 'latitude' not in dataframe.columns or 'longitude' not in dataframe.columns:
            error_html = '<p>Sorry, no geographical data to map yet. (Try uploading a CSV file with addresses.)</p>'
        elif 'name' not in dataframe.columns:
            error_html = '<p>Sorry, in the data there is no column called <em>Name</em> or <em>name</em> - we need this column in the CSV please.</p>'
            # wade through & respond to problems 1 at a time - TODO notify of all missing fields at once
        elif 'employees' not in dataframe.columns:
            error_html = '<p>Sorry, in the data there is no column called <em>Employees</em> or <em>employees</em> - we need this column in the CSV please.</p>'
        else:
            # error_html = 'going to try to build a chart'
            webgeocoder.calculate_distance_from_reference_location('San Francisco, CA, USA')
            # find the coordinates for centre of San Francisco
            # for each row in dataframe, use lat/lng to calculate distance from SF centre
            # add/populate a column with distance

            fig = figure(width=500, height=500, sizing_mode='stretch_both')
            dataframe = webgeocoder.get_dataframe()
            dataframe.columns = map(str.lower, dataframe.columns)
            fig.scatter(x=dataframe['reference_distance'], y=dataframe['employees'], size=25)
            # instantiate a x/y/scatter plot
            # make the distance x axis, make the number of employees y axis




            fig.title.text = 'Distance from central San Francisco vs number of employees'
            fig.grid.grid_line_alpha = 0.2
            fig.xaxis.axis_label = 'Distance from central San Francisco (km)'
            fig.yaxis.axis_label = 'Number of employees'

            source = ColumnDataSource(data=dict(reference_distance=webgeocoder.get_dataframe()['reference_distance'],
                                        employees=webgeocoder.get_dataframe()['employees'],
                                        name=webgeocoder.get_dataframe()['name']
                                        ))
            labels = LabelSet(x='reference_distance', y='employees', text='name', x_offset=0, y_offset=5,
                              source=source, render_mode='canvas')

            fig.add_layout(labels)

            # could add citation as Label with details to print source of data

            # check output/show
            # output_file('CSV-scatter.html')
            # show(fig)
            # do the doings with getting on the page

            script1, div1 = components(fig)
            cdn_javascript = CDN.js_files[0]
            cdn_css = CDN.css_files[0]


    # webgeocoder_dict = webgeocoder.get_dataframe().to_dict()

    inline_disability_flag_property = 'style="pointer-events:auto;color: #444;font-style:normal;opacity:1;"'
    # all pages safely navigable once data has been loaded - could use global constant

    # return render_template('graph.html', error_html=error_html)
    return render_template('graph.html', error_html=error_html, script1=script1,
                           div1=div1, cdn_css=cdn_css, cdn_javascript=cdn_javascript,
                           inline_disability_flag_property=inline_disability_flag_property)

@app.route('/', methods=['GET'])
def index():
    import pandas

    # TODO could refector some of this into a function for use in both '/' GET and POST

    # avoid (visibly) persisting data if user has just landed on home/root/index page
    if isinstance(request.referrer, str):
        referrer_last_part = request.referrer.split('/')[-1]
    else:
        referrer_last_part = str(None)

    if referrer_last_part == 'atlas' or referrer_last_part == 'graph':
        # inline_visibility_flag_tag = 'class="currently-visible"'
        inline_visibility_flag_property = 'style="visibility: visible;"'
        inline_disability_flag_property = 'style="pointer-events:auto;color: #444;font-style:normal;opacity:1;"'
        # use inline style to avoid messing up any class definitions
    else:
        inline_visibility_flag_property = ''
        inline_disability_flag_property = ''


    if isinstance(webgeocoder.get_dataframe(), pandas.DataFrame):
        try:
            result_html = webgeocoder.get_html_from_dataframe()
            print(result_html)
            return render_template('index.html', result_html=result_html, btn='download.html',
                                   file_name=webgeocoder.get_uploaded_filename(),
                                   inline_visibility_flag_property=inline_visibility_flag_property,
                                   inline_disability_flag_property=inline_disability_flag_property)

        except Exception as exception:
            print(exception)
            return render_template('index.html', result_html=str(exception))


    # return render_template('index.html')
    return render_template('index.html', inline_visibility_flag_property=inline_visibility_flag_property,
                           inline_disability_flag_property=inline_disability_flag_property)
    # Issue: after navigating away from page, if dataframe populated, no table shown: could check for dataframe on GET
    # ... should only repopulate page if coming from graph or chart pages

@app.route('/', methods=['POST'])
def index_success_table():


    try:
        upload_file = request.files['file_name']
    except Exception as exception:
        print(exception)
        return render_template('index.html', result_html=str(exception))
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
        inline_visibility_flag_property = 'class="currently-visible"'
        inline_disability_flag_property = 'style="pointer-events:auto;color: #444;font-style:normal;opacity:1;"'
        return render_template('index.html', result_html=result_html, btn='download.html',
                               file_name=webgeocoder.get_uploaded_filename(),
                               inline_visibility_flag_property=inline_visibility_flag_property,
                               inline_disability_flag_property=inline_disability_flag_property
                               )
    except Exception as exception:
        print(exception)
        return render_template('index.html', result_html=str(exception))
    # return statements do not seem to be return'ing out of function, in this sequence of try...except
    # - catch/raise errors elsewhere eg in WebGeocoder
    # this code not very DRY

    # TODO: find out correct exception types in each case and add a catch accordingly

global webgeocoder
webgeocoder = WebGeocoder()


if __name__ == '__main__':
    app.run(debug=True)
    ''' if this app were run by name, eg, to do SQLAlchemy model instantiation,
     then __main__ would not be the instance name '''


