#!/usr/bin/env python
import sys
from asterisk.agi import *
import MySQLdb
from sys import argv
import os,datetime
"""

Determine the Caller ID and Campaign Code based on the calling number. 
Start Recording and Make Call. 

"""
__author__ = 'Justin Zimmer'

def log(msg):
    open('/tmp/unicorepbx.agi.log','ab+',512).write(
        "%s: %s\n"%(datetime.datetime.now(),msg)
    )


log("This is the first log: %s" % argv)
# def startAGI():
  #dbHost = agi.get_variable("UDDBHOST")
dbHost = argv[1]
  #dbUser = agi.get_variable("UDDBUSER")
dbUser = argv[2]
  #dbPass = agi.get_variable("UDDBPASS")
dbPass = argv[3]
  #dbDB = agi.get_variable("UDDBDB")
dbDB = argv[4]
agi = AGI()
log("AGI Called!")
agi.verbose("UniDial PBX Dial Started...")
log("Getting xliteExt...")
xliteExt = agi.env['agi_callerid']
log("Getting dialedNum...")
dialedNum = agi.env['agi_extension']
log("Sending verbose 1...")
agi.verbose("Collecting Caller ID and Campaign for %s" % xliteExt)
log("AGI Connected: %s, %s" % (xliteExt, dialedNum))
try:
  agi.verbose("Connecting to: mysql://%s:%s@%s/%s..." % (dbUser, dbPass, dbHost, dbDB))
  log("Connecting to: mysql://%s:%s@%s/%s..." % (dbUser, dbPass, dbHost, dbDB))
  db = MySQLdb.connect(host=dbHost, user=dbUser,
                         passwd=dbPass, db=dbDB)
except:
  log("I'm sorry, I couldn't connect to your database!")
  agi.verbose("I'm sorry, I couldn't connect to your database!")
  agi.stream_file('cannot-complete-network-error')
  agi.hangup()
  exit(1)

c = db.cursor()
aniQuery = "SELECT campaign, outani, emp_id FROM CELLANI WHERE xliteID='%s';" % xliteExt
log(aniQuery)
c.execute(aniQuery)
result = c.fetchone()
if result is None:
  agi.verbose("Something went wrong!!! Result Empty! ABORT! ABORT!")
  c.close()
  db.close()
  agi.stream_file('cannot-complete-network-error')
  agi.hangup()
  exit(1)
else:
  campaign = result[0]
  outANI = result[1]
  empID = result[2]
  agi.set_callerid(outANI)
  agi.set_variable("CAMPAIGN", campaign)
  agi.set_variable("EMPLOYEE", empID)
  agi.verbose("UniDial PBX Query complete: CAMPAIGN=%s, CALLERID(num)=%s, EMPLOYEE=%s" % (campaign, outANI, empID))
  sys.exit()


# startAGI()
  # while True:
  #   # agi.stream_file('vm-extension')
  #   # result = agi.wait_for_digit(-1)
  #   # agi.verbose("got digit %s" % result)
  #   # if result.isdigit():
  #   #   agi.say_number(result)
  #   # else:
  #   #  agi.verbose("bye!")
  #   #  agi.hangup()
    
  #   sys.exit()
