from PIL import Image
import piexif

def deg_to_dms_rational(deg_float):
    """Convert decimal degrees to degrees, minutes, seconds in rational format."""
    deg = int(deg_float)
    min_float = (deg_float - deg) * 60
    minute = int(min_float)
    sec_float = (min_float - minute) * 60
    return ((deg, 1), (minute, 1), (int(sec_float * 100), 100))

def change_geo_tag(image_path, output_path, lat, lng):
    img = Image.open(image_path)
    
    # Safely load EXIF data
    exif_dict = {}
    try:
        exif_dict = piexif.load(img.info['exif'])
    except KeyError:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

    # Prepare GPS IFD
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if lat >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: deg_to_dms_rational(abs(lat)),
        piexif.GPSIFD.GPSLongitudeRef: 'E' if lng >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: deg_to_dms_rational(abs(lng)),
    }

    # Update EXIF data
    exif_dict['GPS'] = gps_ifd
    exif_bytes = piexif.dump(exif_dict)

    # Save the new image with updated EXIF
    img.save(output_path, "jpeg", exif=exif_bytes)
    print(f"Geo-tag updated to ({lat}°, {lng}°) and saved as '{output_path}'")


# Example Usage:
# image_path = "IMG20250221123356.jpg"
# output_path = "output/"+image_path  # Relative to your project directory
# latitude = 23.0775              # Latitude: 23.0775° N
# longitude = 76.8513             # Longitude: 76.8513° E

# change_geo_tag(image_path, output_path, latitude, longitude)
