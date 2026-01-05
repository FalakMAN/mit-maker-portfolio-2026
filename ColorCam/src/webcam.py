import cv2
from color_corrector import simulate, daltonize
def run_webcam(mode = "normal"):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open webcam.")
        return
    
    print("Press 'Q' to quit.")
    print("""
          Modes:
          1 - Normal
          2 - Protanopia Simulation
          3 - Deuteranopia Simulation
          4 - Tritanopia Simulation
          5 - Protanopia Correction
          6 - Deuteranopia Correction
          7 - Tritanopia Correction
          """)
    
    current_mode = mode

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #bgr to rgb
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #apply mode
        if current_mode == "protanopia_sim":
            rgb = simulate(rgb, "protanopia")
        elif current_mode == "deuteranopia_sim":
            rgb = simulate(rgb, "deuteranopia")
        elif current_mode == "tritanopia_sim":
            rgb = simulate(rgb, "tritanopia")
        elif current_mode == "protanopia_fix":
            rgb = daltonize(rgb, "protanopia")
        elif current_mode == "deuteranopia_fix":
            rgb = daltonize(rgb, "deuteranopia")
        elif current_mode == "tritanopia_fix":
            rgb = daltonize(rgb, "tritanopia")

        #rgb to bgr
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        cv2.imshow("Colorcam - Webcam", bgr)

        key = cv2.waitKey(1) & 0xFF

        #key bindings
        if key == ord('q'):
            break
        elif key == ord('1'):
            current_mode = "normal"
        elif key == ord('2'):
            current_mode = "protanopia_sim"
        elif key == ord('3'):
            current_mode = "deuteranopia_sim"
        elif key == ord('4'):
            current_mode = "tritanopia_sim"
        elif key == ord('5'):
            current_mode = "protanopia_fix"
        elif key == ord('6'):
            current_mode = "deuteranopia_fix"
        elif key == ord('7'):
            current_mode = "tritanopia_fix"


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_webcam()
