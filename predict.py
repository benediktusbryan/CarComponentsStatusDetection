import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

API_URL = "http://127.0.0.1:8000/predict"

# KONEKSI KE CHROME YANG SUDAH TERBUKA
options = webdriver.ChromeOptions()
# Pastikan Chrome dijalankan dengan:
# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"
options.debugger_address = "127.0.0.1:9222"   # remote debugging Chrome yang sudah terbuka
driver = webdriver.Chrome(service=Service(), options=options)

# LOOPING PREDIKSI
try:
    while True:
        try:
            # cari canvas mobil
            canvas = driver.find_element(By.TAG_NAME, "canvas")
            screenshot_path = "canvas.png"
            
            # simpan screenshot canvas ke file
            canvas.screenshot(screenshot_path)

            # kirim screenshot ke API FastAPI
            with open(screenshot_path, "rb") as f:
                files = {"file": ("canvas.png", f, "image/png")}
                response = requests.post(API_URL, files=files, timeout=10)

            if response.ok:
                print("Prediksi:", response.json())
            else:
                print("Error API:", response.status_code, response.text)

        except Exception as e:
            print("Gagal ambil/kirim screenshot:", e)

        # jeda periodik
        time.sleep(0.5)  # ambil setiap 0.5 detik

except KeyboardInterrupt:
    print("Dihentikan oleh user.")

finally:
    driver.quit()