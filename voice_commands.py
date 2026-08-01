import speech_recognition as sr
import pyautogui
import subprocess
import webbrowser
from datetime import datetime
from voice import speak

recognizer = sr.Recognizer()


def listen():

    try:

        with sr.Microphone() as source:

            

            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
    source,
    timeout=2,
    phrase_time_limit=3
)

            command = recognizer.recognize_google(audio)

            command = command.lower()

            

            return command

    except Exception as e:

        print(e)

        speak("Sorry, I couldn't hear you.")

        return ""


def process_voice_command():

    speak("Listening")

    command = listen()

    if command == "":
        return

    # ----------------------------
    # CHROME
    # ----------------------------

    if "chrome" in command:

        speak("Opening Chrome")

        webbrowser.open("https://www.google.com")

    # ----------------------------
    # YOUTUBE
    # ----------------------------

    elif "youtube" in command:

        speak("Opening YouTube")

        webbrowser.open("https://www.youtube.com")

    # ----------------------------
    # CHATGPT
    # ----------------------------

    elif "chatgpt" in command or "chat g p t" in command:

        speak("Opening Chat GPT")

        webbrowser.open("https://chat.openai.com")

    # ----------------------------
    # CALCULATOR
    # ----------------------------

    elif "calculator" in command or "calc" in command:

        speak("Opening Calculator")

        subprocess.Popen("calc.exe")

    # ----------------------------
    # NOTEPAD
    # ----------------------------

    elif "notepad" in command:

        speak("Opening Notepad")

        subprocess.Popen("notepad.exe")

    # ----------------------------
    # PAINT
    # ----------------------------

    elif "paint" in command:

        speak("Opening Paint")

        subprocess.Popen("mspaint.exe")

    # ----------------------------
    # FILE EXPLORER
    # ----------------------------

    elif "explorer" in command or "files" in command:

        speak("Opening File Explorer")

        subprocess.Popen("explorer.exe")

    # ----------------------------
    # SCREENSHOT
    # ----------------------------

    elif "screenshot" in command:

        filename = "Screenshot_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"

        pyautogui.screenshot(filename)

        speak("Screenshot saved")

    # ----------------------------
    # TIME
    # ----------------------------

    elif "time" in command:

        current = datetime.now().strftime("%I:%M %p")

        speak("Current time is " + current)

    # ----------------------------
    # VOLUME UP
    # ----------------------------

    elif "volume up" in command:

        for _ in range(5):
            pyautogui.press("volumeup")

        speak("Volume Increased")

    # ----------------------------
    # VOLUME DOWN
    # ----------------------------

    elif "volume down" in command:

        for _ in range(5):
            pyautogui.press("volumedown")

        speak("Volume Decreased")

    # ----------------------------
    # MUTE
    # ----------------------------

    elif "mute" in command:

        pyautogui.press("volumemute")

        speak("Muted")

    # ----------------------------
    # CLOSE WINDOW
    # ----------------------------

    elif "close window" in command:

        pyautogui.hotkey("alt", "f4")

        speak("Closing Window")

    # ----------------------------
    # GOOGLE SEARCH
    # ----------------------------

    elif command.startswith("search"):

        query = command.replace("search", "").strip()

        if query:

            speak("Searching " + query)

            webbrowser.open(
                "https://www.google.com/search?q=" + query
            )

    # ----------------------------
    # UNKNOWN COMMAND
    # ----------------------------

    else:

        speak("Sorry, I don't understand that command.")