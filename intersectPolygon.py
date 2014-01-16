#!c:\Python27\python.exe

import json, urllib, urllib2, datetime, cgi, cgitb

print ("Content-type: application/json")
print

def buildJSONReturn(theURL, finalGeo):
    # theURL = 'http://2k8salmon1:6080/arcgis/rest/services/landview2014/mndnr_adminfeatures/MapServer/1/query'
    #finalGeo = {'rings': [[[375365.337450312,5321585.17834946], [376486.680253649,5321585.17834946], [376486.680253649,5320748.67825179], [375365.337450312,5320748.67825179], [375365.337450312,5321585.17834946]]]}
    geomUrl = 'http://2k8salmon1:6080/arcgis/rest/services/Utilities/Geometry/GeometryServer/intersect'
    areaUrl = 'http://2k8salmon1:6080/arcgis/rest/services/Utilities/Geometry/GeometryServer/areasAndLengths'
    data = []   # Blank Dictionary to populate with return
    theParams = urllib.urlencode({
        'f': "pjson",
        'sr': "26915",
        'outFields': "*",
        'geometryType': "esriGeometryPolygon",
        'spatialRel': "esriSpatialRelIntersects",
        'geometry': finalGeo
    })

    urlData = json.loads(urllib2.urlopen(theURL, theParams).read())
    try:
        dataReturn =  urlData['features']
        sr = urlData['spatialReference']

    except:
        print "No features"

    sr = "'spatialReference': {'wkid': 26915}, 'geometryType': 'esriGeometryPolygon'"
    for feature in dataReturn:
        geometries = []
        geometry =[]
        geometries.append("{'geometryType': 'esriGeometryPolygon', 'spatialReference': {'wkid': 26915}")
        geometry.append("{'geometryType': 'esriGeometryPolygon', 'spatialReference': {'wkid': 26915}")
        geometries.append(feature['geometry'])
        geometry.append(finalGeo)

        newgeom = str(geometries).replace("{u","'geometries':[{")
        lastgeom = newgeom[1:-1]+"]}"
        finalGeom = lastgeom.replace('"', "")

        newGeometry = str(geometry).replace('"', "")
        lastGeometry = newGeometry.replace("{'rings'","'geometry':{'rings'")
        finalGeometry = lastGeometry[1:-1]+"}"

        geomParams = urllib.urlencode({
            'f': "json",
            'sr': "26915",
            'outFields': "*",
            'geometries': finalGeom,
            'geometry': finalGeometry
        })

        geomData = json.loads(urllib2.urlopen(geomUrl, geomParams).read())

        intersectReturn = str(geomData['geometries'])
        finalReturn = intersectReturn.replace("u","")

        areaParams = urllib.urlencode({
        'polygons': finalReturn,
        'sr':"26915",
        'lengthUnit': "9035",
        'areaUnit':'{"areaUnit":"esriAcres"}',
        'type': "preserveShape",
        'f':"json"
        })

        areaData = json.loads(urllib2.urlopen(areaUrl, areaParams).read())
        area = str(areaData['areas'])
        acres = str("'ACRES':"+area[1:-1])

        featureAttributes =  feature['attributes']
        featureAttributes['ACRES'] = area[1:-1]

        data.append(feature['attributes'])

    #Create the JSON format and return
    jDict = json.dumps(data)
    return(jDict)

#Main Code Block
#-----------------------
#Create instance for storage
form = cgi.FieldStorage()

#get parameters
finalGeo = form.getvalue('geo')
featureName = form.getvalue('featureName')

if featureName == 'Regions':
    theDataUrl = 'http://2k8salmon1:6080/arcgis/rest/services/landview2014/mndnr_adminfeatures/MapServer/1/query'
elif featureName == 'Enforcement':
    theDataUrl = 'http://2k8salmon1:6080/arcgis/rest/services/landview2014/mndnr_adminfeatures/MapServer/4/query'
elif featureName == 'Fisheries':
    theDataUrl = 'http://2k8salmon1:6080/arcgis/rest/services/landview2014/mndnr_adminfeatures/MapServer/1/query'
elif featureName == 'Forestry':
    theDataUrl = 'http://2k8salmon1:6080/arcgis/rest/services/landview2014/mndnr_adminfeatures/MapServer/1/query'
elif featureName == 'ParksTrails':
    theDataUrl = 'http://2k8salmon1:6080/arcgis/rest/services/landview2014/mndnr_adminfeatures/MapServer/1/query'
elif featureName == 'Waters':
    theDataUrl = 'http://2k8salmon1:6080/arcgis/rest/services/landview2014/mndnr_adminfeatures/MapServer/1/query'
elif featureName == 'Wildlife':
    theDataUrl = 'http://2k8salmon1:6080/arcgis/rest/services/landview2014/mndnr_adminfeatures/MapServer/1/query'
else:
    theDataUrl = ''

print buildJSONReturn(theDataUrl, finalGeo)  #function for getting json query return
