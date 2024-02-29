import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
# print(voices)
engine.setProperty('rate',170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        # r.adjust_for_ambient_noise(source,1.2)
        audio = r.listen(source,0,4)

    try:
        print("Recognising...")
        query = r.recognize_google(audio,language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print(f"Say that again")
        return "None"
    return query


if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "start training" in query or "start raining" in query:
            speak("ok,sir")
            speak("which training you would like to do")
        
    
            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("ok sir , You can call me anytime")
                    break

                elif "left hand" in query:
                  speak("Let's start your left side hand doumble lifting,sir")
                  from left_hand_dumble_lifting import  perform_pose_left
                  perform_pose_left(hand = "left")

                elif "right hand" in query:
                  from right_hand_dumble_lifting import  perform_pose_right
                  speak("Let's start your right side hand doumble lifting,sir")
                  perform_pose_right(hand = "right", side = "right")

                elif "squat" in query:
                  from squat import  squat_counter
                  speak("Let's start your squat exercise,sir")
                  squat_counter()
        
                elif "exit" in query:
                  speak("exit in this programm, sir")
                  exit()





