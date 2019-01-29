#!/home/rasil/anaconda3/bin/python


import os
import subprocess
from os import path
import time

print("...starting audio spliting...")

filePath = os.path.dirname(path.abspath(__file__))

#remove files in folders split and tamilAudio

delcmd = "rm "+filePath+"/split/*"
subprocess.call(delcmd, shell=True)
print(delcmd)

delcmd = "rm "+filePath+"/end.txt"
subprocess.call(delcmd, shell=True)

delcmd = "rm "+filePath+"/start.txt"
subprocess.call(delcmd, shell=True)

delcmd = "rm "+filePath+"/tamilAudio/*"
subprocess.call(delcmd, shell=True)


#silence_start
silenceStart = "ffmpeg -i "+filePath+"/rawaudio.wav -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1 | grep silence_start | awk '{print $5}'  | awk '!/size/' | awk '!/time/' | awk '!/silence/'  | sed -e 's/[-]/ /g;s/  */ /g' > start.txt"
subprocess.call(silenceStart, shell=True)
#time.sleep(1)
print("start.txt file created")


#silence end
#time.sleep(1)
silenceEnd = "ffmpeg -i "+filePath+"/rawaudio.wav -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1 | grep silence_duration | awk '{print $5}'  | awk '!/size/' | awk '!/time/' | awk '!/silence/' > tmp.txt"
subprocess.call(silenceEnd, shell=True)
time.sleep(1)
print("tmp.txt file created")

#silence duration
silenceDurCmd = "ffmpeg -i rawaudio.wav -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1 | grep silence_duration | awk '{print $8}'  | awk '!/size/' | awk '!/time/' | awk '!/silence/' > duration.txt"
subprocess.call(silenceDurCmd, shell=True)
time.sleep(1)
print("duration.txt file created")

tempfile = open("end.txt" , "w")
tempfile.write("0\n")
tempfile.close();
 
tempfileopen = filePath+"/tmp.txt"
endFileopen = filePath+"/end.txt"
with open(tempfileopen) as first, open(endFileopen , "a") as second:
	for line in first:
		second.write(line)

first.close()
second.close()
print("end.txt file created")


#Spliting Audio
startFile = filePath+"/start.txt"
endFile = filePath+"/end.txt"
durFile = filePath+"/duration.txt"
i=0
a=1
with open(startFile) as StartFileOpen, open(endFile) as endFileOpen ,open(durFile) as durFileOpen:

	for eachLineStart , eachLineEnd , eachLineDur in zip(StartFileOpen, endFileOpen, durFileOpen):

		xStart = eachLineStart.rstrip()
		print("xStart = {}".format(xStart))
		xStartFloat = float(xStart)
		xEnd = eachLineEnd.rstrip()
		xEndFloat = float(xEnd)
		xDur = xStartFloat - xEndFloat
		if xDur > 30:
			
			temp1 = xDur/24
			temp1 = round(temp1)
			print("original duration = {}".format(xDur))
			print("rounded value = {}".format(temp1))
			x1 = xEndFloat 
			temp2 = xDur/temp1
			print("duration = {}".format(temp2))
			x1 = xEndFloat 

			
			while x1 < xStartFloat:
				
				xEnd = str(x1).rstrip()
				xEndFloat = x1
				xDurFloat = str(temp2).rstrip()
				j=str(i)
				ffmpegSplitCmd = "ffmpeg -i "+filePath+"/rawaudio.wav -ss " + xEnd + " -t " + xDurFloat + " -async 1 " + filePath + "/split/"+j+".wav -y  > /dev/null 2> /dev/null &  "
				print("file {}".format(i))
				print(ffmpegSplitCmd)
				subprocess.call(ffmpegSplitCmd, shell=True)
				i+=1	
				x1 = xEndFloat + temp2
			xDur = 32
			
			
		else:
			
			print("duration = {}".format(xDur))
			xDurFloat = str(xDur).rstrip()
			j=str(i)
			ffmpegSplitCmd = "ffmpeg -i "+filePath+"/rawaudio.wav -ss " + xEnd + " -t " + xDurFloat + " -async 1 " + filePath + "/split/"+j+".wav -y  > /dev/null 2> /dev/null &  "
			print("file {}".format(i))
			print(ffmpegSplitCmd)
			subprocess.call(ffmpegSplitCmd, shell=True)
			i+=1
			

		k=str(a)
		eachLineDur = eachLineDur.rstrip()
		DurCreateCmd = "ffmpeg -ar 48000 -t "+eachLineDur+" -f s16le -acodec pcm_s16le -ac 1 -i /dev/zero -acodec libmp3lame -aq 4 "+ filePath + "/tamilAudio/"+k+".wav -y  > /dev/null 2> /dev/null & "
		print(DurCreateCmd)
		subprocess.call(DurCreateCmd, shell = True)
		a+=2

StartFileOpen.close()
endFileOpen.close()
			
print("File spliting completed")
    

    


print("Audio spliting ends")
