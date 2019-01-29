#!/home/rasil/anaconda3/bin/python


import speech_recognition as sr 
##from translation import google, ConnectError
from py_translator import Translator
from gtts import gTTS
import os
from os import path
import subprocess
import time

print("...starting...")

r = sr.Recognizer()
#while 1:

path1 = os.path.dirname(path.abspath(__file__))
print(path1)

#remove files rawaudio and rawvideo

delcmd = "rm "+path1+"/raw*"
subprocess.call(delcmd, shell=True)
print("rawaudio and rawvideo deleted ")


delcmd = "rm "+path1+"/start.txt "+path1+"/tmp.txt "+path1+"/duration.txt "
subprocess.call(delcmd,shell=True)

#extracting audio from video

cmdToGetVideofile = "ls  "+path1+"/videos/"
videoFileName = subprocess.check_output(cmdToGetVideofile, shell=True)
videoFileName=str(videoFileName).strip("b'\\n'")

cmd_vid2aud = "ffmpeg -i "+path1+"/videos/"+videoFileName+" -ab 32k -ac 1 -ar 44100 -vn "+path1+"/rawaudio.wav -y > /dev/zero"
cmd_video = "ffmpeg -i " + path1 + "/videos/"+videoFileName+" -an -c copy " +path1+"/rawvideo.mp4 -y" 
subprocess.call(cmd_vid2aud, shell=True)
subprocess.call(cmd_video, shell=True)

# calling audioSplit script
time.sleep(1)
import audioSplit
time.sleep(1)
#audioSplit


sortedFiles = sorted(os.listdir(path1 + '/split'))


j=0

for i in sortedFiles:

	eachFile = str(i)
	with sr.AudioFile(path1+'/split/'+eachFile) as source:
		audio = r.record(source)
		print('test {0}'.format(j))
	try:
		
		hindi =  r.recognize_google(audio)
		print(hindi)
		english = Translator().translate(text=hindi, dest='en').text
		print(english)
		tamil = Translator().translate(text=english, dest='ta').text
		print(tamil)
		speakobj = gTTS(text=tamil, lang='ta', slow=False)
		speakobj.save(path1+"/tamilAudio/"+str(j)+".wav")

		
	except:

		#check duration of skipped file and add a silent audio instead

		DurChkCmd = "ffmpeg -i "+path1+"/split/"+str(j)+".wav 2>&1 | grep Duration |  cut -d ' ' -f 4 | sed s/,//"
		DurChkCmd = subprocess.check_output(DurChkCmd,shell=True)
		DurChkCmd = str(DurChkCmd).strip("b'\\n'")
		DurCreateCmd = "ffmpeg -ar 48000 -t "+DurChkCmd+" -f s16le -acodec pcm_s16le -ac 1 -i /dev/zero -acodec libmp3lame -aq 4 "+path1+"/tamilAudio/"+str(j)+".wav -y  > /dev/null 2> /dev/null & "
		print(DurCreateCmd)
		subprocess.call(DurCreateCmd, shell = True)
		print("empty file created with duration: "+DurChkCmd)
		pass

	j=j+2

#merge audio

time.sleep(1)
import merge
time.sleep(1)

print("--------Done--------")


