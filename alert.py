from AiologySimilarity import Similarity
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
from os import environ
import cv2 as cv

class Alarm:
    def __init__(self,ffmpeg_folder_path : str,clear_image : str | None = None,sesivity : int = 95):
        self.similarity = Similarity()
        self.camera = cv.VideoCapture(0)

        environ["PATH"] += f";{ffmpeg_folder_path}"
        self.file = AudioSegment.from_mp3("alert_sound.mp3")

        if clear_image == None:
            self.main_image = self.camera.read()[1]
            self.main_image = cv.resize(self.main_image , (500,500))
        else:
            self.main_image = cv.imread(clear_image)

        self.sensivity = sesivity

    def play_alarm(self):
        play(self.file)

    def start(self):
        start = False

        try:
            while True:
                frame = self.camera.read()[1]
                frame = cv.resize(frame , (500,500))

                if start:
                    detected , _= self.similarity.check_frames(frame,self.main_image,self.sensivity)

                    if not detected:
                        Thread(target=self.play_alarm,daemon=True).start()
                        cv.putText(frame,"Detection !!",(20,50),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)
                    else:
                        cv.putText(frame,"Normal",(20,50),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),1)

                cv.imshow("Review window",frame)
                cv.waitKey(10)

                start = True
        except KeyboardInterrupt:
            pass

        self.camera.release()
        cv.destroyAllWindows()

Alarm("",sesivity=95).start()