import time, OpenTap
import requests
import sys
import json

#from PythonTap import *
from System import String

from .SampleBasicDut import *



@Attribute(OpenTap.DisplayAttribute,
           " TestCase_Delete_User",
           "Testing deleting of a user",
           "RestAPI_Testing")


class SampleTC3(TestStep):
    
    def __init__(self):
        super(SampleTC3, self).__init__()

        prop = self.AddProperty("RestDut","", RESTAPIDut)
        prop.AddAttribute(OpenTap.DisplayAttribute,"1.Select DUT","Select DUT","DUT")
        
        prop = self.AddProperty("id",'2', String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"2.Input id","","Input")

        

        

    def Run(self):
            print("TestCase_DeleteUser")
            #input json file
            #filename=input()
            #with open(filename) as fid:
            #    dat = json.load(fid)
            data = {'id':int(self.id)}

            id=data['id']
            print(id)
            get_resp_id=self.RestDut.DeleteData(self.RestDut.InputURL,str(id))
            get_updated_id=self.RestDut.GetData(self.RestDut.InputURL,str(id))
            data1 = get_updated_id.text
            up_data = json.loads(data1)
            print(up_data)
            #updating the obtained id
            result = 'Pass'
            if bool(up_data) == False:
                print("delete successful")
                #checking if data is present in userlist and i?
                print('checking if data is updated in user list....')
                get_resp_list = self.RestDut.GetData(self.RestDut.InputURL,'')
                data_n = get_resp_list.text
                foo_data = json.loads(data_n)
                total_pages=foo_data["total_pages"]

                idd=-1
                for i in range(1,total_pages+1):
                    
                    response_page_wise =self.RestDut.GetData(self.RestDut.InputURL,str(i))
                    data_p = response_page_wise.text
                    f3_data = json.loads(data_p)
                    data_len = len(f3_data['data'])
                    for i in range(data_len):
                        if str(f3_data['data'][i]['id']) == str(id):
                            idd=id
                            break
                        
                if idd==-1 :
                    print("delete succesful")
                    result = 'Pass'
                    
                else:
                    print("testcase failed")
                    result = 'Fail'
                     
            else: 
                print("test failed")
                result = 'Fail'
            
            if result == "Pass":
                self.UpgradeVerdict(OpenTap.Verdict.Pass)  
            else:
                self.UpgradeVerdict(OpenTap.Verdict.Fail)




            
             