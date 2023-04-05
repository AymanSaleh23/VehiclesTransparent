from string import punctuation
import cv2
import pytesseract
video = cv2.VideoCapture(0)
while True:
    # Load image
    ok, frame = video.read()
    frame = cv2.resize(frame, (980, 720))
    cv2.imshow("Live", frame)
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to make text more visible
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Apply image dilation to enhance characters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    # Apply OCR using Tesseract
    text = pytesseract.image_to_string(dilated, config='--psm 1').strip(punctuation)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # Print recognized text
    print(text)

video.release()
cv2.destroyAllWindows()
