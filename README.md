# AgriHelp: An AI Assistance Platform for Farmers 🌾🤖

AgriHelp is an intelligent, full-stack computer vision application designed to assist farmers by identifying plant leaf diseases in real-time. By leveraging deep learning architectures combined with an accessible hardware-software ecosystem, the platform maps agricultural data directly to diagnostic metrics, providing immediate guidance to optimize crop protection.

---

## 🏗️ Project Architecture & Stack
The application is organized into a modular decoupled architecture:
*   **Frontend Interface:** Built using **Streamlit / Flutter** to provide a clean dashboard for image upload and diagnostic reporting.
*   **Backend Server Engine:** Powered by a high-performance **Python API gateway** mapping functional data and user sessions.
*   **Deep Learning Pipeline:** Utilizes a custom-trained **TensorFlow / Keras CNN** (built on a MobileNet template architecture) trained on the extensive PlantVillage dataset across 38 distinct plant disease classes.

---

## 📁 Repository Structure
```text
AGROBOT/
├── agrobot_env/               # Local Python virtual environment (ignored by Git)
├── plantvillage dataset/      # Deep learning training directory
├── main.py                    # Backend application API server entrypoint
├── app.py                     # Streamlit web dashboard application
├── train.py                   # Deep learning model definition, compilation, and training script
├── agrobot_cnn_model.keras    # Saved production neural network weights file
├── .gitignore                 # Active version control structural exclusion rules
└── README.md                  # System configuration and usage guide


🚀 Local Environment Setup Instructions
Follow these systematic steps to deploy, set up, and boot the full-stack system locally on your environment.

1. System Requirements & Prerequisites
Ensure you have the following core execution environments installed on your machine:

Python 3.10 or 3.11 (Recommended)

Git version control CLI

2. Clone the Repository Workspace
Open your preferred terminal configuration, navigate to your target desktop directory, and clone your project down:

PowerShell
git clone [https://github.com/navyaajain-hub/AGRIHELP--an-AI-assistance-to-farmers.git](https://github.com/navyaajain-hub/AGRIHELP--an-AI-assistance-to-farmers.git)
cd AGRIHELP--an-AI-assistance-to-farmers
3. Initialize and Activate the Virtual Environment
To keep dependencies clean and isolated, initialize a Python local virtual environment framework inside the workspace root:

On Windows (PowerShell/CMD):

PowerShell
python -m venv agrobot_env
.\agrobot_env\Scripts\Activate.ps1
On macOS/Linux:

Bash
python3 -m venv agrobot_env
source agrobot_env/bin/activate

4. Install Component Dependencies
With your environment active, install the absolute core packages required to load computational weights, handle image data streaming, and power the interface layer:

PowerShell
pip install tensorflow keras h5py streamlit fastapi uvicorn numpy pillow
⚙️ Running the Application Platforms
The application requires booting the system backend gateway followed by the user-facing UI interface layer. Ensure your virtual environment (agrobot_env) remains active across both terminal windows.

Step A: Initialize the Deep Learning Training (Optional)
If you need to re-compile or train the custom image layers dynamically from your plantvillage dataset directory, run the structural script:

PowerShell
python train.py
Note: This generates the production compiled agrobot_cnn_model.keras matrix files directly in your root layout.

Step B: Spin Up the Backend Server Gateway
Open a distinct terminal pane inside the root directory, activate the environment, and execute Uvicorn to initialize the model weights:

PowerShell
python -m uvicorn main:app --reload
Upon successful boot, the terminal log will explicitly confirm:
🔍 DEBUG: File exists check: True
🔥 Real TensorFlow model loaded successfully into the backend.

Step C: Relaunch the Interactive Frontend Interface
Open a second parallel terminal window in the root directory, activate the environment, and execute the Streamlit dashboard launch rule:

PowerShell
python -m streamlit run app.py
The terminal window will generate a local network link (typically http://localhost:8501). Open this directly in your web browser.

🛠️ Usage & Operations Guide
Dashboard Boot: Once the browser interface mounts, choose between default diagnostics or custom analysis modules.

Upload Plant Specimen: Drag and drop an image of an affected leaf (.jpg, .jpeg, or .png) into the system dropzone.

Real-Time Diagnostics: The backend API will automatically ingest the tensor image arrays, perform scaling preprocessing, push them through the loaded neural layers, and return the predicted disease category alongside model certainty parameters.

⚖️ License
Distributed under the Apache License 2.0 or MIT License. See LICENSE inside the repository structure for deeper open-source compliance information.