# Mapping class

import pandas as pd

class MAPPING():
  EXCELFILE = None
  EXCELFILE_NAME = ''
  EXCELFILE_DATA = None

  def __init__(self, excel_file_name="crazy_excel_mapping.xlsx"):
      self.EXCELFILE_NAME = excel_file_name
      self.EXCELFILE = pd.ExcelFile(self.EXCELFILE_NAME)
      self.EXCELFILE_DATA = self.getMappingList()

  def getMappingList(self):
      """Return mappings of subscriptionsname"""
      dfs = {sheet_name: self.EXCELFILE.parse(sheet_name) for sheet_name in self.EXCELFILE.sheet_names}
      ret = {'map_data':[]}
      array_1 = dfs['json_sub_info']['sub_short']
      array_2 = dfs['json_sub_info']['subscriptionname']
      array_3 = dfs['json_sub_info']['subscriptionid']

      length = len(array_1)
      # iterate of list with index
      # same as 'for i in range(len(list))'
      for i in range(length):
        ret_data = {'mic_sub_short': array_1[i], 'subscriptionname': array_2[i], 'subscriptionid': array_3[i]}
        ret['map_data'].append( ret_data )
      return ret

if __name__ == "__main__":
    qualys_mapping = MAPPING("crazy_excel_mapping.xlsx")
    foobar = qualys_mapping.getMappingList()
    #foobar['map_data']



