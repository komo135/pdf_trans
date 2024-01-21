from selenium import webdriver
from selenium.webdriver.common.by import By
import pyperclip
import re
import pyautogui
import sys
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from pynput import keyboard
import time


class DeepLTranslator:
    def __init__(self, language="ja"):
        self.driver = None
        self.language = language
        self.base_url = f"https://www.deepl.com/{language}/translator"

    def initialize_browser(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.base_url)
        accept_button = self.driver.find_element(By.XPATH, "//*[@id='dl_cookieBanner']/div/div/div/span/button")
        accept_button.click()

    def translate_text(self):
        try:
            time.sleep(0.2)
            copied_text = pyperclip.paste()
            cleaned_text = self.clean_text(copied_text)
            pyperclip.copy(cleaned_text)

            text_area = self.driver.find_element(By.XPATH,
                                                 '//*[@id="panelTranslateText"]/div[1]/div[2]/section[1]/div[3]/div[2]/d-textarea/div')
            text_area.clear()
            text_area.send_keys(Keys.COMMAND, 'v')

            try:
                self.driver.find_element(By.XPATH, '//*[@id="translation-results-heading"]').click()
            except Exception as e:
                print(f"Error in clicking translation results: {e}")
        except Exception as e:
            print(f"Error in translate_text: {e}")

    @staticmethod
    def clean_text(text):
        # 改行を基準にテキストを行に分割
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # コードブロック（インデントまたは特定のパターンで始まる行）をそのまま保持
            if line.startswith('    ') or line.startswith('\t'):
                cleaned_lines.append(line)
            else:
                # 特殊文字を適切に処理
                line = line.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
                # 余分な空白を削除し、行を整形
                line = ' '.join(line.split())
                cleaned_lines.append(line)
        return '\n'.join(cleaned_lines)

    def quit_browser(self):
        self.driver.quit()


if __name__ == "__main__":
    lang = sys.argv[1] if len(sys.argv) == 2 else "ja"
    translator = DeepLTranslator(language=lang)
    translator.initialize_browser()

    with keyboard.GlobalHotKeys({
        "<cmd>+<shift>+h": translator.initialize_browser,
        "<ctrl>": translator.translate_text,
        "<ctrl>+o": translator.quit_browser
    }) as hotkey_listener:
        hotkey_listener.join()
