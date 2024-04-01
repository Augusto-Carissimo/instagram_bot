from PIL import Image, UnidentifiedImageError
from PIL.ExifTags import TAGS, GPSTAGS
import re
from datetime import datetime

def get_date(filename):
  if 'IMG' in filename:
    date = re.split(r'[-_/]', filename)
    date = date[date.index('IMG') + 1]
    return change_date_format(date)
  else:
    try:
      exif = Image.open(filename)._getexif()
      exif_copy = exif.copy()
      for key, value in exif_copy.items():
          name = TAGS.get(key, key)
          exif[name] = exif.pop(key)
      if 'DateTimeOriginal' in exif:
          return change_date_format(exif['DateTimeOriginal'], input_format='%Y:%m:%d %H:%M:%S')
      else:
          return 'date unknown'
    except:
      return 'date unknown'

def change_date_format(date_str, input_format='%Y%m%d'):
  date_obj = datetime.strptime(date_str, input_format)
  formatted_date = date_obj.strftime('%d/%m/%Y')

  return formatted_date


