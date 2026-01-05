import cv2
import numpy as np

def order_points(pts):
    """
    Orders 4 points in consistent order: top-left, top-right, bottom-right, bottom-left
    """
    pts = pts.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    
    return rect

def get_grid_centers(rect):
    """
    Given ordered corners of the cube face (tl, tr, br, bl),
    return 9 points (x,y) representing the centers of each sticker.
    """
    tl, tr, br, bl = rect
    centers = []
    for i in range(3):
        for j in range(3):
            cx = int(tl[0] + (tr[0]-tl[0])*j/2 + (bl[0]-tl[0])*i/2)
            cy = int(tl[1] + (tr[1]-tl[1])*j/2 + (bl[1]-tl[1])*i/2)
            centers.append((cx, cy))
    return centers

def detect_cube_face(frame):
    """
    Detects the largest quadrilateral roughly square in the frame.
    Returns the 4 ordered corner points or None.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.05 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 0.8 < aspect_ratio < 1.2:
                return order_points(approx), edges
    return None, edges

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cube_face, edges = detect_cube_face(frame)
        if cube_face is not None:
            # draw cube face
            for i in range(4):
                pt1 = tuple(cube_face[i].astype(int))
                pt2 = tuple(cube_face[(i+1)%4].astype(int))
                cv2.line(frame, pt1, pt2, (0,255,0), 2)

            # get 3x3 grid centers
            centers = get_grid_centers(cube_face)
            for cx, cy in centers:
                cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)

        cv2.imshow("Cube Detection", frame)
        cv2.imshow("Edges", edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
