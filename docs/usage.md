# Usage Guide

This guide provides comprehensive examples and workflows for using the Bug Hunter's Recon Platform effectively.

## Quick Start

### 1. Start the Dashboard
```bash
# Activate virtual environment
source .venv/bin/activate

# Launch the web dashboard
python dashboard_app.py

# Access at http://localhost:5000
```

### 2. Run Your First Reconnaissance
```bash
# Basic reconnaissance
./recon_script.sh example.com

# Custom output directory
./recon_script.sh example.com -o /path/to/results

# Verbose output
./recon_script.sh example.com -v

# Force specific scope size
./recon_script.sh example.com -s large
```

## Dashboard Usage

### Navigation Overview

The dashboard provides several sections for comprehensive bug bounty management:

- **Dashboard**: Overview and statistics
- **Recon**: Script editor and campaign management
- **Bug Reports**: Vulnerability tracking and documentation
- **Targets**: Domain and program management
- **Security Checklist**: Interactive testing methodology
- **Tips & Tricks**: Curated knowledge base
- **Reading List**: Educational resources
- **News Feed**: Latest security updates
- **Personal Notes**: Custom documentation
- **Useful Links**: Quick access to tools and resources
- **Attack**: Attack vector methodologies
- **Exploit**: Exploitation techniques and payloads

### Using the Recon Interface

#### 1. Script Editor
- **Edit Scripts**: Modify the reconnaissance bash script directly in the browser
- **Save Scripts**: Download customized scripts to local filesystem
- **Run Scripts**: Execute reconnaissance with target domain input
- **Validate**: Check script syntax and structure

#### 2. Campaign Management
- **Create Campaigns**: Start new reconnaissance sessions
- **Monitor Progress**: Real-time status updates
- **View Results**: Browse and analyze findings
- **Download Reports**: Export results in various formats

### Managing Targets

#### Adding New Targets
1. Navigate to **Bounty Targets** section
2. Click **Add Target**
3. Fill in target information:
   - Domain (required)
   - Program name
   - Platform (HackerOne, Bugcrowd, etc.)
   - Scope type
   - Status (Active/Inactive)
   - Notes

#### Target Management Features
- **Search**: Filter targets by domain name
- **Start Recon**: Launch reconnaissance directly from target list
- **Edit**: Update target information
- **Delete**: Remove targets from database

### Bug Report Tracking

#### Creating Bug Reports
1. Go to **My Bug Reports** section
2. Click **New Bug Report**
3. Complete the report form:
   - Title and description
   - Severity level
   - Target URL
   - Platform information
   - Bounty amount
   - Proof of concept

#### Report Management
- **Filter by Severity**: View critical, high, medium, or low severity bugs
- **Search**: Find specific reports by title
- **Statistics**: Track total reports, earnings, and success rates
- **Export**: Download reports for external documentation

## Command Line Usage

### Basic Reconnaissance Script

#### Syntax
```bash
./recon_script.sh [OPTIONS] <target_domain>
```

#### Options
- `-h, --help`: Display help information
- `-o, --output DIR`: Specify output directory
- `-s, --scope SIZE`: Force scope size (small|medium|large)
- `-v, --verbose`: Enable verbose output
- `-q, --quiet`: Suppress non-essential output
- `-r, --resolvers FILE`: Custom DNS resolvers file
- `-w, --wordlist FILE`: Custom subdomain wordlist

### Scope-Based Execution

The script automatically classifies targets and executes appropriate modules:

#### Small Scope (<50 subdomains, <10 live hosts)
- Directory enumeration
- Technology fingerprinting
- Port scanning (focused)
- Parameter fuzzing
- Wayback history analysis
- Known vulnerability scanning
- JavaScript data extraction
- GitHub/Google dorking
- Broken link hijacking
- Cloud storage misconfiguration checks
- Data breach analysis
- Email and certificate reconnaissance
- Metadata extraction
- Technology profiling
- API endpoint discovery
- GitHub sensitive data extraction

#### Medium Scope (50-300 subdomains, <100 live hosts)
All small scope techniques plus:
- Extended subdomain enumeration
- Subdomain takeover testing
- Nuclei template scanning
- IP range enumeration
- Shodan/Censys/Spyse enumeration
- GF pattern extraction (XSS, SSRF, etc.)
- Heartbleed scanning
- Security misconfiguration scanning

#### Large Scope (>300 subdomains or >100 live hosts)
All medium scope techniques plus:
- Application component signature tracking
- Subsidiary and acquisition enumeration
- ASN and reverse IP/domain lookup
- Extensive IP/network reconnaissance
- All relevant network and web-based reconnaissance vectors

### Example Workflows

#### 1. Quick Assessment
```bash
# Fast reconnaissance for initial assessment
./recon_script.sh target.com --scope small -q

# Results will be in: results/target.com/YYYYMMDD_HHMMSS/
```

#### 2. Comprehensive Analysis
```bash
# Full reconnaissance with custom settings
./recon_script.sh target.com     --scope large     --output ~/recon/target-com     --resolvers ~/.config/bug-hunter/resolvers.txt     --verbose
```

#### 3. Batch Processing
```bash
# Process multiple targets
for domain in $(cat target-list.txt); do
    echo "Processing $domain..."
    ./recon_script.sh "$domain" -o "results/$domain"
    sleep 60  # Rate limiting
done
```

#### 4. API Integration
```bash
# Set API keys for enhanced results
export SHODAN_API_KEY="your_shodan_key"
export VIRUSTOTAL_API_KEY="your_vt_key"
export GITHUB_TOKEN="your_github_token"

./recon_script.sh target.com --scope medium
```

## Advanced Usage

### Customizing the Reconnaissance Script

#### Adding Custom Modules

1. **Create Module Function**:
```bash
module_custom_scan() {
    log "Starting custom scan module..."

    # Your custom reconnaissance logic here
    custom_tool -target "$TARGET" > "$OUTPUT_DIR/custom_results.txt"

    log "Custom scan completed"
}
```

2. **Integrate into Main Function**:
```bash
main() {
    # ... existing code ...

    # Add custom module based on scope
    case $SCOPE_SIZE in
        "LARGE")
            module_custom_scan
            ;;
    esac
}
```

#### Modifying Tool Parameters

Edit tool-specific configurations in the script:

```bash
# Customize subfinder
subfinder -d "$TARGET" -all -silent -t 50 -timeout 10

# Customize nuclei
nuclei -l "$OUTPUT_DIR/live_hosts.txt" -severity critical,high -stats

# Customize nmap
nmap -sS -sV -T4 -p- --min-rate 1000 "$TARGET"
```

### Dashboard Customization

#### Adding Custom Notes Categories
Modify the note categories in `templates/notes.html`:

```html
<select class="form-select" id="noteCategory">
    <option value="methodology">Methodology</option>
    <option value="payloads">Payloads</option>
    <option value="automation">Automation</option>
    <!-- Add your custom categories -->
</select>
```

#### Custom Security Checklist
Edit the checklist data in `templates/checklist.html`:

```javascript
const checklistData = {
    webApp: [
        {title: "Custom Test", priority: "high", description: "Your custom test"},
        // Add more items
    ]
};
```

### Integration with External Tools

#### Burp Suite Integration
```bash
# Export discovered URLs to Burp
cat "$OUTPUT_DIR/all_urls.txt" | sort -u > burp_targets.txt
```

#### Metasploit Integration
```bash
# Generate Metasploit workspace
echo "workspace -a recon_$(date +%Y%m%d)" > msf_commands.txt
echo "db_import $OUTPUT_DIR/nmap_results.xml" >> msf_commands.txt
```

#### Custom Reporting
```bash
# Generate custom report
python3 << EOF
import json
import os

# Load reconnaissance data
with open('$OUTPUT_DIR/summary.json', 'r') as f:
    data = json.load(f)

# Generate custom report format
# Your reporting logic here
EOF
```

## Best Practices

### 1. Scope Management
- Always verify targets are in scope before testing
- Start with small scope to understand target behavior
- Use appropriate rate limiting for large targets
- Respect robots.txt and security.txt files

### 2. Data Organization
- Use consistent directory structures
- Maintain detailed notes for each campaign
- Document interesting findings immediately
- Regular backup of reconnaissance data

### 3. Operational Security
- Use VPN or proxy for reconnaissance activities
- Rotate source IPs for large-scale enumeration
- Monitor for detection and blocking
- Keep tools and payloads updated

### 4. Time Management
- Set realistic timeframes for different scope sizes
- Prioritize high-impact reconnaissance techniques
- Automate repetitive tasks
- Focus manual effort on unique findings

### 5. Quality Control
- Validate all discovered assets
- Cross-reference findings across multiple tools
- Verify vulnerability findings before reporting
- Maintain proof-of-concept documentation

## Troubleshooting

### Common Issues

#### 1. Script Execution Errors
```bash
# Check script permissions
chmod +x recon_script.sh

# Verify tool installations
which subfinder httpx nuclei

# Check PATH variables
echo $PATH
```

#### 2. High Memory Usage
```bash
# Monitor resource usage
htop

# Limit concurrent processes
export MAX_PARALLEL_JOBS=5

# Use smaller wordlists for large targets
```

#### 3. Network Connectivity Issues
```bash
# Test DNS resolution
nslookup target.com

# Check firewall settings
sudo ufw status

# Verify internet connectivity
ping -c 4 8.8.8.8
```

#### 4. Rate Limiting
```bash
# Add delays between requests
sleep 1

# Use proxy rotation
export HTTP_PROXY=http://proxy:port

# Implement custom rate limiting
```

### Performance Optimization

#### 1. Resource Management
- Monitor CPU and memory usage during scans
- Adjust thread counts based on system capabilities
- Use SSD storage for better I/O performance
- Close unnecessary applications during reconnaissance

#### 2. Network Optimization
- Use high-speed internet connections
- Configure DNS settings for faster resolution
- Implement connection pooling where possible
- Monitor bandwidth usage

#### 3. Tool-Specific Optimizations

```bash
# Subfinder optimization
subfinder -d target.com -all -silent -t 100

# Httpx optimization  
httpx -l domains.txt -threads 200 -silent -timeout 5

# Nuclei optimization
nuclei -l targets.txt -c 50 -rate-limit 150
```

## Reporting and Documentation

### Automated Report Generation

The platform generates structured reports in the following format:

```
results/target.com/YYYYMMDD_HHMMSS/
├── 01_initial_assessment/
│   └── scope_classification.txt
├── 02_subdomain_enum/
│   ├── all_subdomains.txt
│   └── live_subdomains.txt
├── 03_host_discovery/
│   └── live_hosts.txt
├── 04_port_scanning/
│   └── port_scan_results.txt
├── 05_vulnerability_scan/
│   └── nuclei_results.json
└── final_report/
    └── reconnaissance_summary.md
```

### Manual Report Enhancement

1. **Add Context**: Include background information about the target
2. **Prioritize Findings**: Rank discoveries by potential impact
3. **Document Methodology**: Explain reconnaissance approach used
4. **Include Proof**: Provide evidence for all findings
5. **Recommend Next Steps**: Suggest follow-up actions

### Export Options

- **JSON**: Machine-readable data export
- **CSV**: Spreadsheet-compatible format
- **Markdown**: Human-readable reports
- **XML**: Structured data exchange
- **PDF**: Professional report format (via conversion)

## Next Steps

After mastering basic usage:

1. Explore the [Tools Reference](tools.md) for detailed command options
2. Check the [API Documentation](api.md) for programmatic access
3. Join the community for tips and techniques
4. Contribute improvements and custom modules
5. Build custom integrations with existing workflows
