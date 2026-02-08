import cv2
from deepface import DeepFace
import pygame
import os
import random
import time

pygame.mixer.init()

emotion_music = {
    "happy": "songs/happy",
    "sad": "songs/sad",
    "angry": "songs/angry",
    "neutral": "songs/neutral",
    "surprise": "songs/happy"
}

last_emotion = None
last_play_time = 0

def play_music(emotion):
    folder = emotion_music.get(emotion, "songs/neutral")
    print("Emotion:", emotion)
    print("Folder path:", folder)

    if not os.path.exists(folder):
        print("❌ Folder does not exist")
        return

    songs = os.listdir(folder)
    print("Songs found:", songs)

    if songs:
        song = random.choice(songs)
        path = os.path.join(folder, song)

        print("Trying to play:", path)

        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    else:
        print("❌ No songs in folder")



cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']

        cv2.putText(frame, emotion, (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,255,0), 2)

        now = time.time()

        # play only if emotion changed and 10 sec passed
        if emotion != last_emotion and now - last_play_time > 10:
            play_music(emotion)
            last_emotion = emotion
            last_play_time = now

    except:
        pass

    cv2.imshow("Emotion Music Player", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
