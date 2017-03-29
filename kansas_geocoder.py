'''
Created on November 5th, 2010
Notes:
This is built to parse json results from ESRI geocoders/locators

All rights reserved under the copyright laws of the United States.

You may freely redistribute and use this sample code, with or without modification.
The sample code is provided without any technical support or updates.

Disclaimer OF Warranty: THE SAMPLE CODE IS PROVIDED "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE, OR NONINFRINGEMENT ARE DISCLAIMED. IN NO EVENT SHALL
ESRI OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED AND ON ANY THEORY
OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ARISING IN ANY WAY OUT
OF THE USE OF THIS SAMPLE CODE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
THESE LIMITATIONS SHALL APPLY NOTWITHSTANDING ANY FAILURE OF ESSENTIAL PURPOSE OF
ANY LIMITED REMEDY.

For additional information contact: Environmental Systems Research Institute, Inc.

Attn: Contracts Dept.
380 New York Street
Redlands, California, U.S.A. 92373
Email: contracts@esri.com

Additional tweaks for the KS_Geocoder made by Mike D'Attilio with the Kansas Adjutant General's Office, Division of Emergency Management on 3/17/2017
Mike's code was generalized by Kristen Jordan Koenig of the Kansas Data Access and Support Center on 3/17/2017
'''

import sys, traceback
from urllib import urlencode
from urllib2 import HTTPError, URLError, urlopen
from json import loads
from arcpy import GetMessages, AddError, ListFields
from arcpy.da import UpdateCursor

def getGeocodeURL():
    #change the url if you want to use a different geocoding service
    url = r'http://services.kansasgis.org/arcgis4/rest/services/Geocoders/KS_Geocoder/GeocodeServer/findAddressCandidates?'
    return url

def main():
    pass
    ##################################
    #in this portion, define which method you want to use. See the methods below for descriptions and parameters that you might need to change.
##    geocodeParsedTable()
##    geocodeSingleLineInputTable()
    geocodeHardcodedAddresses()
    ##################################

#use this example if you want to geocode a table of addresses that has a single line input. This will add coordinates to your table.
def geocodeSingleLineInputTable():
    setGlobals()
    table = r"" #define your table here
    SingleLineInputField = "" #define your single line input field here

    latField = "" #define your latitude field (the Y field). This field should already exist in the table.
    longField = "" #define your longitude field (the X field). This field should already exist in the table.
    fields = (latField, longField, SingleLineInputField)

    with UpdateCursor(table, fields) as rows:
        for row in rows:
            address = {'SingleLine':row[2]}
            xy = geoCodeAddress(address)
            if xy != None:
                row[0] = xy[1] #sets latitude value
                row[1] = xy[0] #sets longitude value
                rows.updateRow(row) #updates the row

#use this example if you want to geocode a table of parsed addresses. This will add coordinates to your table.
def geocodeParsedTable():
    setGlobals()
    table = r"" #define your table here
    streetField = "" #define your street address field name here
    cityField = "" #define your city field here
    stateField = "" #define your state field here
    zipField = "" #define your zip code field here

    latField = "" #define your latitude field (the Y field). This field should already exist in the table.
    longField = "" #define your longitude field (the X field). This field should already exist in the table.

    fields = (latField, longField, streetField, cityField, stateField, zipField)

    with UpdateCursor(table, fields) as rows:
        for row in rows:
            address = {'Street':row[2],'City':row[3],'State':row[4],'Zip':row[5]} #creates a dictionary of the address
            xy = geoCodeAddress(address)
            if xy != None:
                row[0] = xy[1] #sets latitude value
                row[1] = xy[0] #sets longitude value
                rows.updateRow(row) #updates the row


#use this example if you want to hard code the addresses to be geocoded
def geocodeHardcodedAddresses():
    try:
        setGlobals()
        address = {}

        #single line input example
##        address['SingleLine'] = '2020 SW 32nd Street, Topeka, KS 66611'
##        xy = geoCodeAddress(address)
##        if xy != None:
##            print str(xy[0]) + ' ' + str(xy[1])

        #parsed examples
        address['Street'] =  '2020 SW 32nd Street'
        address['City'] = 'Topeka'
        address['State']= 'KS'
        address['Zip']= '66611'
        xy = geoCodeAddress(address)
        if xy != None:
            print str(xy[0]) + ' ' + str(xy[1]) + ' ' + address['Street'] + ' ' + address['City']

        address['Street'] =  '2010 SW 32nd Street'
        address['City'] = 'Topeka'
        address['State']= 'KS'
        address['Zip']= '66611'
        xy = geoCodeAddress(address)
        if xy != None:
            print str(xy[0]) + ' ' + str(xy[1]) + ' ' + address['Street'] + ' ' + address['City']

        address['Street'] =  '2020 SW 32nd terrace'
        address['City'] = 'Topeka'
        address['State']= 'KS'
        address['Zip']= '66611'
        xy = geoCodeAddress(address)
        if xy != None:
            print str(xy[0]) + ' ' + str(xy[1]) + ' ' + address['Street'] + ' ' + address['City']

        address['Street'] =  '5175 Tuttle Cove Rd'
        address['City'] = 'Manhattan'
        address['State']= 'KS'
        address['Zip']= '66502'
        xy = geoCodeAddress(address)
        if xy != None:
            print str(xy[0]) + ' ' + str(xy[1]) + ' ' + address['Street'] + ' ' + address['City']

        address['Street'] =  '2800 SW TOPEKA BLVD'
        address['City'] = 'TOPEKA'
        address['State']= 'KS'
        address['Zip']= '66611'
        xy = geoCodeAddress(address)
        if xy != None:
            print str(xy[0]) + ' ' + str(xy[1]) + ' ' + address['Street'] + ' ' + address['City']


        address['Street'] =  ''
        address['City'] = 'Topeka'
        address['State']= 'KS'
        address['Zip']= ''
        xy = geoCodeAddress(address)
        if xy != None:
            print str(xy[0]) + ' ' + str(xy[1]) + ' ' + address['Street'] + ' ' + address['City']

    except:

        # Return any python specific errors and any error returned by the geoprocessor
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "Python Errors:\nTraceback Info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        gpmsg = "GP ERRORS:\n" + GetMessages(2) + "\n"


        print pymsg
        print gpmsg
        AddError(pymsg)
        AddError(gpmsg)


class dascgeocoder:
    def __init__(self,at=None):
        #Constructor gives the ability to set the rest url to your findAddressCandidates method. The ? needs to be included
        self.token = at
        self.locator_url = getGeocodeURL()
        self.count = 0

        #extra settings for all geocodes
        settings = {}
        settings['f'] = 'pjson'
        settings['SingleLine']=''
        settings['category']=''
        settings['outFields']=''
        settings['maxLocations']=''
        settings['outSR']= 4269
        settings['searchExtent']=''
        settings['location']=''
        settings['distance']=''
        settings['magicKey']=''
#        settings['searchExtent'] = '{"xmin":-102.095947265625,"ymin":36.925048828125,"xmax":-94.559326171875,"ymax":40.0726318359375,"spatialReference":{"wkid":4326}}'
        self.settings = urlencode(settings)

    def __buildResult(self, data):
        # use this section to manipulate the result data into some other format if desired

        return data

    def getLocation(self,address):
        self.__params = urlencode(address)
        try:
##            self.__url = self.locator_url + self.__params + '&f=json&Region=Kansas&CountryCode=USA&searchExtent={"xmin":-102.095947265625,"ymin":36.925048828125,"xmax":-94.559326171875,"ymax":40.0726318359375,"spatialReference":{"wkid":4326}}' # use coma seperated list of fileds in the outfileds param
            self.__url = self.locator_url + self.__params + '&' + self.settings
##            print self.__url
##            self.__url = r'http://services.kansasgis.org/arcgis4/rest/services/Geocoders/KS_Geocoder/GeocodeServer/findAddressCandidates?Street=2020+sw+32nd+street&City=topeka&State=ks&ZIP=66611&SingleLine=&category=&outFields=&maxLocations=&outSR=&searchExtent=&location=&distance=&magicKey=&f=pjson'
            self.__data = urlopen(self.__url).read()
            self.__result = self.__buildResult(loads(self.__data))
            self.count += 1
            return self.__result
        except HTTPError, e:
            return "HTTP error: %d" % e.code
        except URLError, e:
            return "Network error: %s" % e.reason.args[1]


def setGlobals():
    #Environment Settings
    global dascgeocoder, app_id, app_secret, access_token


def geoCodeAddress(address):
    #main routine to geocode the addresses
    dascgeocoder1 = dascgeocoder()
    dascgeocoder1.locator_url = getGeocodeURL()
    result = dascgeocoder1.getLocation(address)
    if result != None:
        if 'candidates' in result:
            candidates = result['candidates']
            if (len(candidates) > 0):
                # evaluate the candidates to see which one has the highest score
                topScore = 0
                for c in candidates:
                    score = float(c['score'])
                    if score > topScore:
                        # if the candidate score is higher than any other
                        # current scores, replace the topScore and first candidate
                        topScore = score
                        first = c
            else:
                first = None
            ##print 'first is', first
            if first != None:
                loc = first['location']
                x = loc['x']
                y = loc['y']
                L = [x,y]
                return L
            else:
                return first
    else:
        return None


if __name__ == '__main__':
    main()

