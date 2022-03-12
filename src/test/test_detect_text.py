import pytest
import pytest_mock
import flask
from src import detector
import json

def create_app():
    app = flask.Flask(__name__)
    return app

class TestTextDetector():
    app=create_app()

    def test_detect_text(self):
        import io
        path = "..\\resources\\img.png"
        # [START vision_python_migration_text_detection]
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        d = {'a': content}

        self.app.post("/",json=json.dumps(d))