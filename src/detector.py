from base64 import b64decode
import flask
from flask import request, jsonify
from google.cloud import vision

SKIPWORDS = ['eur', 'stk', 'straße', 'str.', 'tel', 'posten', 'www', 'geschlossen','*','datum','terminalnummer','+ ','transaktions']
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
MARKETS = ['drogerie', 'lidl', 'rewe', 'real', 'allguth', 'dm', 'edeka','ldl','aldi']
BLACKLIST_WORDS = ['steuer-nr', 'eur*', 'pfand']


def check_number(text):
    text = text.replace('x', '')
    try:
        number = int(text)
        return number
    except Exception as e:
        return False


def check_price_and_place(text):
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
        if contain_substring(STOPWORDS,text.lower()):
            break
        if contain_substring(
                SKIPWORDS +
                MARKETS +
                BLACKLIST_WORDS,
                text.lower()):
            continue
        if number == 1:
            number = check_number(text)
            if number:
                continue
            else:
                number = 1
        if check_price_and_place(text):
            continue
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
    print("You have connected with the server!")
    try:
        client = vision.ImageAnnotatorClient.from_service_account_json(
            'resources//ocr.json')
        content = request.get_json(force=True)
        # print(content)
        byte_content = b64decode(content['image'])
        # print(byte_content)

        image = vision.Image(content=byte_content)
        response = client.document_text_detection(image=image)
        texts = response.full_text_annotation.text
        articles = parse_texts(texts)
        # print("articles:", articles)

        if response.error.message:
            print('{}\nFor more info on error messages, check:https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
            return '{}\nFor more info on error messages, check:https://cloud.google.com/apis/design/errors'.format(
                response.error.message), 400

        else:
            return jsonify(articles), 200
    except Exception as e:
        print(e)
        return "Request must specify image and features.",500


def read_image(path):
    """Detects text in the file."""
    import io
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    return content


if __name__ == '__main__':
    # path = "resources\\edeka.jpg"
    # path = "resources\\lidl.jpg"
    # byte_content = read_image(path)
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
    # response=app.test_client().post('/', data=None)
    # print(response.json)

    app.run(debug= True,host='0.0.0.0')
