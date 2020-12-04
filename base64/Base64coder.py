import base64
# For both Python 2.7 and Python 3.x

#
# in
#
encoded_string = ""
with open("imageToSave.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

base64_str = encoded_string.decode()
print(base64_str)

#
# out
#
with open("imageOut.jpg", "wb") as fh:
    fh.write(base64.decodebytes(encoded_string))
