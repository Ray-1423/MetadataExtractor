import os
import exifread
from PyPDF2 import PdfReader
from datetime import datetime
import importlib.metadata
import pprint

# function to extract from an image
def extractFromImage(file_path):
    metadata = {
        'name': os.path.basename(file_path),
        'size': os.path.getsize(file_path),
        'created_time': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
        'modified_time': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
        'exif': {}
    }
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            metadata['exif'] = {tag: str(val) for tag, val in tags.items()}
            gps_lat = next((val for tag, val in tags.items() if "GPSLatitude" in tag), None)
            gps_lat_ref = next((val for tag, val in tags.items() if "GPSLatitudeRef" in tag), None)
            gps_lon = next((val for tag, val in tags.items() if "GPSLongitude" in tag), None)
            gps_lon_ref = next((val for tag, val in tags.items() if "GPSLongitudeRef" in tag), None)
            try:
                if gps_lat and gps_lat_ref and gps_lon and gps_lon_ref:
                    lat = convert_gps_to_degrees(gps_lat, gps_lat_ref)
                    lon = convert_gps_to_degrees(gps_lon, gps_lon_ref)
                    metadata['gps_coordinates'] = {'latitude': lat, 'longitude': lon}
                else:
                    metadata['gps_coordinates'] = "No GPS data found"
            except:
                metadata['gps_coordinates'] = "GPS data may exist but cood not be coordinatized (read through exif data)"
    except Exception as e:
        return f"Exifread error: {e}"
    
    return metadata

# helper to convert gps to degrees
def convert_gps_to_degrees(value, ref):
    # value is a list like [34, 0, 0] or [34/1, 0/1, 0/1]
    def to_float(ratio):
        return float(str(ratio).split("/")[0]) / float(str(ratio).split("/")[1]) if "/" in str(ratio) else float(ratio)
    d = to_float(value.values[0])
    m = to_float(value.values[1])
    s = to_float(value.values[2])
    coord = d + (m / 60.0) + (s / 3600.0)
    if ref.values != 'N' and ref.values != 'E':
        coord = -coord
    return coord

# function to extract from pdf
def extractFromPDF(file_path):
    metadata = {
        'name': os.path.basename(file_path),
        'size': os.path.getsize(file_path),
        'created_time': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
        'modified_time': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
        'pdf_meta': {}
    }
    
    try:
        reader = PdfReader(file_path)
        doc_info = reader.metadata  # formerly reader.getDocumentInfo()
        for key, value in doc_info.items():
            metadata['pdf_meta'][key] = str(value)
    except Exception as e:
        return f"PDF error: {e}"
    
    return metadata

# main code to call function depending on if its an image or document
def extract_metadata(path):
    ans = ""
    if os.path.exists(path):
        ans += "Valid path - performing metadata extraction \n\n"
        if path.lower().endswith((".jpg", ".jpeg")):
            metadata = extractFromImage(path)
            ans += pprint.pformat(metadata, indent=2)
            return ans
        elif path.lower().endswith(".pdf"):
            metadata = extractFromPDF(path)
            ans += pprint.pformat(metadata, indent=2)
            return ans
        else:
            return "Filetype not supported (only jpg/jpeg and pdf)."
    else:
        return "Invalid path - make sure the filepath exists."