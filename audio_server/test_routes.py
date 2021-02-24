import pytest, datetime
from . import create_app

class TestAPI:

    #This test function checks the response code for GET request.
    #If a GET request is made using any of the 3 audio_type, then the test would PASS
    #If anything apart from the 3 audio_type, then the test would FAIL.
    def test_fetch(self):
        requests = create_app().test_client(self)
        response = requests.get('/song')
        assert response.status_code == 200

    #This test function checks the response code(200) for GET request.
    #If a GET request is made using any of the 3 audio_type along with a valid audio_id, then the test would PASS
    #If a GET request is made using any of the 3 audio_type along with an invalid audio_id, then the test would FAIL
    #If anything apart from the 3 audio_type along with an invalid auido_id, then the test would FAIL.
    def test_fetch_valid_id(self):
        requests = create_app().test_client(self)
        response = requests.get('/song/1')
        assert response.status_code == 200

    #This test function checks the content(application/json) of GET request.
    #If a GET request is made using anything, then the test would PASS
    def test_fetch_content(self):
        requests = create_app().test_client(self)
        response = requests.get('/hi')
        assert response.content_type == 'application/json'

    #This test function checks the status code of DELETE request.
    #If a DELETE request is made using a valid audio_type and auido_id, then the test would PASS
    def test_delete(self):
        requests = create_app().test_client(self)
        response = requests.delete('/song/1')
        assert response.status_code == 200

    #This test function checks the status code of POST request.
    #If a POST request is made using a valid audio_type and json, then the test would PASS
    def test_post(self):
        requests = create_app().test_client(self)
        response = requests.post('/song/add', json={'name':'test', 'duration':100, 'upload':datetime.datetime.now()})
        assert response.status_code == 200

    


    