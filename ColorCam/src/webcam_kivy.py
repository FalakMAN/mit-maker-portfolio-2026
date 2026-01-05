import os
import time
import cv2
import numpy as np
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder
from color_corrector import simulate, daltonize

MODES = {
    "normal": "normal",
    "prot_sim": "protanopia_sim",
    "deut_sim": "deuteranopia_sim",
    "trit_sim": "tritanopia_sim",
    "prot_fix": "protanopia_fix",
    "deut_fix": "deuteranopia_fix",
    "trit_fix": "tritanopia_fix"
}

class WebcamRoot(BoxLayout):
    mode = StringProperty("normal")
    status_text = StringProperty("Ready")
    blend = NumericProperty(0.5)
    fps = NumericProperty(0.0)

    def __init__(self, capture_index = 0, fps_target = 30, **kwargs):
        super().__init__(**kwargs)
        self.capture_index = capture_index
        self.cap = cv2.VideoCapture(self.capture_index)
        if not self.cap.isOpened():
            self.status_text = f"Cannot open webcame #{self.capture_index}"
            return
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.current_mode = MODES["normal"]
        self._last_time = time.time()
        Clock.schedule_interval(self.update, 1.0/fps_target)


    def on_stop(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()

    def update(self, dt):
        #read the frame
        ret, frame_bgr = self.cap.read()
        if not ret:
            self.status_text = "Failed to read the frame"
            return
        
        #bgr to rgb
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_rgb = cv2.flip(frame_rgb, 1)

        #apply the mode
        if self.current_mode == MODES["prot_sim"]:
            processed_rgb = simulate(frame_rgb, "protanopia")
        elif self.current_mode == MODES["deut_sim"]:
            processed_rgb = simulate(frame_rgb, "deuteranopia")
        elif self.current_mode == MODES["trit_sim"]:
            processed_rgb = simulate(frame_rgb, "tritanopia")
        elif self.current_mode == MODES["prot_fix"]:
            processed_rgb = daltonize(frame_rgb, "protanopia")
            alpha = float(self.blend)     #slider b/w og and correction
            processed_rgb = cv2.convertScaleAbs((1 - alpha)*frame_rgb + alpha*processed_rgb)
        elif self.current_mode == MODES["deut_fix"]:
            processed_rgb = daltonize(frame_rgb, "deuteranopia")
            alpha = float(self.blend)     #slider b/w og and correction
            processed_rgb = cv2.convertScaleAbs((1 - alpha)*frame_rgb + alpha*processed_rgb)
        elif self.current_mode == MODES["trit_fix"]:
            processed_rgb = daltonize(frame_rgb, "tritanopia")
            alpha = float(self.blend)     #slider b/w og and correction
            processed_rgb = cv2.convertScaleAbs((1 - alpha)*frame_rgb + alpha*processed_rgb)
        else:
            processed_rgb = frame_rgb

            
        #preparing kivy texture
        h, w = processed_rgb.shape[:2]

        #flipping vertically for kivy
        display = processed_rgb
        buf = display.tobytes()

        tex = Texture.create(size = (w, h), colorfmt = 'rgb')
        tex.blit_buffer(buf, colorfmt = 'rgb', bufferfmt = 'ubyte')
        tex.flip_vertical() #orientation just in case

        #set texture
        self.ids.video_view.texture = tex

        #update fps
        now = time.time()
        self.fps = 1.0/(now - self._last_time) if now != self._last_time else 0.0
        self._last_time = now
        self.status_text = f"Mode: {self.current_mode} | FPS: {self.fps: .1f}"

        
    #ui callback
    def set_mode_normal(self):
        self.current_mode = MODES["normal"]
    def set_mode_prot_sim(self):
        self.current_mode = MODES["prot_sim"]
    def set_mode_deut_sim(self):
        self.current_mode = MODES["deut_sim"]
    def set_mode_trit_sim(self):
        self.current_mode = MODES["trit_sim"]
    def set_mode_prot_fix(self):
        self.current_mode = MODES["prot_fix"]
    def set_mode_deut_fix(self):
            self.current_mode = MODES["deut_fix"]
    def set_mode_trit_fix(self):
        self.current_mode = MODES["trit_fix"]

    def set_blend(self, value):
        self.blend = value

    def snapshot(self):
        #takes a picture
        tex = self.ids.video_view.texture
        if tex is None:
            self.status_text = "No frame to save"
            return
            
        pixels = tex.pixels
        w, h = tex.size
        arr = np.frombuffer(pixels, dtype = np.uint8)
        arr = arr.reshape(h, w, 4)
        arr = arr[:, :, :3]

        #rgb to bgr
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        out_dir = "snapshots"
        os.makedirs(out_dir, exist_ok = True)
        fname = os.path.join(out_dir, f"snapshot_{int(time.time())}.png")
        cv2.imwrite(fname, bgr)
        self.status_text = f"Saved: {fname}"

    def quit_app(self):
        #stop app
        if self.cap and self.cap.isOpened():
            self.cap.release()
        App.get_running_app().stop()
        if hasattr(self, "vcam"):
            self.vcam.close()


class ColorCamApp(App):
    def build(self):
        return WebcamRoot()
    
if __name__ == "__main__":
    ColorCamApp().run()



