import enum
import datetime
import re


class CadocsIntents(enum.Enum):
   GetSmells = "get_smells"
   GetSmellsDate = "get_smells_date"
   Report = "report"
   Info = "info"

def valid_link(url):
   re_equ = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
   ck_url = re.findall(re_equ, url)
   if ck_url:
      return True
   else:
      return False

def valid_date(date):
   rs_date = re.findall('\d{2}/\d{2}/\d{4}',date)
   if(rs_date):
      ls = rs_date[0].split("/")

      is_correct = None

      try:
         newDate = datetime.datetime(int(ls[2]),int(ls[0]),int(ls[1]))
         is_correct = True
      except ValueError:
         is_correct = False
      return is_correct
   return False