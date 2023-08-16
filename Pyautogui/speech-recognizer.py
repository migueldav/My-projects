from time import sleep
import speech_recognition as sr
import pyautogui as pya
import numpy as np
import cv2
from pyperclip import copy

r = sr.Recognizer()
r.energy_threshold = 3000
pya.PAUSE = 0.5

def helper(text):
    return ' '.join(text.split()[1:]).lower()

def listen_microphone(paused=False):
    def recognize_audio(source):
        audio = r.listen(source)
        try:
            return r.recognize_google(audio, language='en').lower()
        except sr.UnknownValueError:
            print("Could not recognize audio.")
            sleep(0.6)
        except sr.RequestError as e:
            print("Error requesting results: {0}".format(e))
    
    def process_image(*template_paths):
        screenshot = pya.screenshot()
        screenshot_image = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)
        best_match = None
        best_similarity = 0
        best_y = float(1100)
        best_x = float(1100)

        templates = []
        for path in template_paths:
            template = cv2.imread(path, 0)
            if template is not None:
                templates.append(template)

        for template in templates:
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            locations = np.where(result >= threshold)
            locations = list(zip(*locations[::-1]))
            similarities = [result[loc[::-1]] for loc in locations]
            if similarities:
                for loc, similarity in zip(locations, similarities):
                    click_x, click_y = loc
                    if similarity > best_similarity:
                        if click_y < best_y or (click_y == best_y and click_x < best_x):
                            best_similarity = similarity
                            best_match = (click_x, click_y)
                            best_y = click_y
                            best_x = click_x

        return best_match

    def resize_template(template_path, width, height):
        template = cv2.imread(template_path)
        resized_template = cv2.resize(template, (width, height))
        resized_path = f'{template_path}_resized.png'
        cv2.imwrite(resized_path, resized_template)
        return resized_path

    def open_app(application):
        pya.press('win')
        pya.write(application)
        pya.press('enter')
        sleep(1.4)
        return application
    
    def search(term, app=''):
        list_if = ['youtube', 'whatsapp', 'disney', 'star']
        if app in list_if:
            search_youtube_resized = resize_template('img/searchytb.png', 50, 50)
            search_whatsapp_resized = resize_template('img/searchwhats.png', 50, 50)
            search_disney_resized = resize_template('img/searchds.png', 50, 50)
            results = process_image(search_whatsapp_resized, search_disney_resized, search_youtube_resized)
            if results is not None:
                click_x, click_y = results
                if click_x is not None and click_y is not None:
                    pya.click(click_x + 20, click_y + 20)
                    copy(term)
                    pya.hotkey('ctrl', 'v')
                    pya.press('enter')
        else:
            results = process_image('img/searchnet.png', 
                                    'img/searchcrunchyroll.png')
            if results is not None:
                click_x, click_y = results
                if click_x is not None and click_y is not None:
                    pya.click(click_x + 20, click_y + 20)
                    copy(term)
                    pya.hotkey('ctrl', 'v')
                    pya.press('enter')

    def open_website(site):
        if site == 'whatsapp':
            pya.write('web.whatsapp')
            pya.press('enter')
            sleep(1.5)
        else:
            pya.write(site)
            pya.press('enter')
            sleep(1.4)

    def open_browser():
        pya.click(x=558, y=741)
        pya.hotkey('ctrl', 'shift', 'w')

    def wait_for_play():
        nonlocal paused
        while paused:
            with sr.Microphone() as source:
                print("Waiting for 'play' command...")
                text = recognize_audio(source)
                if text == 'play':
                    paused = False
                    print("Resuming execution!")
                    break

    while True:
        if not paused:
            with sr.Microphone() as source:
                print("Say something...")
                text = recognize_audio(source)
                print(f"You said: {text}")
                sleep(0.6)
        else:
            wait_for_play()
            continue

        if text == 'open browser':
            open_browser()

        elif isinstance(text, str) and text.startswith('open'):
            app = helper(text)
            open_app(app)
            sleep(1.4)
            browsers = ['google', 'edge', 'opera', 'brave']
            if app in browsers:
                with sr.Microphone() as source2:
                    text2 = recognize_audio(source2)
                    print(f'fl: {text2}')
                    if isinstance(text2, str) and text2.startswith('open'):
                        site = helper(text2)
                        open_website(site)
                        sleep(0.7)
                        with sr.Microphone() as source3:
                            text3 = recognize_audio(source3)
                            print(f'vl: {text3}')
                            if isinstance(text3, str) and text3.startswith('search'):
                                term = helper(text3)
                                search(term, site)

            elif app == 'spotify':
                sleep(0.7)
                with sr.Microphone() as source2:
                    text2 = recognize_audio(source2)
                    print(f'fl: {text2}')
                    if isinstance(text2, str) and text2.startswith('search'):
                        term = helper(text2)
                        search(term, app)

        elif isinstance(text, str) and text.startswith('pause'):
            paused = True
            print("Execution paused. Waiting for 'play' command...")

        elif isinstance(text, str) and text.startswith('stop'):
            print('Program terminated')
            break

listen_microphone()
