import json
from . import app, client, cache, create_token1

class Test_rent_id():
    var = 0
    def test_rent_valid_input_post_name(self, client):
        token = create_token1()
        data = {
            'user_id':2,
            'books_id':5,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/rent', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        Test_rent_id.var = res_json['rent_id']
        assert res.status_code == 200
    
    def test_rent_invalid_post_name(self, client):
        token = create_token1()
        data = {
            'books_id':5,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/rent', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    def test_rent_getlist(self, client): # client dr init test
        token = create_token1()
        data = {
            'r': 1,
            'rp': 25,
        }
        res = client.get('/rent/list', query_string = data,
                            headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_rent_get_invalid_id_token(self, client):
        res = client.get('/rent/'+str(Test_rent_id.var),
                        headers={'Authorization':'Bearer abc'})
        
        res_json = json.loads(res.data)
        assert res.status_code == 500
    
    def test_rent_get_valid_id_token(self, client):
        token = create_token1()
        res = client.get('/rent/'+str(Test_rent_id.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_rent_invalid_getlist(self, client): # client dr init test
        token = create_token1()
        data = {
            'r': 1,
            'rp': 25,
        }
        res = client.get('/rent/list1', query_string = data,
                            headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404