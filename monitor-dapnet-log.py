import datetime
import json
import os
import re
import requests
import time



def getSettings(json_file):

  with open(json_file) as settings_file:
    file_contents = settings_file.read()

  return json.loads(file_contents)



def follow(thefile, seekToEnd, currentDate):
  '''generator function that yields new lines in a file
  '''
  # seek the end of the file

  if seekToEnd:                                                                 # Seek to the end of the file. But only on the first file of the run.
    thefile.seek(0, os.SEEK_END)
        
  # start infinite loop
  while True:

    line = thefile.readline()                                                   # Read the next line of the file

    if not line:                                                                # What if there isn't one?
      if currentDate != getCurrentDate():                                       # If we've gone into a new day, break out of this loop
        yield "It's a new day!"
        break

      time.sleep(1)                                                             # Wait for one second and try again in a bit.
      continue

    yield line                                                                  # Return the line received from the file

def getCurrentDate():
  return datetime.date.today().strftime('%Y-%m-%d')
  

def waitForTodaysFileToExist(filename, currentDate):

  fileExists = False
  checkCurrentDate = getCurrentDate()
  
  while checkCurrentDate == currentDate and not fileExists:
  
    fileExists = os.path.exists(filename)
    time.sleep(1)
    checkCurrentDate = getCurrentDate()

  return fileExists


def extractMessage(message_text):
  
  # Checking for Message
  p = re.compile(settings["regex"]["message"])
  r = p.findall(message_text)

  message = {}

  if r:


    message["type"] = "M"
    message["date"] = r[0][0]
    message["ric"] = r[0][1]
    message["text"] = r[0][2]

    message["subject"] = "Message via DAPNET"
    message["body"] = message["text"]
    message["tags"] = "spiral_notepad, dapnet, message, ric-" + message["ric"]
    message["priority"] = 3


  # Checking for Error
  p = re.compile(settings["regex"]["error"])
  r = p.findall(message_text)

  if r:

    message["type"] = "E"
    message["date"] = r[0][0]
    message["ric"] = "0000000"
    message["text"] = r[0][1]

    message["subject"] ="ERROR FROM DAPNET"
    message["body"] = "[" + message["date"] + "] " + message["text"]
    message["tags"] = "rotating_light, dapnet, error, urgent"
    message["priority"] = 5


  # Checking for Debug
  p = re.compile(settings["regex"]["debug"])
  r = p.findall(message_text)

  if r:

    message["type"] = "D"
    message["date"] = r[0][0]
    message["ric"] = r[0][1]
    message["text"] = r[0][2]

    message["subject"] = "Debug via DAPNET"
    message["body"] = message["text"]
    message["tags"] = "gear, dapnet, debug, ric-" + message["ric"]
    message["priority"] = 1

  return message


def sendToNtfy(message, endpoint):
  
  ntfy_headers = {}

  ntfy_headers["Tags"] = message["tags"]
  ntfy_headers["Priority"] = str(message["priority"])
  ntfy_headers["Title"] = message["subject"]

  response = requests.post(endpoint,
    data = message["body"],
    headers = ntfy_headers)

  response_text = str(response.status_code)

  print ("[" + response_text + "]")


def infoMessage(infotype, **kwargs):
  logfile = kwargs.get('optional', None)

  message = {}
  
  message["ric"] = "0000000"
  message["text"] = ""
  message["type"] = "I"
  send = False

  if infotype == "online":

      message["subject"] = "DAPNET ntfy pager online"
      message["body"] = "Monitoring for DAPNET calls"
      message["tags"] = "wave, ntfy, online"
      message["priority"] = 3
      send = True

  elif infotype == "logfile":
  
      message["subject"] = "Monitoring logfile"
      message["body"] = logfile
      message["tags"] = "floppy_disk, ntfy, logfile"
      message["priority"] = 1
      send = True

  else:

      print("invalid infotype")


  if send:
    sendMessage(message)



def sendMessage(message):

  print(message)
  
  for profile in settings["profiles"]:

    isAddressableToTargetProfile = False
    isTargetProfileEnabled = False

    # The rules here are a little complex, but to determine whether a message can potentially be sent to a given user:
    #   a. the type needs to contained within the enabled message types within the profile, AND any of:
    #     x. the target RIC is same as that in the profile, or
    #     y. the text contains the same callsign as that in the profile, or
    #     z. the message type is I (information) or E (error)
    if message["type"] in settings["profiles"][profile]["messagetypes"]:

      if message["ric"] == settings["profiles"][profile]["ric"] \
      or ( 
          message["text"].upper().find(settings["profiles"][profile]["call"]) >= 0
          and
          settings["profiles"][profile]["alertoncall"] 
          and
          message["ric"] != "0000008"
          ) \
      or message["type"] in ["I", "E"]:
        
        isAddressableToTargetProfile = True

    if settings["profiles"][profile]["enabled"]:
      isTargetProfileEnabled = True

    if isAddressableToTargetProfile == True and isTargetProfileEnabled == True and message["ric"] != "0000008":
      print(settings["profiles"][profile])
      sendToNtfy(message, settings["profiles"][profile]["endpoint"])


  

if __name__ == '__main__':

  settings = getSettings("config.json")

  infoMessage("online")

  seekToEnd = True                                                              # First iteration, so we start from the end of the logfile

  while True:

    currentDate = getCurrentDate()

    filename = settings["logfile"]["path"] + \
        settings["logfile"]["format"].replace("{date}", currentDate)            # Get the actual filename based on the current date 
    
    infoMessage("logfile", optional = filename)

    fileExists = waitForTodaysFileToExist(filename, currentDate)                # Sit here and wait until the file actually exists
                                                                                #     (or the current date changes again)

    if fileExists:                                                              # If the file ever turns up for this day, start to process it
                                                                                # otherwise, move on to the next iteration for the new day

      logfile = open(filename,"r")                                              # Open the file for reading
      loglines = follow(logfile, seekToEnd, currentDate)                        # Create the generator

      for line in loglines:                                                     # Iterate the generator - THIS IS THE PRIMARY WORK LOOP

        if getCurrentDate() != currentDate:                                     # If it's a new day, break out and look for the new file
          break;

        # THIS IS WHERE THE WORK GETS DONE
        settings = getSettings("config.json")                                   # Force reload of settings, this should prevent the need 
                                                                                # to restart the application after a profile change
        
        message = extractMessage(line)                                          # Get the message details out of the log line
        sendMessage(message)                                                    # Send the message out (if appropriate)


    seekToEnd = False                                                           # Because, at this point, we'd be looking for a new file, we
                                                                                # don't want to skip to the end of it so we get everything

