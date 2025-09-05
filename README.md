# Car Components Status Detection

An AI application to detect and display 3D model car status in real-time. Using lightweight CNN model to classify the car components status.

---

## Setup

**1. Clone this repository**
   ```bash
   https://github.com/benediktusbryan/CarComponentsStatusDetection.git
   cd CarComponentsStatusDetection
   ```

**2. Download the model file**

   [Download model file](https://drive.google.com/file/d/1OQAYN74HhhgoTGMXecnAx4FzJS-BP7Fx/view?usp=sharing)
   Don't forget to move model file to CarComponentsStatusDetection directory

**3. Install dependencies**
   ```bash
   npm install
   ```

**4. Run the backend**
   ```bash
   uvicorn main:app --reload
   ```

**5. Run the python agent**
   ```bash
   python predict.py
   ```

**6. Run the frontend**
   ```bash
   cd my-app
   npm run dev
   ```

**7. Open in browser**  
   ```
   http://localhost:5173
   ```

**8. Open the browser from Command Prompt**
   ```bash
   "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"
   ```

**9. Open the 3D Model Car**
   [3D Model Car Simulation](https://euphonious-concha-ab5c5d.netlify.app/)

---

## Usage

- **Backend API**:
  - `POST /predict` → Upload an image, get prediction results.
  - `GET /status` → Get the latest status (used by frontend).

- **Frontend**:
  - Displays a list of car components with their status (`Open` / `Closed`).

Example API response:
```json
{
  "status": {
    "Front Right": "Closed",
    "Front Left": "Open",
    "Rear Right": "Closed",
    "Rear Left": "Closed",
    "Hood": "Open"
  }
}
```

## Troubleshooting

### Backend
- **Issue:** `RuntimeError: CUDA error: device not found`  
  **Solution:** Run on CPU by ensuring `device = "cpu"` in `main.py`.

- **Issue:** `FileNotFoundError: 'car_parts_model.pth' not found`  
  **Solution:** Place the trained model in the backend folder or update the path.

- **Issue:** API returns empty status.  
  **Solution:** Ensure at least one prediction request was sent before calling `/status`.

---

### Frontend
- **Issue:** `You are using Node.js 18.16.1. Vite requires Node.js version 20.19+ or 22.12+.`  
  **Solution:** Upgrade Node.js using [Node.js official site](https://nodejs.org) or `nvm`.

- **Issue:** `npm error could not determine executable to run`  
  **Solution:** Delete `node_modules` and reinstall:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

---

### Selenium Script
- **Issue:** `selenium.common.exceptions.WebDriverException: unknown error: cannot connect to Chrome`  
  **Solution:** Start Chrome with `--remote-debugging-port=9222` and ensure no other Chrome instance is running.

- **Issue:** `selenium.common.exceptions.NoSuchElementException: no such element: Unable to locate element: {"method":"tag name","selector":"canvas"}`  
  **Solution:** Verify the page actually contains a `<canvas>` element.

- **Issue:** API call timeout.  
  **Solution:** Ensure FastAPI backend is running on `http://127.0.0.1:8000`.

---
