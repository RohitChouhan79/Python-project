# Thi project For Download youtube vidio and audio by link

#import pytube
from pytube import YouTube

#create two input for link and and chosing option of audio and vidio
link=input("please provide your youtube link")
check=input("press 1 for vidio and press 2 for audio")

#  We have use if option for download vidio and audio
#there if="1" use for vidio 
if check=="1":
    youtube_1=YouTube(link)
    videos=youtube_1.streams.filter(progressive=True)
    vid=list(enumerate(videos))
    
    for i in vid:
        print(i)
    strm=int(input("Provide which stream you want to download"))
    videos[strm].download()
    print("successfully download")
 # this code for download youtube audio  
if check=="2":
    youtube_1=YouTube(link)
    audio=youtube_1.streams.filter(only_audio=True)
    aud=list(enumerate(audio))
    
    for i in aud:
        print(i)
    strm=int(input("Provide which stream you want to download"))
    audio[strm].download()
    print("successfully download")
