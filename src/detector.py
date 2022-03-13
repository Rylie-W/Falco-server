from base64 import b64encode
import flask
from flask import request, jsonify
from google.cloud import vision

SKIPWORDS = ['eur', 'stk', 'straße', 'tel', 'posten', 'www']
STOPWORDS = [
    'summe',
    'visa',
    'mastercard',
    'mwst',
    'brutto',
    'netto',
    'zahlen',
    'kreditkarte',
    'ust-id-nr',
    'rück geld']
MARKETS = ['drogerie', 'lidl', 'rewe', 'real', 'allguth', 'dm', 'edeka']
BLACKLIST_WORDS = ['steuer-nr', 'eur*', 'pfand']


def check_number(text):
    text = text.replace('x', '')
    try:
        number = int(text)
        return number
    except Exception as e:
        return False


def check_price(text):
    if ' ' in text:
        price = text.split(' ')[0]
    else:
        price = text
    price = price.replace('B', '').replace('A', '')
    price = price.replace(',', '.')
    try:
        _ = float(price)
        return True
    except Exception as e:
        return False


def contain_substring(words, text):
    for word in words:
        if word in text:
            return True
    return False


def parse_texts(texts):
    texts = texts.split('\n')
    articles = dict()
    number = 1

    for text in texts:
        if contain_substring(
                SKIPWORDS +
                STOPWORDS +
                MARKETS +
                BLACKLIST_WORDS,
                text.lower()):
            continue
        if check_price(text):
            continue
        if number == 1:
            number = check_number(text)
            if number:
                continue
            else:
                number = 1
        if text != '':
            if articles.get(text) is not None:
                articles[text] += number
            else:
                articles[text] = number
        number = 1

    return articles


app = flask.Flask(__name__)
# ENCODING = 'utf-8'


@app.route('/', methods=['POST'])
def detect_text():
    client = vision.ImageAnnotatorClient.from_service_account_json(
        'resources\\ocr.json')
    byte_content = request.data

    image = vision.Image(content=byte_content)
    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation.text
    # texts = response.text_annotations[1:]
    articles = parse_texts(texts)
    print("articles:", articles)
    # for i,text in enumerate(texts):
    #     description = text.description
    #     print("line "+str(i)+': ',description)
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
        return '{}\nFor more info on error messages, check:https://cloud.google.com/apis/design/errors'.format(
            response.error.message), 400

    else:
        return jsonify(articles), 200


def read_image(path):
    """Detects text in the file."""
    import io
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    return content


if __name__ == '__main__':
    path = "resources\\edeka.jpg"
    byte_content = read_image(path)
    # https://stackoverflow.com/questions/37225035/serialize-in-json-a-base64-encoded-data
    # bytes
    # base64_bytes = b64encode(byte_content)
    # string
    # base64_string = base64_bytes.decode(ENCODING)
    '''
    test
    https://betterprogramming.pub/google-vision-and-google-sheets-api-line-by-line-receipt-parsing-2e2661261cda
    https://stackoverflow.com/questions/64649598/how-to-send-an-image-via-post-request-in-flask
    '''
    # response=app.test_client().post('/', data=byte_content)
    # print(response.json)

    app.run(host='localhost')
