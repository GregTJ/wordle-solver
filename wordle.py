from clipboard import paste
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from corpora import SOLUTIONS, OTHER
from solve import Constraint, guess, constrain

driver = webdriver.Chrome(service=Service('chromedriver.exe'))
driver.get('https://www.powerlanguage.co.uk/wordle/')
driver.implicitly_wait(3)


def shadow_root(element):
    return driver.execute_script('return arguments[0].shadowRoot', element)


_ = driver.find_element(By.CSS_SELECTOR, 'body > game-app')
game = shadow_root(_).find_element(By.CSS_SELECTOR, '#game')

modal = game.find_element(By.CSS_SELECTOR, 'game-modal')
close_modal = shadow_root(modal).find_element(By.CSS_SELECTOR, 'div > div > div')
close_modal.click()

_ = game.find_element(By.CSS_SELECTOR, 'game-keyboard')
keys = shadow_root(_).find_elements(By.CSS_SELECTOR, '#keyboard > div > button')
keys = {k.get_attribute('data-key'): k for k in keys}


def enter_word(word):
    for c in word:
        keys[c].click()
    keys['↵'].click()


def read_row(n):
    _ = game.find_element(By.CSS_SELECTOR, f'#board > game-row:nth-child({n + 1})')
    tiles = shadow_root(_).find_elements(By.CSS_SELECTOR, f'div > game-tile')
    tiles = [Constraint[t.get_attribute('evaluation') or 'absent'] for t in tiles]
    return tiles


row = 0
for i in range(6):
    current = guess(SOLUTIONS, OTHER)
    enter_word(current)
    if stats := modal.find_elements(By.CSS_SELECTOR, '#game > game-modal > game-stats'):
        shadow_root(stats[0]).find_element(By.CSS_SELECTOR, '#share-button').click()
        print(current, paste(), sep='\n\n')
        close_modal.click()
        driver.close()
        break

    constraints = read_row(row)
    SOLUTIONS, OTHER = constrain(SOLUTIONS, OTHER, current, constraints)
    row += 1
