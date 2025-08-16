# Bug Hunter's Recon Automation Platform

A comprehensive, local-first web platform for managing bug bounty reconnaissance and security research.



## 🎯 Features

- **Local Web Dashboard**: Manage campaigns, notes, and results from a secure, local web interface.
- **Dynamic Tool Integration**: Utilizes over 25 industry-standard tools for comprehensive reconnaissance.
- **Scope-Based Scanning**: Automatically adjusts scanning intensity based on the target's size (Small, Medium, Large).
- **Centralized Management**: Keep track of bug reports, bounty targets, checklists, notes, and useful links all in one place.
- **Modular Reconnaissance**: The powerful `recon_script.sh` organizes findings into a clean, structured directory layout.

## 🛠️ Installation

### Prerequisites
- A Debian-based Linux distribution (Kali Linux recommended)
- Python 3.8+ and `pip`
- Go (Go 1.21+)

### Quick Install
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-org/bug-hunter-recon-platform.git](https://github.com/your-org/bug-hunter-recon-platform.git)
    cd bug-hunter-recon-platform
    ```

2.  **Run the installer:**
    This will update your system, install all required system packages, and download the necessary Go and Python tools.
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage

### 1. Start the Web Dashboard
To launch the platform, run the main application file:
```bash
python dashboard_app_enhanced.py
````

Then, open your web browser and navigate to **http://127.0.0.1:5000**.

### 2\. Run a Recon Scan

The platform includes a powerful command-line script for running reconnaissance.

  - **Basic Scan:**

    ```bash
    ./recon_script.sh -d example.com
    ```

  - **Scan with a Forced Scope (e.g., Large):**

    ```bash
    ./recon_script.sh -d example.com -s large
    ```

Results will be saved in a new directory inside the `results/` folder.

## 📁 Project Structure

  - **`dashboard_app_enhanced.py`**: The main Flask web application.
  - **`recon_script.sh`**: The core reconnaissance engine.
  - **`install.sh`**: The automated installation script.
  - **`templates/`**: Contains all the HTML pages for the web dashboard.
  - **`static/`**: Contains CSS and JavaScript files.
  - **`bug_hunter_enhanced.db`**: The application's SQLite database.
  - **`docs/`**: Contains detailed documentation on installation and usage.

## 🤝 Contributing

Contributions are welcome\! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.
