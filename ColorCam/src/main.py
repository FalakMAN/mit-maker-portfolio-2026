import cv2
from color_corrector import simulate, daltonize

img = cv2.imread("/Users/naz/Documents/ColorCam/images/pexels-pixabay-358312.jpg")

if img is None:
    print("Image not found!")
    exit()

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
prot_rgb = simulate(img_rgb, "protanopia")
deut_rgb = simulate(img_rgb, "deuteranopia")
trit_rgb = simulate(img_rgb, "tritanopia")

prot = cv2.cvtColor(prot_rgb, cv2.COLOR_RGB2BGR)
deut = cv2.cvtColor(deut_rgb, cv2.COLOR_RGB2BGR)
trit = cv2.cvtColor(trit_rgb, cv2.COLOR_RGB2BGR)

prot_fix = daltonize(img, "protanopia")
deut_fix = daltonize(img, "deuteranopia")
trit_fix = daltonize(img, "tritanopia")

cv2.imshow("Original", img)
cv2.imshow("Protanopia Correction", prot)
cv2.imshow("Deuteranopia Correction", deut)
cv2.imshow("Tritanopia Correction", trit)

cv2.waitKey(0)
cv2.destroyAllWindows()