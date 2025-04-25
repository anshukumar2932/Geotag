from flask import Flask, render_template, request, redirect, url_for, session
import os
from geo_utils import get_geo_tag, update_geo_tag, get_location_name

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        lat = float(request.form['latitude'])
        lng = float(request.form['longitude'])

        if file and allowed_file(file.filename):
            filename = file.filename
            path_original = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_original)

            lat_before, lng_before = get_geo_tag(path_original)
            path_updated = os.path.join(app.config['UPLOAD_FOLDER'], f"updated_{filename}")
            update_geo_tag(path_original, path_updated, lat, lng)
            lat_after, lng_after = get_geo_tag(path_updated)

            # Reverse geocode
            location_before = get_location_name(lat_before, lng_before) if lat_before else "No location found"
            location_after = get_location_name(lat_after, lng_after)

            # Store in session
            session.update({
                'original': path_original,
                'updated': path_updated,
                'lat_before': lat_before,
                'lng_before': lng_before,
                'lat_after': lat_after,
                'lng_after': lng_after,
                'location_before': location_before,
                'location_after': location_after
            })

            return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():
    return render_template('result.html', **session)

if __name__ == '__main__':
    app.run(debug=True)
