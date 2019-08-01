import json
from . import app, client, cache, create_token

class TestClientCrud():
    var = 0
    def test_Client_valid_input_post_name(self, client):
        token = create_token()
        data = {
            'client_key':'CLIENT10',
            'client_secret':'SECRET12',
            'status':True,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/Client', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        TestClientCrud.var = res_json['client_id']
        assert res.status_code == 200
    
    def test_Client_invalid_post_name(self, client):
        token = create_token()
        data = {
            'client_secret':'SECRET08',
            'status':True,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/Client', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400
    

    def test_Client_valid_input_put(self, client):
        token = create_token()
        data = {
            'client_key':'CLIENT15',
            'client_secret':'SECRET20',
            'status':True,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.put('/Client/'+str(TestClientCrud.var), data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Client_invalid_input_put(self, client):
        token = create_token()
        data = {
            'client_secret':'SECRET20',
            'status':True,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.put('/Client/'+str(TestClientCrud.var), data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_client_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/Client/list',
                            headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Client_get_invalid_id_token(self, client):
        res = client.get('/Client/'+str(TestClientCrud.var),
                        headers={'Authorization':'Bearer abc'})
        
        res_json = json.loads(res.data)
        assert res.status_code == 500
    
    def test_Client_get_valid_id_token(self, client):
        token = create_token()
        res = client.get('/Client/'+str(TestClientCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Client_delete_token(self, client):
        token = create_token()
        res = client.delete('/Client/'+str(TestClientCrud.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Client_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/Client/500',
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_client_invalid_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/Client/list1',
                            headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404
    

    


    

    