import cv2, mediapipe

cap = cv2.VideoCapture(0)
cameraWidth, cameraHeight = 640,360

mpHands = mediapipe.solutions.hands
hands = mpHands.Hands()
mpDraw = mediapipe.solutions.drawing_utils

#Get the gesture of hand move.
def getMove(landmarks,app):
    event = []
    #if the hand is upward, return 'hi' just for test case
    if landmarks[0].y > landmarks[9].y: 
        event.append('Hi') 
    #if the hand is downward and 4th, 5th fingers are curled:
    elif landmarks[16].y < landmarks[14].y and landmarks[20].y < landmarks[18].y:
        #Check if walk or not
        app.handX = app.width * (1-landmarks[5].x) 
        if landmarks[8].y < landmarks[11].y and landmarks[12].y > landmarks[11].y:
            event.append('Left') 
        elif landmarks[8].y > landmarks[7].y and landmarks[12].y < landmarks[7].y:
            event.append('Right') 
        elif landmarks[8].y > landmarks[5].y and landmarks[12].y > landmarks[9].y:
            event.append('Ready') 
        #Check if attach or not, based on thumb position.
        if (landmarks[4].x - landmarks[3].x > 0.015 and app.handChoice == 'Left') or (
            landmarks[4].x - landmarks[3].x < -0.015 and app.handChoice == 'Right'):
            event.append('Attack') 
    return event
    
def handMove(app):
    success, img = cap.read()
    img = cv2.resize(img,(cameraWidth, cameraHeight))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    ### wrapper of hand tracking studied from
    ### https://youtu.be/NZde8Xt78Iw 
    if results.multi_hand_landmarks:
        for handType in results.multi_handedness:
            app.handChoice = handType.classification[0].label
        for handLandmarks in results.multi_hand_landmarks:
            events = getMove(handLandmarks.landmark,app)
            for event in events: app.handEventSet.add(event)
            for id, landMark in enumerate(handLandmarks.landmark):
                height, width, channel = img.shape
                cx, cy = int(landMark.x * width), int(landMark.y * height)
                cv2.circle(img, (cx,cy), 7, (234,230,47), cv2.FILLED)
                #See ids
                # cv2.putText(img, str(id), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),3)
            mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

    #Mirror like: 
    img = cv2.flip(img,1)

    cv2.imshow("Camera", img)

