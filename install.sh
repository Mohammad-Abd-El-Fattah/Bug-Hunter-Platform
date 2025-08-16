#!/bin/bash

# Bug Hunter's Recon Platform - Installation Script
# Automated installer for Kali Linux and Ubuntu

set -e

echo "🚀 Bug Hunter's Recon Platform Installer"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root"
        exit 1
    fi
}

# Update system packages
update_system() {
    log "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
}

# Install Go programming language
install_go() {
    if command -v go &> /dev/null; then
        log "Go is already installed: $(go version)"
        return
    fi

    log "Installing Go programming language..."

    # Download and install Go
    GO_VERSION="1.21.5"
    wget -q https://golang.org/dl/go${GO_VERSION}.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go
    sudo tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz
    rm go${GO_VERSION}.linux-amd64.tar.gz

    # Add Go to PATH
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
    export PATH=$PATH:/usr/local/go/bin
    export PATH=$PATH:$HOME/go/bin

    log "Go installed successfully"
}

# Install Python3 and pip
install_python() {
    log "Installing Python3 and pip..."
    sudo apt install -y python3 python3-pip python3-venv

    # Install Flask and other Python dependencies
    pip3 install flask sqlite3 requests beautifulsoup4 lxml
}

# Install reconnaissance tools
install_tools() {
    log "Installing reconnaissance tools..."

    # Install tools via apt
    sudo apt install -y \
        nmap \
        dig \
        curl \
        jq \
        awscli \
        dnsrecon \
        theharvester \
        whatweb \
        gospider \
        ffuf

    # Install Go-based tools
    log "Installing Go-based tools..."

    # ProjectDiscovery tools
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
    go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
    go install -v github.com/projectdiscovery/katana/cmd/katana@latest
    go install -v github.com/projectdiscovery/asnmap/cmd/asnmap@latest

    # Other tools
    go install github.com/tomnomnom/assetfinder@latest
    go install github.com/tomnomnom/waybackurls@latest
    go install github.com/lc/gau/v2/cmd/gau@latest
    go install github.com/haccer/subjack@latest
    go install github.com/owasp-amass/amass/v4/...@master
    go install github.com/tomnomnom/gf@latest

    # Install altdns
    pip3 install py-altdns

    # Install massdns
    if [ ! -d "massdns" ]; then
        git clone https://github.com/blechschmidt/massdns.git
        cd massdns
        make
        sudo cp bin/massdns /usr/local/bin/
        cd ..
        rm -rf massdns
    fi

    # Install httprobe
    go install github.com/tomnomnom/httprobe@latest

    # Install s3scanner
    pip3 install s3scanner

    # Install linkfinder
    if [ ! -d "LinkFinder" ]; then
        git clone https://github.com/GerbenJavado/LinkFinder.git
        cd LinkFinder
        pip3 install -r requirements.txt
        sudo ln -sf $(pwd)/linkfinder.py /usr/local/bin/linkfinder
        cd ..
    fi

    # Install secretfinder
    if [ ! -d "SecretFinder" ]; then
        git clone https://github.com/m4ll0k/SecretFinder.git
        cd SecretFinder
        pip3 install -r requirements.txt
        sudo ln -sf $(pwd)/SecretFinder.py /usr/local/bin/secretfinder
        cd ..
    fi

    # Install github-subdomains
    if [ ! -d "github-subdomains" ]; then
        git clone https://github.com/gwen001/github-subdomains.git
        cd github-subdomains
        pip3 install -r requirements.txt
        sudo ln -sf $(pwd)/github-subdomains.py /usr/local/bin/github-subdomains
        cd ..
    fi

    # Install waymore
    pip3 install waymore
}

# Install nuclei templates
install_nuclei_templates() {
    log "Installing Nuclei templates..."
    nuclei -update-templates
}

# Install wordlists
install_wordlists() {
    log "Installing wordlists..."

    # Install SecLists
    if [ ! -d "/usr/share/seclists" ]; then
        sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists
    fi

    # Create custom wordlists directory
    mkdir -p ~/wordlists

    # Download common subdomain wordlists
    if [ ! -f "~/wordlists/subdomains-top1million-110000.txt" ]; then
        wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-110000.txt -O ~/wordlists/subdomains-top1million-110000.txt
    fi
}

# Setup project structure
setup_project() {
    log "Setting up project structure..."

    # Create necessary directories
    mkdir -p ~/bug-hunter-platform/{results,wordlists,scripts,logs}

    # Make scripts executable
    chmod +x recon_script.sh

    # Copy files to project directory
    cp recon_script.sh ~/bug-hunter-platform/scripts/
    cp dashboard_app.py ~/bug-hunter-platform/
    cp -r templates ~/bug-hunter-platform/

    # Create configuration file
    cat > ~/.config/bug-hunter/config.conf << EOF
# Bug Hunter Platform Configuration
RESULTS_DIR=~/bug-hunter-platform/results
WORDLISTS_DIR=~/bug-hunter-platform/wordlists
SCRIPTS_DIR=~/bug-hunter-platform/scripts

# API Keys (optional - add your keys here)
SHODAN_API_KEY=
VIRUSTOTAL_API_KEY=
CENSYS_API_ID=
CENSYS_API_SECRET=
GITHUB_TOKEN=
EOF

    mkdir -p ~/.config/bug-hunter
}

# Configure DNS resolvers
setup_dns_resolvers() {
    log "Setting up DNS resolvers..."

    # Download public DNS resolvers
    curl -s https://public-dns.info/nameservers.txt | head -100 > ~/bug-hunter-platform/resolvers.txt

    # Add popular resolvers
    cat >> ~/bug-hunter-platform/resolvers.txt << EOF
8.8.8.8
8.8.4.4
1.1.1.1
1.0.0.1
9.9.9.9
149.112.112.112
208.67.222.222
208.67.220.220
EOF

    sort -u ~/bug-hunter-platform/resolvers.txt -o ~/bug-hunter-platform/resolvers.txt
}

# Create desktop shortcut
create_shortcuts() {
    log "Creating shortcuts..."

    # Create bash alias
    echo 'alias bug-hunter="cd ~/bug-hunter-platform && python3 dashboard_app.py"' >> ~/.bashrc
    echo 'alias recon="~/bug-hunter-platform/scripts/recon_script.sh"' >> ~/.bashrc

    # Create desktop file
    cat > ~/Desktop/bug-hunter.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Bug Hunter Dashboard
Comment=Local bug bounty reconnaissance dashboard
Exec=gnome-terminal -- bash -c "cd ~/bug-hunter-platform && python3 dashboard_app.py; exec bash"
Icon=applications-internet
Terminal=false
Categories=Security;Network;
EOF

    chmod +x ~/Desktop/bug-hunter.desktop
}

# Verify installation
verify_installation() {
    log "Verifying installation..."

    local missing_tools=()
    local tools=("subfinder" "assetfinder" "amass" "httpx" "naabu" "nuclei" 
                 "waybackurls" "gau" "katana" "gospider" "nmap" "dig" "curl" "jq")

    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done

    if [ ${#missing_tools[@]} -eq 0 ]; then
        log "✅ All tools installed successfully!"
    else
        warning "❌ Missing tools: ${missing_tools[*]}"
        warning "Please install missing tools manually"
    fi

    # Check Python dependencies
    python3 -c "import flask, sqlite3, requests; print('✅ Python dependencies OK')" 2>/dev/null || warning "❌ Python dependencies missing"
}

# Main installation function
main() {
    echo "Starting Bug Hunter Platform installation..."

    check_root
    update_system
    install_go
    install_python
    install_tools
    install_nuclei_templates
    install_wordlists
    setup_project
    setup_dns_resolvers
    create_shortcuts
    verify_installation

    echo ""
    log "🎉 Installation completed!"
    echo ""
    info "To start the platform:"
    echo "  1. Open terminal and run: bug-hunter"
    echo "  2. Or double-click the desktop shortcut"
    echo "  3. Access dashboard at: http://localhost:5000"
    echo ""
    info "To run reconnaissance:"
    echo "  recon example.com"
    echo ""
    warning "Please restart your terminal or run: source ~/.bashrc"
}

# Run main function
main "$@"
