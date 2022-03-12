from base64 import b64encode
import flask
from flask import request, send_file
from google.cloud import vision

app = flask.Flask(__name__)
# ENCODING = 'utf-8'

@app.route('/', methods=['POST'])
def detect_text():
    client=vision.ImageAnnotatorClient.from_service_account_json('resources\\ocr.json')
    byte_content=request.data

    image=vision.Image(content=byte_content)
    response = client.text_detection(image=image)
    texts = response.text_annotations[1]
    print(texts)
    description=texts.description
    print(description)
    # print(texts)
    # print('Texts:')
    #
    # for text in texts:
    #     print('\n"{}"'.format(text.description))
    #
    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                  for vertex in text.bounding_poly.vertices])
    #
    #     print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return response

def read_image(path):
    """Detects text in the file."""
    import io
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    return content

if __name__ == '__main__':
    path = "resources\\img.png"
    byte_content=read_image(path)
    # https://stackoverflow.com/questions/37225035/serialize-in-json-a-base64-encoded-data
    # bytes
    # base64_bytes = b64encode(byte_content)
    # string
    # base64_string = base64_bytes.decode(ENCODING)

    # https://betterprogramming.pub/google-vision-and-google-sheets-api-line-by-line-receipt-parsing-2e2661261cda
    # https://stackoverflow.com/questions/64649598/how-to-send-an-image-via-post-request-in-flask
    app.test_client().post('/',data=byte_content)
    # app.run(host='localhost')