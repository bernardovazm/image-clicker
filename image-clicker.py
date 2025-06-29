import pyautogui, os, keyboard, datetime, json
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

def is_within_schedule(image_name):
    try:
        if 'scheduled_images' not in globals():
            return True
        if image_name not in scheduled_images:
            return True
            
        schedule = scheduled_images[image_name]
        if not schedule.get('active', True):
            return False

        if schedule.get('clicked', False):
            return False
            
        current_time = datetime.datetime.now().time()
        
        for interval in schedule.get('intervals', []):
            start_time = datetime.datetime.strptime(interval['start_time'], '%H:%M').time()
            end_time = datetime.datetime.strptime(interval['end_time'], '%H:%M').time()
            
            if start_time <= end_time:
                if start_time <= current_time <= end_time:
                    return True
            else:
                if current_time >= start_time or current_time <= end_time:
                    return True
        
        return False
    except Exception as e:
        if is_logger_active:
            print(f"Schedule check error for {image_name}: {e}")
        return True

def find_image(image, grayscale=True, confidence=1.0):
    try:
        image_name = strip_image_path(image)
        if not is_within_schedule(image_name):
            if is_logger_active:
                print(f"[{datetime.datetime.now()}] {image_name} fora do horário agendado.")
            return False
            
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

def click_image(point, image_name, duration=duration, tween=pyautogui.easeInSine):
    try:
        current_pos = pyautogui.position()
        pyautogui.moveTo(point, duration=duration, tween=tween)
        pyautogui.click()
        
        if 'scheduled_images' in globals() and image_name in scheduled_images:
            scheduled_images[image_name]['clicked'] = True
            if is_logger_active:
                print(f"[{datetime.datetime.now()}] {image_name} checked as clicked.")
        
        if should_return_position:
            pyautogui.moveTo(current_pos, duration=duration, tween=tween)
            if is_logger_active:
                print(f"[{datetime.datetime.now()}] Mouse position returned.")
    except:
        return False

def reset_clicked_status():
    if 'scheduled_images' in globals():
        for image_name in scheduled_images:
            scheduled_images[image_name]['clicked'] = False
            if is_logger_active:
                print(f"[{datetime.datetime.now()}] Reset clicked status for {image_name}")

def main():
    print(f"[{datetime.datetime.now()}] Script started, searching on your main monitor for images to click. Hold {key_quit} to exit.")
    load_config()
    is_on = not keyboard.is_pressed(key_quit)
    last_reset = datetime.datetime.now()
    
    while is_on:
        current_time = datetime.datetime.now()
        if (current_time - last_reset).total_seconds() >= 60:
            reset_clicked_status()
            last_reset = current_time
        
        images_dir = os.listdir(f'{os.getcwd()}/{images_path}')
        images_list = [
            str(f'{os.getcwd()}/{images_path}/{image}').replace("\\","/")
            for image in images_dir
            if image.endswith(tuple(file_extensions))
            ]
        for image in images_list:
            image_name = strip_image_path(image)
            image_pos = find_image(image, grayscale, confidence)
            if image_pos is not False:
                click_image(image_pos, image_name, duration)
                print(f"[{datetime.datetime.now()}] {image_name} clicked.")
        is_on = not keyboard.is_pressed(key_quit)
main()