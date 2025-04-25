from PIL import Image
import piexif
from geopy.geocoders import Nominatim

def deg_to_dms_rational(deg_float):
    deg = int(deg_float)
    min_float = (deg_float - deg) * 60
    minute = int(min_float)
    sec_float = (min_float - minute) * 60
    return ((deg, 1), (minute, 1), (int(sec_float * 100), 100))

def get_geo_tag(image_path):
    try:
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info['exif'])
        gps_info = exif_dict.get('GPS', {})
        
        if not gps_info:
            return None, None
        
        lat = gps_info.get(piexif.GPSIFD.GPSLatitude)
        lat_ref = gps_info.get(piexif.GPSIFD.GPSLatitudeRef)
        lng = gps_info.get(piexif.GPSIFD.GPSLongitude)
        lng_ref = gps_info.get(piexif.GPSIFD.GPSLongitudeRef)

        if lat and lng:
            lat_deg = sum(x[0]/x[1] for x in lat)
            lng_deg = sum(x[0]/x[1] for x in lng)
            if lat_ref == b'S': lat_deg *= -1
            if lng_ref == b'W': lng_deg *= -1
            return lat_deg, lng_deg
    except Exception as e:
        return None, None

def update_geo_tag(image_path, output_path, lat, lng):
    img = Image.open(image_path)
    try:
        exif_dict = piexif.load(img.info['exif'])
    except KeyError:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: deg_to_dms_rational(abs(lat)),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if lng >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: deg_to_dms_rational(abs(lng)),
    }

    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)
    img.save(output_path, "jpeg", exif=exif_bytes)

def get_location_name(lat, lng):
    try:
        geolocator = Nominatim(user_agent="geoapp")
        location = geolocator.reverse((lat, lng), language='en')
        return location.address if location else "Unknown location"
    except Exception as e:
        return f"Error finding location: {e}"
