import cv2
import winsound   # for beep feedback on Windows

def posture_monitor():
    # Connect to laptop camera
    cap = cv2.VideoCapture(0)

    # Load Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not accessible")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        posture = "Unknown"

        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Rule: if face is too low → bad posture
            if y > 250:
                posture = "Bad"
                print("⚠️ Bad posture detected!")
                winsound.Beep(1000, 300)   # short beep alert
            else:
                posture = "Good"
                print("✅ Good posture")

        # Show posture status on screen
        cv2.putText(frame, f"Posture: {posture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Smart Cognitive Load Desk - Webcam", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the posture monitor
posture_monitor()