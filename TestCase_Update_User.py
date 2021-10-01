import time, OpenTap
import requests
import sys
import json

#from PythonTap import *
from System import String

from .SampleBasicDut import *



@Attribute(OpenTap.DisplayAttribute,
           " TestCase_Update_User",
           "updating a user",
           "RestAPI_Testing")


class SampleTC2(TestStep):
    
    def __init__(self):
        super(SampleTC2, self).__init__()

        prop = self.AddProperty("RestDut","", RESTAPIDut)
        prop.AddAttribute(OpenTap.DisplayAttribute,"1.Select DUT","Select DUT","DUT")

        prop = self.AddProperty("FirstName","Janet", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"2.Input FirstName","Input FirstName","Input")

        prop = self.AddProperty("id","2", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"3.Input Id","Input id","Input")

        

       


    def Run(self):
        print("TestCase_updateUser_PUT")
        data = {'first_name':self.FirstName,'id':int(self.id)}

        id=data['id']
        #self.RestDut.InputURL = 'https://reqres.in/api/users/'
        print(self.RestDut.InputURL+str(id))
        get_resp_id=self.RestDut.GetData(self.RestDut.InputURL,str(id))
        data1 = get_resp_id.text
        fo_data = json.loads(data1)
        attr = data.keys()
        result = "Pass"
        #updating the obtained id
        if fo_data == {}:
            print("no user with the given id")
            sys.exit(0)
        else: 
            update_data_id =  self.RestDut.PatchData(self.RestDut.InputURL,str(id),data)
            
            get_updated_id=self.RestDut.GetData(self.RestDut.InputURL,str(id))
            data1 = get_updated_id.text
            up_data = json.loads(data1)
            print(up_data)
            for i in attr:
                if (str(data[i])!=str(up_data['data'][i])):
                            print(data[i], 'is not same as',up_data['data'][i])
                            print("test case failed")
                            result = 'Fail' 
                           
            if result == 'Pass':
                print("successfully updated")
               




                #checking if data is present in userlist and updated?
                print('checking if data is updated in user list....')
                get_resp_list = self.RestDut.GetData(self.RestDut.InputURL,'')
                data_n = get_resp_list.text
                foo_data = json.loads(data_n)
                total_pages=foo_data["total_pages"]

                idd=-1
                for i in range(1,total_pages+1):
                    
                    response_page_wise =self.RestDut.GetData(self.RestDut.InputURL,'?page='+str(i))
                    data_p = response_page_wise.text
                    f3_data = json.loads(data_p)
                    data_len = len(f3_data['data'])
                    for i in range(data_len):
                        if str(f3_data['data'][i]['id']) == str(id):
                            idd=id
                            for j in attr:
                                if str(data[j])!=str(f3_data['data'][i][j]):
                                    print("test case failed")
                                    result = 'Fail'
                                    break
                            
            if result == "Pass":
                 self.UpgradeVerdict(OpenTap.Verdict.Pass)  
            else :
                 self.UpgradeVerdict(OpenTap.Verdict.Fail)  
             