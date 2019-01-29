#!/home/rasil/anaconda3/bin/python


import subprocess
import os
from os import path
import time


filePath = os.path.dirname(path.abspath(__file__))

delcmd = "rm "+filePath+"/fileName.txt"
subprocess.call(delcmd, shell=True)

delcmd = "rm "+filePath+"/tempName.txt"
subprocess.call(delcmd, shell=True)

makelist = "ls "+filePath+"/tamilAudio | sort -n > "+filePath+"/tempName.txt"
print(makelist)
subprocess.call(makelist,shell=True)

tmpfile = "touch "+filePath+"/fileName.txt"
subprocess.call(tmpfile,shell=True)

temp1 = filePath+"/tempName.txt"
temp2 = filePath+"/tamilAudio/fileName.txt"

with open(temp1) as temp, open(temp2, "a") as orgFile:
	for eachLine in temp:
		eachLine = eachLine.rstrip()
		orgFile.write("file '"+eachLine+"'\n")
temp.close()
orgFile.close()

#merging tamil audio files

mergeAudioCmd = "ffmpeg -f concat -i "+filePath+"/tamilAudio/fileName.txt -c copy "+filePath+"/tamilAudio/TamilAudio.wav -y  > /dev/null 2> /dev/null &"
print(mergeAudioCmd)
subprocess.call(mergeAudioCmd, shell=True)

#merging tamil audio with rawvideo
time.sleep(1)
mergeVideoCmd = "ffmpeg -i "+filePath+"/rawvideo.mp4 -i "+filePath+"/tamilAudio/TamilAudio.wav -c copy "+filePath+"/finalVideo.mkv -y  > /dev/null 2> /dev/null &"
print(mergeVideoCmd)
subprocess.call(mergeVideoCmd, shell=True)


















