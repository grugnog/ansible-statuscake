#!/usr/bin/python

from ansible.module_utils.basic import *
import requests

class StatusCake:

    def __init__(self, module, username, api_key, name, url, test_tags, check_rate, test_type, contact, tcp_port, custom_header):
        self.headers = {"Username": username, "API": api_key}
        self.module = module
        self.name = name
        self.url = url
        self.test_tags = test_tags
        self.test_type = test_type
        self.contact = contact
        self.tcp_port = tcp_port
        self.custom_header = custom_header
        self.check_rate = check_rate

    def check_response(self,resp):
        if resp['Success'] == False:
            self.module.exit_json(changed=False, meta= resp['Message'])
        else:
            self.module.exit_json(changed=True, meta= resp['Message'])
            
    def check_test(self):
        API_URL = "https://app.statuscake.com/API/Tests"
        response = requests.put(API_URL, headers=self.headers)
        json_object = response.json()

        for item in json_object:
            if item['WebsiteName'] == self.name:
                return item['TestID']
                    
    def create_test(self):
        API_URL = "https://app.statuscake.com/API/Tests/Update"
        data = {"WebsiteName": self.name, "WebsiteURL": self.url, "CheckRate": self.check_rate,
                    "TestType": self.test_type, "TestTags": self.test_tags, "ContactGroup": self.contact,
                    "Port": self.tcp_port, "CustomHeader": self.custom_header}

        test_id = self.check_test()
        
        if not test_id:
            response = requests.put(API_URL, headers=self.headers, data=data)    
            self.check_response(response.json())
        else:
            data['TestID'] = test_id
            response = requests.put(API_URL, headers=self.headers, data=data)
            self.check_response(response.json())

def main():
    
    fields = {
        "username": {"required": True, "type": "str"},
        "api_key": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "url": {"required": True, "type": "str"},
        "test_tags": {"required": False, "type": "str"},
        "check_rate": {"required": False, "default": 300, "type": "int"},
        "test_type": {"required": False, "choices": ['HTTP', 'TCP'],"type": "str"},
        "contact": {"required": False, "type": "int"},
        "port": {"required": False, "type": "int"},
        "user_agent": {"required": False, "default":"Fake Agent", "type": "str"}
    }   

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)
    
    username = module.params['username']
    api_key = module.params['api_key']
    name = module.params['name']
    url = module.params['url']
    test_tags = module.params['test_tags']
    check_rate = module.params['check_rate']
    test_type = module.params['test_type']
    contact = module.params['contact']
    tcp_port = module.params['port']
    custom_header = '{"User-Agent":"' + module.params['user_agent'] + '"}'

    test_object = StatusCake(module, username, api_key, name, url, test_tags, check_rate, test_type, contact, tcp_port, custom_header)
    test_object.create_test()

if __name__ == '__main__':  
    main()
