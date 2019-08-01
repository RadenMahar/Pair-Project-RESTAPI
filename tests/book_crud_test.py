import json
from . import app, client, cache, create_token

class TestBookCrud():
    var = 0
    def test_Books_valid_input_post_name(self, client):
        token = create_token()
        data = {
            'books_title': 'fuckin',
            'books_isbn': 'ashole',
            'writter': 'mahardsa',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/Books', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        TestBookCrud.var = res_json['books_id']
        assert res.status_code == 200
    
    def test_Books_invalid_post_name(self, client):
        token = create_token()
        data = {
            'books_isbn': 'lkjdlkjaldjal',
            'writter': 'lkjdlajdlksadiiuiuiyu',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/Books', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400
    

    def test_Books_valid_input_put(self, client):
        token = create_token()
        data = {
            'books_title': 'dadlksajdlksjd',
            'books_isbn': 'dsalksajdajdnmnzmx',
            'writter': 'maharpasdadnji',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.put('/Books/'+str(TestBookCrud.var), data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Books_invalid_input_put(self, client):
        token = create_token()
        data = {
            'books_isbn': 'dsalksajdajdnmnzmx',
            'writter': 'maharpasdadnji',
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.put('/Books/'+str(TestBookCrud.var), data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_Books_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/Books/list',
                            headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Books_get_invalid_id_token(self, client):
        res = client.get('/Books/'+str(TestBookCrud.var),
                        headers={'Authorization':'Bearer abc'})
        
        res_json = json.loads(res.data)
        assert res.status_code == 500
    
    def test_Books_get_valid_id_token(self, client):
        token = create_token()
        res = client.get('/Books/'+str(TestBookCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Books_delete_token(self, client):
        token = create_token()
        res = client.delete('/Books/'+str(TestBookCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Books_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/Books/500',
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_Books_invalid_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/Books/list1',
                            headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404