from common.models import ClerkProfile  # Assuming ClerkProfile is defined in the common app
import face_recognition
import cv2
import numpy as np
from datetime import datetime
from common.models import Attendance  # Import the Attendance model

# Fetch all clerks from the ClerkProfile
clerks = ClerkProfile.objects.all()

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Get the current date for session marking
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# Store the known face encodings and names
known_face_encodings = []
known_face_names = []
known_face_ids = []  # Store employee IDs for marking attendance

# Loop through each clerk to load their image and encode faces
for clerk in clerks:
    user_id = clerk.user.id  # Fetch user ID
    profile_image_url = clerk.profile_image.url if clerk.profile_image else None

    if profile_image_url:  # If the clerk has a profile image
        image = face_recognition.load_image_file(profile_image_url)  # Load the profile image
        image_encoding = face_recognition.face_encodings(image)  # Get face encoding
        
        if image_encoding:  # If a face encoding exists for the image
            known_face_encodings.append(image_encoding[0])  # Store the face encoding
            known_face_names.append(clerk.user.username)  # Store the clerk's name
            known_face_ids.append(user_id)  # Store the clerk's ID

# Initialize clerk set to mark attendance dynamically
clerk_set = set(known_face_names)

# Loop through the webcam feed to capture faces
while clerk_set:  # Run loop only if there are clerks left to mark
    ret, frame = video_capture.read()
    if not ret:
        print("❌ ERROR: Failed to capture video frame. Check your webcam.")
        break

    # Resize and convert the frame to RGB (for face_recognition)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")

    if face_locations:
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)  # Compare faces
            name = "Unknown"

            # Calculate the face distance and find the best match
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                user_id = known_face_ids[best_match_index]

                # Mark attendance if the clerk is present
                if name in clerk_set:
                    clerk_set.remove(name)  # Remove from the set after marking present
                    print(f"✅ Attendance marked for {name} (ID: {user_id})")

                    # Create an attendance record in the database
                    current_time = now.strftime("%H:%M:%S")
                    session = "Morning" if now.hour < 12 else "Afternoon"  # Determine session

                    # Save attendance in the database using the ForeignKey
                    attendance_entry = Attendance.objects.create(
                        employee_id=user_id,  # Store the employee ID
                        employee_name=name,  # Store the employee name
                        date=now.date(),
                        time=now.time(),
                        session=session,
                        status="Present"
                    )

    # Display webcam feed
    cv2.imshow("Attendance System", frame)

    # Press 'q' to exit manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("🎉 All clerks marked present. Exiting...")
video_capture.release()
cv2.destroyAllWindows()
