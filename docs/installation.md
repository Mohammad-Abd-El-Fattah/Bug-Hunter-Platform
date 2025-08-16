# Installation Guide

This guide provides detailed instructions for installing the Bug Hunter's Recon Platform on Kali Linux and other Debian-based systems.

## System Requirements

### Minimum Requirements
- **OS**: Kali Linux 2023.1+ or Ubuntu 20.04+
- **RAM**: 8GB (16GB recommended for large-scale reconnaissance)
- **Storage**: 50GB available space
- **Network**: Stable internet connection
- **Privileges**: Sudo access for tool installation

### Recommended Requirements
- **OS**: Kali Linux (latest rolling release)
- **RAM**: 16GB or more
- **Storage**: 100GB+ SSD storage
- **CPU**: Multi-core processor (4+ cores)
- **Network**: High-speed connection for rapid enumeration

## Pre-Installation Steps

### 1. Update System Packages
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Essential Dependencies
```bash
# Development tools
sudo apt install -y build-essential python3-dev python3-pip python3-venv git curl wget

# Security tools base
sudo apt install -y nmap dig curl jq awscli dnsrecon theharvester whatweb gospider ffuf

# Library dependencies for Python packages
sudo apt install -y libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libsqlite3-dev
```

### 3. Install Go Programming Language
```bash
# Download and install Go 1.21+
GO_VERSION="1.21.5"
wget https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz
rm go${GO_VERSION}.linux-amd64.tar.gz

# Add Go to PATH
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc

# Verify installation
go version
```

## Automated Installation

### Option 1: Quick Install Script
```bash
# Clone the repository
git clone https://github.com/your-org/bug-hunter-recon-platform.git
cd bug-hunter-recon-platform

# Run automated installer
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation
Follow the manual steps below if you prefer to install components individually.

## Manual Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-org/bug-hunter-recon-platform.git
cd bug-hunter-recon-platform
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Install Go-Based Tools

#### ProjectDiscovery Tools
```bash
# Core reconnaissance tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/asnmap/cmd/asnmap@latest

# Update nuclei templates
nuclei -update-templates
```

#### Additional Go Tools
```bash
# Enumeration tools
go install github.com/tomnomnom/assetfinder@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/tomnomnom/httprobe@latest
go install github.com/haccer/subjack@latest
go install github.com/tomnomnom/gf@latest

# OWASP Amass
go install -v github.com/owasp-amass/amass/v4/...@master
```

### 4. Install Python-Based Tools

#### Using pip
```bash
# Virtual environment tools
pip install s3scanner waymore py-altdns

# Alternative: Use pipx for global installation
sudo apt install pipx
pipx ensurepath
pipx install s3scanner
pipx install waymore
```

#### Manual Installation
```bash
# LinkFinder
git clone https://github.com/GerbenJavado/LinkFinder.git
cd LinkFinder
pip install -r requirements.txt
sudo ln -sf $(pwd)/linkfinder.py /usr/local/bin/linkfinder
cd ..

# SecretFinder
git clone https://github.com/m4ll0k/SecretFinder.git
cd SecretFinder
pip install -r requirements.txt
sudo ln -sf $(pwd)/SecretFinder.py /usr/local/bin/secretfinder
cd ..

# GitHub Subdomains
git clone https://github.com/gwen001/github-subdomains.git
cd github-subdomains
pip install -r requirements.txt
sudo ln -sf $(pwd)/github-subdomains.py /usr/local/bin/github-subdomains
cd ..
```

### 5. Install System Tools

#### MassDNS
```bash
git clone https://github.com/blechschmidt/massdns.git
cd massdns
make
sudo cp bin/massdns /usr/local/bin/
cd ..
rm -rf massdns
```

#### AltDNS
```bash
pip install py-altdns
# or
git clone https://github.com/infosec-au/altdns.git
cd altdns
pip install -r requirements.txt
sudo python setup.py install
cd ..
```

### 6. Configure API Keys (Optional)

Create configuration directory:
```bash
mkdir -p ~/.config/bug-hunter
```

Create API configuration file:
```bash
cat > ~/.config/bug-hunter/api-keys.conf << EOF
# Bug Hunter Platform API Configuration
# Add your API keys below for enhanced functionality

# Shodan
SHODAN_API_KEY=your_shodan_api_key_here

# VirusTotal
VIRUSTOTAL_API_KEY=your_virustotal_api_key_here

# Censys
CENSYS_API_ID=your_censys_api_id_here
CENSYS_API_SECRET=your_censys_api_secret_here

# GitHub (for github-subdomains)
GITHUB_TOKEN=your_github_token_here

# SecurityTrails
SECURITYTRAILS_API_KEY=your_securitytrails_api_key_here
EOF
```

### 7. Set Up DNS Resolvers
```bash
# Download public DNS resolvers
curl -s https://public-dns.info/nameservers.txt | head -100 > ~/.config/bug-hunter/resolvers.txt

# Add popular resolvers
cat >> ~/.config/bug-hunter/resolvers.txt << EOF
8.8.8.8
8.8.4.4
1.1.1.1
1.0.0.1
9.9.9.9
149.112.112.112
208.67.222.222
208.67.220.220
EOF

# Remove duplicates
sort -u ~/.config/bug-hunter/resolvers.txt -o ~/.config/bug-hunter/resolvers.txt
```

### 8. Install Wordlists
```bash
# Create wordlists directory
mkdir -p ~/wordlists

# Download SecLists
git clone https://github.com/danielmiessler/SecLists.git ~/wordlists/SecLists

# Download additional subdomain wordlists
wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt -O ~/wordlists/subdomains-top1million.txt
```

## Post-Installation Setup

### 1. Create Project Directory Structure
```bash
mkdir -p ~/bug-hunter-platform/{results,wordlists,scripts,logs}
```

### 2. Set Permissions
```bash
# Make scripts executable
chmod +x recon_script.sh
chmod +x install.sh

# Set proper permissions for tools
sudo chmod +x /usr/local/bin/massdns
```

### 3. Initialize Database
```bash
# Activate virtual environment
source .venv/bin/activate

# Initialize SQLite database
python -c "from dashboard_app import init_db; init_db()"
```

### 4. Test Installation
```bash
# Test key tools
subfinder -version
httpx -version
nuclei -version
naabu -version

# Test Python dashboard
python dashboard_app.py &
sleep 2
curl -s http://localhost:5000 > /dev/null && echo "✅ Dashboard working" || echo "❌ Dashboard failed"
pkill -f dashboard_app.py
```

## Configuration

### 1. Bash Script Configuration
Edit the reconnaissance script variables:
```bash
nano recon_script.sh

# Modify these variables as needed:
# DEFAULT_RESOLVERS_FILE
# DEFAULT_WORDLIST_PATH
# DEFAULT_OUTPUT_DIR
```

### 2. Dashboard Configuration
Edit dashboard settings:
```bash
nano dashboard_app.py

# Modify these settings:
# DATABASE_PATH
# RESULTS_DIR
# Debug mode (set to False for production)
```

### 3. Tool-Specific Configuration

#### Subfinder
```bash
# Configure subfinder providers
nano ~/.config/subfinder/provider-config.yaml
```

#### Amass
```bash
# Configure amass data sources
nano ~/.config/amass/config.ini
```

## Troubleshooting

### Common Issues

#### 1. Go Tools Not Found
```bash
# Ensure Go bin directory is in PATH
echo $PATH | grep go/bin
export PATH=$PATH:$HOME/go/bin
```

#### 2. Python Package Installation Errors
```bash
# Use virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Permission Denied Errors
```bash
# Fix permissions
sudo chown -R $USER:$USER ~/.config/
chmod +x recon_script.sh
```

#### 4. Database Connection Issues
```bash
# Reinstall Python dependencies
pip install --force-reinstall sqlite3
```

### Getting Help

If you encounter issues during installation:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review tool-specific documentation
3. Create an issue on the project repository
4. Join the community Discord server

## Verification

### Complete Installation Check
```bash
# Run verification script
bash verify_installation.sh
```

### Manual Verification
```bash
# Check all required tools
for tool in subfinder assetfinder amass httpx naabu nuclei waybackurls gau katana gospider; do
    if command -v $tool >/dev/null 2>&1; then
        echo "✅ $tool: installed"
    else
        echo "❌ $tool: missing"
    fi
done
```

## Next Steps

After successful installation:

1. Review the [Usage Guide](usage.md)
2. Check the [Tools Reference](tools.md)
3. Explore the [API Documentation](api.md)
4. Start your first reconnaissance campaign

## Uninstallation

To completely remove the platform:

```bash
# Remove Go tools
rm -rf $HOME/go/bin/{subfinder,httpx,nuclei,naabu,katana,asnmap,assetfinder,waybackurls,gau,httprobe,subjack,gf,amass}

# Remove Python environment
rm -rf .venv

# Remove configuration
rm -rf ~/.config/bug-hunter

# Remove project files
cd .. && rm -rf bug-hunter-recon-platform
```
