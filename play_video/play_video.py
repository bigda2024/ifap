import cv2
import threading

class VideoPlayer:
    def __init__(self, video_path):
        self.video_path = video_path
        self.playing = False

    def play_video(self):
        if not self.video_path:
            print("No video file selected.")
            return

        self.playing = True

        def run():
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                print("Cannot open video file.")
                return

            while cap.isOpened() and self.playing:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow('Video', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            self.stop_video()

        # Run the video playback in a separate thread to avoid blocking
        threading.Thread(target=run).start()

    def stop_video(self):
        self.playing = False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python app.py <path_to_video>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    player = VideoPlayer(video_path)
    player.play_video()
