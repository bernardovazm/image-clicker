import pyautogui, os, keyboard, datetime, json, cv2
is_logger_active = False
images_path = "images"
key_quit = "esc"
file_extensions = [".png", ".jpg"]
should_return_position = False
grayscale = True
duration = 0.1
confidence = 1.0

def create_folder(name):
    try:
        os.mkdir(os.getcwd() + "/" + name)
    except:
        return False
create_folder(images_path)

def strip_image_path(image, images_path=images_path):
    return str(image.replace(f"{os.getcwd()}/{images_path}/".replace("\\","/"), ""))

def load_config():
    try:
        globals_dict = globals()
        with open("config.json", "r") as f:
            config = json.load(f)
            for var in config:
                globals_dict[var] = config[var]
                if is_logger_active:
                    print(f"G [{datetime.datetime.now()}] Variable {var} updated to: {globals_dict[var]}")
            return(globals())
    except FileNotFoundError:
        print(f"File config.json not found, using default values...")
    except Exception as e:
        print(f"Exception: {e}")

def find_image(image, grayscale=True, confidence=1.0):
    try:
        location = pyautogui.locateOnScreen(image, grayscale=grayscale, confidence=confidence)
        return location
    except pyautogui.ImageNotFoundException:
        if is_logger_active:
            print(f"X [{datetime.datetime.now()}] {strip_image_path(image)} not found.")
        return False
    except Exception as e:
        if is_logger_active:
            print(f"X [{datetime.datetime.now()}] Except: {e}, {strip_image_path(image)}.")
        return False

def click_image(point, duration=duration, tween=pyautogui.easeInSine):
    try:
        current_pos = pyautogui.position()
        pyautogui.moveTo(point, duration=duration, tween=tween)
        pyautogui.click()
        if should_return_position:
            pyautogui.moveTo(current_pos, duration=duration, tween=tween)
            if is_logger_active:
                print(f"[{datetime.datetime.now()}] Mouse position returned.")
    except:
        return False

def main():
    print(f"[{datetime.datetime.now()}] Script started, searching on your main monitor for images to click. Hold {key_quit} to exit.")
    load_config()
    is_on = not keyboard.is_pressed(key_quit)
    while is_on:
        images_dir = os.listdir(f'{os.getcwd()}/{images_path}')
        images_list = [
            str(f'{os.getcwd()}/{images_path}/{image}').replace("\\","/")
            for image in images_dir
            if image.endswith(tuple(file_extensions))
            ]
        for image in images_list:
            image_pos = find_image(image, grayscale, confidence)
            if image_pos is not False:
                click_image(image_pos, duration)
                print(f"[{datetime.datetime.now()}] {strip_image_path(image)} clicked.")
        is_on = not keyboard.is_pressed(key_quit)
main()