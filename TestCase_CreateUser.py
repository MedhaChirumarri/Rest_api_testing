import time, OpenTap
import requests
import sys
import json

#from PythonTap import *
from System import String

from .SampleBasicDut import *



@Attribute(OpenTap.DisplayAttribute,
           " TestCase_CreateUser",
           "Creating a new user",
           "RestAPI_Testing")


class SampleTC1(TestStep):
    
    def __init__(self):
        super(SampleTC1, self).__init__()

        prop = self.AddProperty("RestDut","", RESTAPIDut)
        prop.AddAttribute(OpenTap.DisplayAttribute,"1.Select DUT","Select DUT","DUT")

        prop = self.AddProperty("FirstName","Janet", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"2.Input FirstName","Input FirstName","Input")

        prop = self.AddProperty("Job","Developer", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"3.Input Job","Input Job","Input")

       

       


    def Run(self):
  
        #time.sleep(3)
        print("TestCase_CreateUser_POST")
        #input json file
        #filename=input()
        #with open(filename) as fid:
        #    dat = json.load(fid)
        data = {'name':self.FirstName,'job':self.Job}
        print(self.RestDut.InputURL)
        response = self.RestDut.PostData(self.RestDut.InputURL,'users',data)
        print("Post Request Sent")

        input_data = response.json()
        input_data.pop("createdAt")
        attr = input_data.keys()
        print(attr)
        id=input_data['id']
        print(id)
        print(self.RestDut.InputURL+'users/'+str(id))
        
        get_resp_id=self.RestDut.GetData(self.RestDut.InputURL,'users/'+str(id))
        data = get_resp_id.text
        fo_data = json.loads(data)
        print(fo_data)
        result='Pass'
        for i in attr:
                    if fo_data=={}:
                        print("404 error - id not present ")
                        result = 'Fail'
                        break
                    elif str(input_data[i])!=str(fo_data['data'][i]):
                        print("not the same data at id api!")
                        result = 'Fail'
                        break
        if result=='Pass': 
                    
            print("fetched details of the created user is stored in fo_data (id data)")
                            
            print('checking if same data is present in user list....')
            get_resp_list = self.RestDut.GetData(self.RestDut.InputURL,'users')
            data_n = get_resp_list.text
            foo_data = json.loads(data_n)
            total_pages=foo_data["total_pages"]


            idd=-1
            for i in range(1,total_pages+1):
                
                response_page_wise =self.RestDut.GetData(self.RestDut.InputURL,'users/?page='+str(i))
                data_p = response_page_wise.text
                f3_data = json.loads(data_p)
                
                data_len = len(f3_data['data'])
                for i in range(data_len):
                    if str(f3_data['data'][i]['id']) == str(id):
                        idd=id
                        for j in attr:
                            if str(input_data[j])!=str(f3_data['data'][i][j]):
                                print("not the same data!")
                                sys.exit(0)
                            
                        print("fetched details of the created user is also present in user list and can be acessed using f3_data['data'][i]")
                        print(f3_data['data'][i])

            if idd==-1:
                print("id not found in users list")
                result = 'Fail'        
                
        if result == "Pass":
                self.UpgradeVerdict(OpenTap.Verdict.Pass)  
        else:
                self.UpgradeVerdict(OpenTap.Verdict.Fail)            

            
        


