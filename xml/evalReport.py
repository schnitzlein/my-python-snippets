from xml.dom import minidom

XMLDatei = minidom.parse ("report_response.xml")

Ebene1 = XMLDatei.getElementsByTagName("SCAN_LIST")

# SCAN
Ebene2_Namen = Ebene1[0].childNodes

# TITLE, REF, USER_LOGIN, LAUNCH_DATETIME, DURATION, PROCESSING_PRIORITY, PROCESSED, STATUS, TARGET 
#Ebene3_Namen = Ebene2_Namen.childNodes
#for node in Ebene3_Namen:
#    if (node == "TITLE"):
#        print(Namen)

scans = XMLDatei.getElementsByTagName("SCAN")
for scan in scans:
    title = scan.getElementsByTagName("TITLE")[0]
    scan_ref = scan.getElementsByTagName("REF")[0]
    print("TITLE: {}, scan_ref: {}".format(title.firstChild.data, scan_ref.firstChild.data))
