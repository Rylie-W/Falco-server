# falco-server
This is the backend repository for <b>Falco</b>, a food-saving application with dietary advice.

It listens http requests with the byte array of a receipt image in their body on port 5000, and sends responses with json in their body, of which the key is products and the value is corresponding numbers in the receipt.

## How to Run
### Requirements
[Google service account](https://support.google.com/a/answer/7378726?hl=en) : https://support.google.com/a/answer/7378726?hl=en
### Download the Project
<code>
git clone https://github.com/Rylie-W/falco-server.git

cd falco-server
</code>

### Add the JSON File of Your Google Service Account
Paste your JSON file into the directory <code>falco-server/src/resources</code> with the name <code>ocr.json</code>.

### Install Requirements
<code>pip install -r requirements.txt</code>

### Run the Server

<code>
cd src

python detector.py
</code>
