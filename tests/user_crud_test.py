import json
from . import app, client, cache, create_token

class Test_User_id():
    var = 0
    def test_User_valid_input_post_name(self, client):
        token = create_token()
        data = {
            'user_name':'mapan',
            'user_age':76,
            'user_sex':'male',
            'client_id': 15,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/User', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        Test_User_id.var = res_json['user_id']
        assert res.status_code == 200
    
    def test_User_invalid_post_name(self, client):
        token = create_token()
        data = {
            'user_age':799,
            'user_sex':'female',
            'client_id': 2,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.post('/User', data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400
    

    def test_User_valid_input_put(self, client):
        token = create_token()
        data = {
            'user_name':'sempak',
            'user_age':76,
            'user_sex':'male',
            'client_id': 15,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.put('/User/'+str(Test_User_id.var), data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_User_invalid_input_put(self, client):
        token = create_token()
        data = {
            'user_age':76,
            'user_sex':'male',
            'client_id': 1,
        }
        #karena post menggunakan data, sedangkan get menggunkan query_string
        res = client.put('/User/'+str(Test_User_id.var), data=json.dumps(data),
                        headers={'Authorization':'Bearer ' + token},
                        content_type='application/json')
        
        res_json = json.loads(res.data)
        assert res.status_code == 400

    def test_user_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/User/list',
                            headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_User_get_invalid_id_token(self, client):
        res = client.get('/User/'+str(Test_User_id.var),
                        headers={'Authorization':'Bearer abc'})
        
        res_json = json.loads(res.data)
        assert res.status_code == 500
    
    def test_User_get_valid_id_token(self, client):
        token = create_token()
        res = client.get('/User/'+str(Test_User_id.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_User_delete_token(self, client):
        token = create_token()
        res = client.delete('/User/'+str(Test_User_id.var),
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    def test_Client_invalid_delete_token(self, client):
        token = create_token()
        res = client.delete('/User/500',
                        headers={'Authorization':'Bearer ' + token})
        
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    def test_client_invalid_getlist(self, client): # client dr init test
        token = create_token()
        res = client.get('/User/list1',
                            headers={'Authorization':'Bearer ' + token},
                            content_type='application/json')

        res_json = json.loads(res.data)
        assert res.status_code == 404
    

    


    

    