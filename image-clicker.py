import pyautogui, os, keyboard, datetime, json
images_path = "images"
key_quit = "esc"
file_extensions = [".png", ".jpg"]
should_return_position = False
grayscale = True
duration = 0.1

def create_folder(name):
    try:
        os.mkdir(os.getcwd() + "/" + name)
    except:
        return False
create_folder(images_path)

def load_config():
    try:
        globals_dict = globals()
        with open("config.json", "r") as f:
            config = json.load(f)
            for var in config:
                globals_dict[var] = config[var]
            return(globals())
    except FileNotFoundError:
        print(f"File config.json not found, using default values...")
    except Exception as e:
        print(f"Exception: {e}")

def find_image(image, grayscale=True):
    try:
        location = pyautogui.locateOnScreen(image, grayscale=grayscale)
        return location
    except pyautogui.ImageNotFoundException:
        return False

def click_image(point, duration=duration, tween=pyautogui.easeInSine):
    try:
        current_pos = pyautogui.position()
        pyautogui.moveTo(point, duration=duration, tween=tween)
        pyautogui.click()
        if should_return_position:
            pyautogui.moveTo(current_pos, duration=duration, tween=tween)
        print(f'{datetime.datetime.now()} - {str(point.replace(f"{os.getcwd()}/{images_path}/".replace("\\","/"), ""))} clicked')
    except:
        return False

def main():
    print(f"{datetime.datetime.now()} - Script started, searching main monitor for images to click. Hold {key_quit} to exit.")
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
            if find_image(image) is not False:
                click_image(image, duration)
        is_on = not keyboard.is_pressed(key_quit)
main()