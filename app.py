from flask import Flask, request, render_template
from PIL import Image
import os
from geo_utils import get_geo_tag, get_location_name, update_geo_tag  # Import your geo_utils functions

app = Flask(__name__)

# Route to handle the form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Process the image to get geotag
        try:
            # Get the current geotag of the image
            lat_before, lng_before = get_geo_tag(file_path)
            location_before = "Unknown location"
            
            if lat_before and lng_before:
                # Get the location name using lat/lng
                location_before = get_location_name(lat_before, lng_before)

            # After the user updates the geotag, capture new latitude and longitude
            lat_after = float(request.form['latitude'])
            lng_after = float(request.form['longitude'])
            location_after = get_location_name(lat_after, lng_after)

            # Update the geotag of the image with new latitude and longitude
            updated_image_path = os.path.join("uploads", "updated_" + file.filename)
            update_geo_tag(file_path, updated_image_path, lat_after, lng_after)

            # Render the result page with the geotag details
            return render_template('result.html',
                                   lat_before=lat_before, lng_before=lng_before, location_before=location_before,
                                   lat_after=lat_after, lng_after=lng_after, location_after=location_after,
                                   original=file.filename, updated="updated_" + file.filename)

        except Exception as e:
            return str(e)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
