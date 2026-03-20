from PIL import Image,ExifTags
image=Image.open('Kodak_CX7530.jpg')
exif_data=image.getexif()
gps_data = exif_data.get_ifd(34853)
print(gps_data)

for tag_id,value in exif_data.items():
  tag_name = ExifTags.TAGS.get(tag_id, tag_id) 
  print(f"{tag_name:25} : {value}")
for tag_id,value in gps_data.items():
  gps=ExifTags.GPSTAGS.get(tag_id,tag_id)
  print(f"{gps:25}:{value}")

