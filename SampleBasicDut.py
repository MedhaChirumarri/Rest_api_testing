"""
 A basic example of how to define a DUT driver.
"""
from PythonTap import *
import OpenTap
import requests
from System import String

@Attribute(OpenTap.DisplayAttribute, "RestAPI DUT", "A basic example of a DUT driver.", "Python Example")
class RESTAPIDut(Dut):
    def __init__(self):
        "Set up the properties, methods and default values of the instrument."
        super(RESTAPIDut, self).__init__() # The base class initializer must be invoked.

        prop = self.AddProperty("InputURL","https://reqres.in/api/", String)
        prop.AddAttribute(OpenTap.DisplayAttribute,"Input RESTApi Url","","Input")

    def PostData(self, RestUrl,addUrl,Data):
        """Called by TAP when the test plan starts."""
        self.Info("Python Instrument Opened")
        response = requests.post(RestUrl+addUrl, Data)
        print("Sending Post Request To https://reqres.in/api/users")
        print("Response From REST Server: ", response.json())
        return response

    def GetData(self, RestUrl,addUrl):
        """Called by TAP when the test plan starts."""
        self.Info("Python Instrument Opened")
        response = requests.get(RestUrl+addUrl)
        print("Sending GET request to the given url")
        return response

    def PatchData(self, RestUrl,addUrl,Data):
        """Called by TAP when the test plan starts."""
        self.Info("Python Instrument Opened")
        response = requests.patch(RestUrl+addUrl,Data)
        print("Sending GET request to the given url")
        return response 
    
    def DeleteData(self, RestUrl,addUrl):
        """Called by TAP when the test plan starts."""
        self.Info("Python Instrument Opened")
        response = requests.delete(RestUrl+addUrl)
        print("Sending GET request to the given url")
        return response

    