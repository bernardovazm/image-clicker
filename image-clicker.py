import pyautogui, os, keyboard
images_path = "images"
key_quit = "esc"

def create_folder(name):
    try:
        os.mkdir(os.getcwd() + "/" + name)
    except:
        return False
create_folder(images_path)

def find_image(image, grayscale=True):
    try:
        location = pyautogui.locateOnScreen(image, grayscale=grayscale)
        return location
    except pyautogui.ImageNotFoundException:
        return False

def click_image(path, duration=0.1, tween=pyautogui.easeInSine):
    try:
        pyautogui.moveTo(path, duration=duration, tween=tween)
        pyautogui.click()
    except:
        return False

def main():
    print(f"Searching for images to click, keep {key_quit} pressed to exit.")
    is_on = not keyboard.is_pressed(key_quit)
    while is_on:
        images_dir = os.listdir(f'{os.getcwd()}/{images_path}')
        images_list = [str(f'{os.getcwd()}/{images_path}/{image}').replace("\\","/").replace(" ", " ") for image in images_dir]
        for image in images_list:
            if find_image(image) is not False:
                click_image(image)
                print(f'{image} clicked')
        is_on = not keyboard.is_pressed(key_quit)
main()