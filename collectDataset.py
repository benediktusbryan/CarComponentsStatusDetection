from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time, os, random

# URL web 3D mobil
URL = "https://euphonious-concha-ab5c5d.netlify.app/"

# Lokasi folder dataset
DATASET_DIR = "dataset"

# Jumlah dataset
DATASET_NUM = 200

# Mapping tombol komponen di web -> nama label
COMPONENTS = {
    # "Front Left Door": "front_left",
    # "Front Right Door": "front_right",
    # "Rear Left Door": "rear_left",
    # "Rear Right Door": "rear_right",
    "Hood": "hood"
}

# Setup webdriver (pastikan ChromeDriver sesuai versi Chrome)
driver = webdriver.Chrome()
driver.get(URL)
time.sleep(10)  # tunggu canvas 3D load

actions = ActionChains(driver)

# def random_rotate_car(canvas):
def random_rotate_car(canvas, steps=3):
    """
    Putar mobil ke arah acak beberapa kali
    steps = jumlah rotasi acak
    """
    for _ in range(steps):
        dx = random.randint(-150, 150)   # drag horizontal random
        # dy = random.randint(-5, 5)   # drag vertikal random
        actions.click_and_hold(canvas).move_by_offset(dx, 0).release().perform()
        time.sleep(0.8)

def capture(component, state, idx):
    """Simpan screenshot dengan nama file sesuai komponen & state"""
    folder = os.path.join(DATASET_DIR, f"{component}_{state}")
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{component}_{state}_{idx}.png")
    driver.save_screenshot(filename)
    print(f"Saved {filename}")

def toggle_component(button_text):
    """Klik tombol untuk ubah state komponen"""
    btn = driver.find_element(By.XPATH, f"//button[contains(text(),'{button_text}')]")
    btn.click()
    time.sleep(1)

# for i in range(DATASET_NUM):
#     canvas = driver.find_element(By.TAG_NAME, "canvas")
#     random_rotate_car(canvas, steps=3)
#     # capture(comp_label, "close", i)
#     capture("all", "close", i)

# Loop semua komponen
for comp_name, comp_label in COMPONENTS.items():
    # for state in ["closed", "open"]:
        # Pastikan ke state benar
    toggle_component(comp_name)  

    # Ambil 10 variasi view acak
    for i in range(0,95):
        canvas = driver.find_element(By.TAG_NAME, "canvas")
        random_rotate_car(canvas, steps=1)
        capture(comp_label, "open", i)
    toggle_component(comp_name)

driver.quit()