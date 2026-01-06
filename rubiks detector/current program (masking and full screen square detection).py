import cv2
import numpy as np

# HSV color ranges for cube colors
COLOR_RANGES = {
    "white": ((0, 0, 200), (180, 50, 255)),
    "yellow": ((20, 100, 100), (35, 255, 255)),
    "red1": ((0, 100, 100), (10, 255, 255)),
    "red2": ((160, 100, 100), (180, 255, 255)),
    "orange": ((10, 100, 100), (20, 255, 255)),
    "blue": ((100, 150, 0), (130, 255, 255)),
    "green": ((40, 70, 70), (80, 255, 255))
}

def create_color_mask(hsv):
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for color, (low, high) in COLOR_RANGES.items():
        lower = np.array(low)
        upper = np.array(high)
        temp_mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.bitwise_or(mask, temp_mask)
    return mask

def get_largest_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    # largest contour
    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < 1000:
        return None
    return largest

def get_3x3_grid(rect):
    x, y, w, h = rect
    step_w, step_h = w//3, h//3
    centers = []
    for i in range(3):
        for j in range(3):
            cx = x + step_w//2 + j*step_w
            cy = y + step_h//2 + i*step_h
            centers.append((cx, cy))
    return centers

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = create_color_mask(hsv)

        # clean mask
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        largest = get_largest_contour(mask)
        if largest is not None:
            x, y, w, h = cv2.boundingRect(largest)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

            centers = get_3x3_grid((x, y, w, h))
            for cx, cy in centers:
                cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)

        cv2.imshow("Cube Detection", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
