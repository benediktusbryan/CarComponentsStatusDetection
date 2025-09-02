# Car Components Status Detection

A simple AI application to detect and display 3D model car status in real-time.

---

## Setup

1. **Clone this repository**
   ```bash
   https://github.com/benediktusbryan/CarComponentsStatusDetection.git
   cd CarComponentsStatusDetection
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run the backend**
   ```bash
   uvicorn main:app --reload
   ```

4. **Run the python agent**
   ```bash
   python predict.py
   ```

5. **Run the frontend**
   ```bash
   npm run dev
   ```

6. Open in browser:  
   ```
   http://localhost:5173
   ```

---

## Usage

1. **Open the browser from Command Prompt**
   ```bash
   "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/ChromeDebug"
   ```

2. **Open the 3D Model Car**
   [3D Model Car Simulation](https://euphonious-concha-ab5c5d.netlify.app/)
   
3. **Monitor the Dashboard**
- Each status will be displayed with a badge:
  - ✅ **Green** = Open
  - ❌ **Red** = Closed

---

## Troubleshooting

### 1. Node.js Version Error
```
You are using Node.js 18.x
Vite requires Node.js version 20.19+ or 22.12+
```
 **Solution**: Upgrade Node.js  
- Download from [Node.js Official Site](https://nodejs.org/)  
- Or use [nvm](https://github.com/nvm-sh/nvm) to manage versions:
  ```bash
  nvm install 22
  nvm use 22
  ```

### 2. `npm error could not determine executable to run`
- Delete `node_modules` and reinstall:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```
- Ensure `npm` is installed correctly:
  ```bash
  npm -v
  node -v
  ```

### 3. API Not Found / CORS Issues
- Make sure your backend (`http://127.0.0.1:8000/status`) is running.
- If CORS error appears, enable CORS in backend (e.g., using `fastapi.middleware.cors` in FastAPI).

---
