import time
import serial
import cv2
import tkinter as tk
from PIL import Image, ImageTk

# =========================
#   SERIAL PORT SETUP
# =========================
# Change port if needed:
#   Raspberry Pi USB = '/dev/ttyUSB0' or '/dev/ttyACM0'
#   UART pins = '/dev/ttyAMA0'
ser = serial.Serial('/dev/ttyUSB0', 115200 , timeout=1)
time.sleep(2)  # allow serial to stabilise

# =========================
#   TKINTER FULLSCREEN SETUP
# =========================
root = tk.Tk()
root.attributes('-fullscreen', True)
root.bind('<Escape>', lambda e: root.destroy())

# Screen resolution
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# =========================
#   LOAD BACKGROUND IMAGE
# =========================
image = cv2.imread('imageJ.jpg')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

h, w = image.shape[:2]
scale = min(screen_width / w, screen_height / h)
new_w, new_h = int(w * scale), int(h * scale)

resized_image = cv2.resize(image_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)

label = tk.Label(root)
label.pack(fill='both', expand=True)

# =========================
#   TEXT POSITIONS
# =========================
pos1 = (int(new_w * 0.23), int(new_h * 0.415))  # First line
pos2 = (int(new_w * 0.23), int(new_h * 0.63))   # Second line (63%)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2
color = (255, 255, 255)
thickness = 3

# =========================
#   READ WEIGHT FROM SERIAL
# =========================
def read_weight_from_serial():
    """Reads weight in KG directly from COM port."""
    try:
        line = ser.readline().decode("utf-8").strip()
        if line:
            return float(line)     # already in KG
        else:
            return None
    except:
        return None

# =========================
#   UPDATE DISPLAY LOOP
# =========================
def update_display():
    weight_kg = read_weight_from_serial()
    if weight_kg is None:
        weight_kg = 0.0  # fallback value

    frame = resized_image.copy()

    # Draw live weight
    cv2.putText(frame, f"{weight_kg:.2f} Kg", pos1,
                font, font_scale, color, thickness, cv2.LINE_AA)

    # Draw 2.5x weight
    cv2.putText(frame, f"{weight_kg * 2.5:.2f} Kg", pos2,
                font, font_scale, color, thickness, cv2.LINE_AA)

    # Convert to Tkinter image
    img_tk = ImageTk.PhotoImage(Image.fromarray(frame))
    label.config(image=img_tk)
    label.image = img_tk

    root.after(200, update_display)  # refresh every 0.2 sec

# Start loop
update_display()
root.mainloop()

# Close serial port on exit
ser.close()
