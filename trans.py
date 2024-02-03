from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import re
import pyautogui
import os
import sys
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
# from pynput import keyboard
import keyboard
import time


import logging

logging.basicConfig(level=logging.INFO)


class DeepLTranslator:
    def __init__(self, language="ja"):
        self.driver = None
        self.language = language
        self.base_url = f"https://www.deepl.com/{language}/translator"

    def initialize_browser(self):
        logging.info("Initializing browser")
        # ChromeDriverManager().install()
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        
        wait = WebDriverWait(self.driver, 10)
        accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cookieBanner > div > span > button")))
        accept_button.click()
    
    def translate_text(self):
        logging.info("Translating text")
        # クリップボードを初期化
        pyperclip.copy('')
        
        i = 0
        for i in range(100):
            keyboard.send("ctrl+c")
            time.sleep(0.3)
        
            copied_text = pyperclip.paste()
            if copied_text:
                break
            
            i += 1
            logging.info("try: %s", i)
        
        cleaned_text = self.clean_text(copied_text)
        pyperclip.copy(cleaned_text)
    
        try:
            text_area = self.driver.find_element(By.XPATH,
                                                 '//*[@id="headlessui-tabs-panel-7"]/div/div[1]/section/div/div[2]/div[1]/section/div/div[1]/d-textarea/div[1]')
            text_area.clear()
            text_area.send_keys(Keys.CONTROL, 'v')
            # try:
            #     self.driver.find_element(By.XPATH, '//*[@id="translation-results-heading"]').click()
            # except Exception as e:
            #     print(f"Error in clicking translation results: {e}")
        except Exception as e:
            print(f"Error in translate_text: {e}")
        logging.info("Translated text")
        
    @staticmethod
    def clean_text(text):
        # 改行を基準にテキストを行に分割
        lines = text.split('\r\n')
        cleaned_lines = []
        
        if lines:
            for i in range(len(lines)):
                line = lines[i].encode("utf-8").replace(b"\xe2\x80\x90", b"").decode()
                
                if i == 0:
                    cleaned_lines.append(line + " ")
                else:
                    # logging.info("line: %s", line)
                    
                    is_upper = line[0].isupper() if line else False
                    is_priod = cleaned_lines[-1][-1] == "."
                    
                    if is_upper and is_priod:
                        cleaned_lines.append("\n" + line + " ")
                    else:
                        cleaned_lines[-1] += line + " "
            
            return '\n'.join(cleaned_lines).replace("  ", " ")
        else:
            return text
        
    def quit_browser(self):
        logging.info("Quitting browser")
        self.driver.quit()
        self.driver = None

    def exit_program(self):
        logging.info("Exiting program")
        keyboard.clear_all_hotkeys()
        
        self.quit_browser()
        os._exit(0)

if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) == 2 else "ja"
    translator = DeepLTranslator(language=lang)
    translator.initialize_browser()
    
    keyboard.add_hotkey("ctrl+shift+h", translator.initialize_browser)
    keyboard.add_hotkey("alt", translator.translate_text)
    keyboard.add_hotkey("ctrl+o", translator.quit_browser)
    keyboard.add_hotkey("ctrl+shift+z", translator.exit_program)
    keyboard.wait()
    