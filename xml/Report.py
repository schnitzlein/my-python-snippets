# Qualys Report class

from xml.dom import minidom


class REPORT():
  XMLFILE = None
  XMLFILE_NAME = ''

  def __init__(self, xml_file_name="report_response.xml"):
      self.XMLFILE_NAME = xml_file_name
      self.XMLFILE = minidom.parse(self.XMLFILE_NAME)

  def getScanList(self):
      """Return the qualys API scanlist as dictionary, getScanList() -> dict[ (title, scan_ref) ]"""
      # scanlist_dict['scans'][i] with tuple (title, scan_ref)
      scanlist_dict = { "scans": [] }

      # TITLE, REF, USER_LOGIN, LAUNCH_DATETIME, DURATION, PROCESSING_PRIORITY, PROCESSED, STATUS, TARGET 

      scans = self.XMLFILE.getElementsByTagName("SCAN")
      for scan in scans:
          title = scan.getElementsByTagName("TITLE")[0]
          scan_ref = scan.getElementsByTagName("REF")[0]
          print("TITLE: {}, scan_ref: {}".format(title.firstChild.data, scan_ref.firstChild.data))

          myScanTuple = (title, scan_ref)

          scanlist_dict['scans'].append( myScanTuple )
      print("Number of Scans: {}".format( len(scanlist_dict['scans'])) )
      return scanlist_dict


if __name__ == "__main__":
    qualys_report = REPORT("report_response.xml")
    qualys_report.getScanList()
