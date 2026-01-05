import numpy as np
import cv2

PROTANOPIA = np.array([
    [0.0, 1.05118294, -0.05116099],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
])

DEUTERANOPIA = np.array([
    [1.0, 0.0, 0.0],
    [0.9513092, 0.0, 0.0486992],
    [0.0, 0.0, 1.0]
])

TRITANOPIA = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [-0.86744736, 1.86727089, 0.0]
])

#3x3 color matrix
def apply_matrix(img, matrix):
    matrix = matrix.astype(np.float32)
    corrected = cv2.transform(img.astype(np.float32), matrix)
    return np.clip(corrected, 0, 255).astype(np.uint8)

def simulate(img, deficiency):
    if deficiency == "protanopia":
        return apply_matrix(img, PROTANOPIA)
    elif deficiency == "deuteranopia":
        return apply_matrix(img, DEUTERANOPIA)
    elif deficiency == "tritanopia":
        return apply_matrix(img, TRITANOPIA)
    else:
        raise ValueError("Invalid deficiency type")
    
def daltonize(img, deficiency):
    #simulate color-blindness
    sim = simulate(img, deficiency)

    #find color diff
    error = img.astype(np.int16) - sim.astype(np.int16)

    #create correction layer
    correction = np.zeros_like(error)

    if deficiency == "protanopia":
        #red to green/blue
        correction[..., 1] = error[..., 0]*0.7
        correction[..., 2] = error[..., 0]*0.7
    
    elif deficiency == "deuteranopia":
        #green to red/blue
        correction[..., 0] = error[..., 1]*0.7
        correction[..., 2] = error[..., 1]*0.7

    elif deficiency == "tritanopia":
        #blue to red/green
        correction[..., 0] = error[..., 2]*0.7
        correction[..., 1] = error[..., 2]*0.7

    else:
        raise ValueError("Invalid deficency type.")
    
    #add the corrections
    out = img + correction

    #return final image
    return np.clip(out, 0, 255).astype(np.uint8)