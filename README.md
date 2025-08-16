# Bug Hunter's Recon Automation Platform

A comprehensive reconnaissance automation platform designed specifically for bug bounty hunters and penetration testers. This platform combines an intelligent bash-based reconnaissance engine with a local web dashboard for campaign management and result analysis.

## 🎯 Features

### Intelligent Scope Classification
- **Automatic Target Assessment**: Determines scope size through initial passive reconnaissance
- **Adaptive Module Selection**: Different scanning strategies for small, medium, and large targets
- **Resource Optimization**: Prevents over-scanning small targets and under-scanning large ones

### Comprehensive Tool Integration
- **25+ Industry-Standard Tools**: subfinder, amass, nuclei, nmap, httpx, and many more
- **Modular Architecture**: Independent modules for different reconnaissance phases
- **Scope-Adaptive Execution**: Different techniques based on target size

### Local Web Dashboard
- **No Authentication Required**: Runs locally on localhost for security
- **Real-time Monitoring**: Live view of reconnaissance progress
- **Campaign Management**: Track multiple targets and sessions
- **Integrated Script Editor**: Write and save custom bash scripts

## 📋 Scope Classification

The platform automatically classifies targets into three categories:

- **SMALL**: <50 subdomains & <10 live hosts
  - Focus: Deep manual testing, quick wins identification
  - Techniques: 16 focused reconnaissance methods

- **MEDIUM**: 50-300 subdomains & <100 live hosts  
  - Focus: Balanced automation and manual testing
  - Techniques: 22 comprehensive methods

- **LARGE**: >300 subdomains or >100 live hosts
  - Focus: Maximum automation deployment
  - Techniques: 25+ extensive reconnaissance vectors

## 🛠️ Installation

### Prerequisites
- Kali Linux (recommended) or Ubuntu 20.04+
- 8GB+ RAM (16GB recommended for large scopes)
- 50GB+ available storage
- Stable internet connection

### Quick Installation
```bash
# Clone the repository
git clone https://github.com/your-org/bug-hunter-recon-platform.git
cd bug-hunter-recon-platform

# Run the automated installer
chmod +x install.sh
./install.sh

# Start the dashboard
python3 dashboard_app.py
```

### Manual Installation
If you prefer to install manually, see the [Installation Guide](docs/installation.md) for detailed instructions.

## 🚀 Usage

### Starting the Platform
```bash
# Start the web dashboard
python3 dashboard_app.py

# Access at http://localhost:5000
```

### Command Line Usage
```bash
# Basic reconnaissance
./recon_script.sh -d example.com

# Force specific scope
./recon_script.sh -d example.com -s large

# Custom output directory
./recon_script.sh -d example.com -o /path/to/results

# Verbose mode
./recon_script.sh -d example.com -v
```

### Web Dashboard
1. **Navigate to Recon section**
2. **Create new campaign** with target domain
3. **Monitor progress** in real-time
4. **View results** and download reports
5. **Edit bash scripts** as needed

## 📊 Dashboard Navigation

- **Dashboard**: Overview and statistics
- **Platforms & Bugs**: Bug bounty platform integration
- **My Bug Reports**: Track discovered vulnerabilities
- **Bounty Targets**: Manage target domains
- **Security Checklist**: Testing methodologies
- **Tips & Tricks**: Best practices and techniques
- **Reading List**: Curated security resources
- **News Feed**: Latest security news
- **Personal Notes**: Custom documentation
- **Useful Links**: Quick access to tools
- **Recon**: Primary reconnaissance interface
- **Attack**: Attack methodologies
- **Exploit**: Exploitation techniques

## 🔧 Configuration

### API Keys (Optional)
Edit `~/.config/bug-hunter/config.conf`:
```bash
SHODAN_API_KEY=your_shodan_key
VIRUSTOTAL_API_KEY=your_vt_key
CENSYS_API_ID=your_censys_id
CENSYS_API_SECRET=your_censys_secret
GITHUB_TOKEN=your_github_token
```

### DNS Resolvers
The platform automatically configures DNS resolvers, but you can customize them in `resolvers.txt`.

## 📁 Output Structure

```
results/target.com/YYYYMMDD_HHMMSS/
├── 01_initial_assessment/
│   └── scope_classification.txt
├── 02_subdomain_enum/
│   ├── passive/
│   ├── active/
│   └── permutation/
├── 03_host_discovery/
│   ├── http/
│   ├── https/
│   └── alive/
├── 04_port_scanning/
│   ├── tcp/
│   ├── udp/
│   └── service_scan/
├── 05_crawling/
│   ├── endpoints/
│   ├── parameters/
│   └── js_files/
├── 06_vulnerability_scan/
│   ├── nuclei/
│   ├── secrets/
│   └── misconfigs/
├── 07_intelligence/
│   ├── osint/
│   ├── wayback/
│   └── github/
├── 08_technology_stack/
├── 09_cloud_assets/
├── 10_advanced_recon/
└── final_report/
    └── reconnaissance_report.md
```

## 🔍 Included Tools

### Subdomain Enumeration
- **subfinder**: Fast passive subdomain enumeration
- **assetfinder**: Additional passive sources
- **amass**: Comprehensive active/passive enumeration
- **altdns**: Permutation-based discovery
- **massdns**: DNS resolution at scale

### Network Analysis
- **nmap**: Port scanning and service detection
- **naabu**: Fast port discovery
- **httprobe**: HTTP/HTTPS probe
- **httpx**: HTTP toolkit with advanced features

### Content Discovery
- **waybackurls**: Historical URL discovery
- **gau**: GetAllUrls from various sources
- **katana**: Modern web crawler
- **gospider**: Fast web spider
- **linkfinder**: JavaScript endpoint extraction

### Vulnerability Assessment
- **nuclei**: Template-based vulnerability scanner
- **s3scanner**: AWS S3 bucket scanner
- **secretfinder**: Secrets in JavaScript files
- **subjack**: Subdomain takeover detection

### Intelligence Gathering
- **theHarvester**: OSINT framework
- **crt.sh**: Certificate transparency
- **dnsrecon**: DNS enumeration
- **asnmap**: ASN discovery
- **whatweb**: Technology identification

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Usage Examples](docs/usage.md)
- [Tool Commands Reference](docs/tools.md)
- [API Documentation](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized testing purposes only. Users are responsible for ensuring they have proper authorization before testing any systems. The developers are not responsible for any misuse or damage caused by this tool.

## 🙏 Acknowledgments

- [ProjectDiscovery](https://projectdiscovery.io/) for excellent reconnaissance tools
- [OWASP](https://owasp.org/) for security testing methodologies
- The bug bounty community for continuous innovation
- All open-source tool developers who made this platform possible

## 📞 Support

- Create an [Issue](https://github.com/your-org/bug-hunter-recon-platform/issues) for bug reports
- Join our [Discord](https://discord.gg/your-invite) for community support
- Follow [@BugHunterPlatform](https://twitter.com/your-handle) for updates

---

**Happy Hunting! 🐛**
