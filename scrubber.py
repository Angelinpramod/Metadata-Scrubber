from PIL import Image
image=Image.open('Kodak_CX7530.jpg')
exif_data=image.getexif()

for tag_id,value in exif_data.item():
  tag_name = ExifTags.TAGS.get(tag_id, tag_id) 
  print(f"{tag_name:25} : {value}")
