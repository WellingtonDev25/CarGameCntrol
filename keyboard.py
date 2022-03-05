from pynput.keyboard import Key, Controller
import time
kb = Controller()

# Press and release space
kb.press(Key.left)
time.sleep(1)
kb.press(Key.left)
time.sleep(1)
kb.press(Key.left)
time.sleep(1)
kb.press(Key.left)
kb.release()