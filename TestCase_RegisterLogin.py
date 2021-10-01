import time, OpenTap
import requests
import sys
import json

#from PythonTap import *
from System import String

from .SampleBasicDut import *


@Attribute(OpenTap.DisplayAttribute,
           " TestCase_Register_Login",
           "registering and logging of a user",
           "RestAPI_Testing")


class SampleTC4(TestStep):
    
    def __init__(self):
        super(SampleTC4, self).__init__()

        prop = self.AddProperty("RestDut","", RESTAPIDut)
        prop.AddAttribute(OpenTap.DisplayAttribute,"1.Select DUT","Select DUT","DUT")

        prop = self.AddProperty("RegEmail","janet.weaver@reqres.in", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"2.Input Register email","Input Register email","Input")

        prop = self.AddProperty("RegPwd","janet", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"3.Input Reg Pwd","Input Reg Pwd","Input")

        prop = self.AddProperty("LoginEmail","janet.weaver@reqres.in", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"4.Input Login email","Input Login email","Input")

        prop = self.AddProperty("LoginPwd","janet", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"5.Input Login Pwd","Input Login Pwd","Input")

        

       


    def Run(self):
        #filename=input()
        print("TestCase_Register_Login")
        #with open(filename) as fid:
        #    dat = json.load(fid)
        
        data = {'email':self.RegEmail,'password':self.RegPwd}    
        response = self.RestDut.PostData(self.RestDut.InputURL,'register',data)
       
        if 'password' not in data.keys():
            print(response)
            sys.exit(0)
        else:
            print(response,'registration succesful')
        register_data = response.json()
        token = register_data['token']
        id=register_data['id']

        data2= {'email':self.LoginEmail,'password':self.LoginPwd}

        login_resp = self.RestDut.PostData(self.RestDut.InputURL,'login',data2)
        login_data = login_resp.json()
        try:
            if (login_data['token']==token) and (data['password']==data2['password']):
                data_of_id = self.RestDut.GetData(self.RestDut.InputURL,'login/'+str(id))
                data_of_id = data_of_id.json()
                print(data_of_id)
            else:
                print("password doesnt match")

        except:
            print('user not found')
        self.UpgradeVerdict(OpenTap.Verdict.Pass)  