# A little script to email me when a course has an open seat so I can register.

import urllib2
import re
import time
import smtplib
import string
         
def sendEmail(text):
    username = 'example@gmail.com'
    password = 'password'
     
    SUBJECT = ""
    FROM = username
    TO = 'adrien.emery@gmail.com'
    TEXT = text
    BODY = string.join((
            "From: %s" % FROM,
            "To: %s" % TO,
            "Subject: %s" % SUBJECT ,
            "",
            TEXT
            ), "\r\n")
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    
    server.sendmail(FROM, TO, BODY)
        
    server.quit()   

response = urllib2.urlopen('https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=CHBE&course=459&section=201')
html = response.read()

match = re.search(r'Status: (\w*)', html)

course_dict = {'ENPH STT':'https://courses.students.ubc.ca/cs/main?pname=sttcode&tname=sttcode&dept=BASC&spec=ENPH5&sttcode=93934',
               'CHBE 459':'https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=CHBE&course=459&section=201'}

course_status = {'ENPH STT':'Full',
                 'CHBE 459':'0'}


url = course_dict['CHBE 459']
response = urllib2.urlopen(url)
html = response.read()

status = None

while True:

    for key in course_dict:
        response = urllib2.urlopen(course_dict[key])
        html = response.read()
        
        if 'STT' in key:
            match = re.search(r'Status: (\w*)', html)
            
            if not match.group(1) == 'Full':
                status = 'Open'
                # send email notifictaion
                sendEmail(key + ' - Status:' + status)
                #print key + ' - Status:' + status
            else:
                status = 'Full'
                # send email notifictaion
                #print key + ' - Status: ' + status
        else:
            match = re.search(r'General Seats Remaining:</td><td align=left><strong>(\d*)</strong>', html)
            
            if match:
                #print key + ' - Seats: ' + match.group(1)
                
                # send email if seats available > 0
                if float(match.group(1)):
                    sendEmail(key + ' - Seats: ' + match.group(1))                
    
    # wait 30 seconds
    time.sleep(30)
            
        
    