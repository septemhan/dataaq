#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import numpy as np
import time


#Pin define
#ADC pin define
Clock = 16
Address = 20
DataOut = 21
#GPIO define

#Sensor Pin define
sensor_dict = {
0:"Temp0", #channel and name of the sensor
1:"Temp1",
2:"Temp2",
3:"Temp3",
4:"Temp4",
5:"Temp5",
6:"Temp6",
7:"Temp7",
}
#Glabal paramters:

ADCNow = [0,0,0,0,0,0,0,0,0]
StartStatus = False


def ADC_Read(channel):
	value = 0;
	for i in range(0,4):
		if((channel >> (3 - i)) & 0x01):
			GPIO.output(Address,GPIO.HIGH)
		else:
			GPIO.output(Address,GPIO.LOW)
		GPIO.output(Clock,GPIO.HIGH)
		GPIO.output(Clock,GPIO.LOW)
	for i in range(0,6):
		GPIO.output(Clock,GPIO.HIGH)
		GPIO.output(Clock,GPIO.LOW)
	time.sleep(0.001)
	for i in range(0,10):
		GPIO.output(Clock,GPIO.HIGH)
		value <<= 1
		if(GPIO.input(DataOut)):
			value |= 0x01
		GPIO.output(Clock,GPIO.LOW)
	return value

def ADC_Read_All():

	for channel in range (0,7):
		AdcNow[Channel] = ADC_Read(channel)
		
	#return AdcNow
	
def CreateFile():

	import datetime,os,sys
			
	unix_ts = time.localtime(time.time())  
	ts_format = format = '%Y-%m-%d %H:%M'  
	formatted_ts = time.strftime(format,unix_ts)
	pathname = os.path.dirname(sys.argv[0])
	abspath = os.path.abspath(pathname)
	os.chdir(abspath)

	series_dir = "TemperatureSeries"
	if not os.path.exists(series_dir):   #create a directory if the directry does not exist
		os.makedirs(series_dir)
					
	pathname = os.path.dirname(sys.argv[0])
	abspath = os.path.abspath(pathname)
	os.chdir(os.path.join(abspath,series_dir))

	today = datetime.datetime.today()
	SeriesFile = today.strftime('%m%d%Y') #get a string of date in format of "04182016"

	if not os.path.exists(SeriesFile):
		tempDataFile = open(SeriesFile,'w')
		tempDataFile.close()
	return SeriesFile
	
def WriteData(_SeriesFile,_ADCNow):

	try:
		tempDataFile = open(_SeriesFile,'a')
		if len(_ADCNow)==8:
			writeline = ''
			for d in _ADCNow:
				writeline = writeline+str(d)+','
			tempDataFile.write(str(formatted_ts)+','+writeline)
			tempDataFile.write('\n')
			tempDataFile.close()
	
	except IOError:
		print "unbale to create file"

	os.chdir(abspath)
	print " done add data to file "   
	
def WriteEndline(_SeriesFile):

	try:
	    endline1 = "---------------------------------------\n"
		endline2 = str(time.time())+"\n"
		endline3 = "---------------------------------------\n"
		tempDataFile = open(_SeriesFile,'a')
		
		tempDataFile.write(endline1)
		tempDataFile.write(endline2)
		tempDataFile.write(endline3)
		tempDataFile.close()

	except IOError:
		print "unbale to add endline"
			
def SendFilebyEmail(_SeriesFile,_emaill):
 
	import smtplib
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	from email.header import Header
	
	mail_host="smtp.163.com"  #host server
    mail_user="linchen_han@163.com"    #username
    mail_pass=""   #password 
	 
	sender = 'from@runoob.com'
	receivers = ['200565200@qq.com'] 
	 
	
	message = MIMEMultipart()
	message['From'] = Header("MPS Experiment Hub", 'utf-8')
	message['To'] =  Header("users", 'utf-8')
	subject = 'Transfer data from hub to user by emails'
	message['Subject'] = Header(subject, 'utf-8')
	 
	#main body
	message.attach(MIMEText('This email is used to tranfer data from MPS experiment hub to user by emails', 'plain', 'utf-8'))
	 
	#adding attachment
	series_dir = "TemperatureSeries"
	pathname = os.path.dirname(sys.argv[0])
	abspath = os.path.abspath(pathname)
	os.chdir(os.path.join(abspath,series_dir))
	today = datetime.datetime.today()
	FileName = today.strftime('%m%d%Y')
	
	att1 = MIMEText(open(FileName, 'rb').read(), 'base64', 'utf-8')
	att1["Content-Type"] = 'application/octet-stream'
	# adding the name of the attachment
	att1["Content-Disposition"] = 'attachment; filename=FileName'
	message.attach(att1)
	 

	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host, 25)
		smtpObj.login(mail_user,mail_pass)
		smtpObj.sendmail(sender, receivers, message.as_string())
		print "Email successfully sent"
	except smtplib.SMTPException:
		print "Error: cannot send emails"
		
	
def start(_duration=10):
	time_start = time.time()
	while(time.time()-time_start)<=_duration):
	    try:
			ADC_Read_All()
			print AdcNow
			time.sleep(0.01)
			#WriteData(SeriesFile,ADCNow)
		except Exception,e:
		    print "Catch error at timestamp: s%" %formatted_ts
			print str(e)
			
	#WriteEndline(SeriesFile)
	

	


def main():
	#initialize GPIO
	print "initialize GPIO"
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(Clock,GPIO.OUT)
	GPIO.setup(Address,GPIO.OUT)
	GPIO.setup(DataOut,GPIO.IN,GPIO.PUD_UP)
	
	
	#creating file for data storage
	SeriesFile = CreateFile()
	duration = 10 #unit in secnd
	
	#get start time
	unix_ts = time.localtime(time.time())  
	time_start = time.time()
	ts_format = format = '%Y-%m-%d %H:%M'  
	formatted_ts = time.strftime(format,unix_ts)	
	print "Task starts at %s" %formatted_ts
	
	#start a job
	start(duration)
	
	#stop GPIO pin
	GPIO.cleanup()
	
	

if __name__=='__main__':
    main()

