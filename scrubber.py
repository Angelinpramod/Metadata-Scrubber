from PIL import Image
image=Image.open('Kodak_CX7530.jpg')
print(image.getexif())
