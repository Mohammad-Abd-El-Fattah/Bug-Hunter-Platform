#!/bin/bash

# Bug Hunter's Reconnaissance Script
# Intelligent scope-based recon automation for Kali Linux
# Author: Security Researcher
# Version: 1.0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Global variables
TARGET=""
OUTPUT_DIR=""
SCOPE_SIZE=""
SUBDOMAIN_COUNT=0
LIVE_HOST_COUNT=0
START_TIME=$(date +%s)

# Banner function
banner() {
    echo -e "${PURPLE}"
    echo "╔══════════════════════════════════════════════════╗"
    echo "║           Bug Hunter's Recon Suite              ║"
    echo "║        Intelligent Scope-Based Automation        ║"
    echo "║              Version 1.0                         ║"
    echo "╚══════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Logging function
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

# Check dependencies module
check_dependencies() {
    log "Checking dependencies..."

    local tools=("subfinder" "assetfinder" "amass" "httpx" "naabu" "nuclei" 
                 "waybackurls" "gau" "katana" "gospider" "theHarvester" 
                 "ffuf" "nmap" "dig" "curl" "jq" "aws" "altdns" "massdns" 
                 "httprobe" "linkfinder" "secretfinder" "s3scanner" 
                 "dnsrecon" "asnmap" "gf" "subjack" "whatweb")

    local missing_tools=()

    for tool in "${tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done

    if [ ${#missing_tools[@]} -eq 0 ]; then
        log "All required tools are installed ✓"
    else
        error "Missing tools: ${missing_tools[*]}"
        echo -e "${YELLOW}Install missing tools with:${NC}"
        for tool in "${missing_tools[@]}"; do
            case $tool in
                "subfinder"|"httpx"|"nuclei"|"naabu")
                    echo "go install -v github.com/projectdiscovery/${tool}/cmd/${tool}@latest"
                    ;;
                "assetfinder")
                    echo "go install github.com/tomnomnom/assetfinder@latest"
                    ;;
                "amass")
                    echo "sudo apt install amass"
                    ;;
                "waybackurls")
                    echo "go install github.com/tomnomnom/waybackurls@latest"
                    ;;
                "gau")
                    echo "go install github.com/lc/gau/v2/cmd/gau@latest"
                    ;;
                "katana")
                    echo "go install github.com/projectdiscovery/katana/cmd/katana@latest"
                    ;;
                "gospider")
                    echo "sudo apt install gospider"
                    ;;
                "ffuf")
                    echo "sudo apt install ffuf"
                    ;;
                "s3scanner")
                    echo "pip3 install s3scanner"
                    ;;
                "linkfinder")
                    echo "git clone https://github.com/GerbenJavado/LinkFinder.git"
                    ;;
                "secretfinder")
                    echo "git clone https://github.com/m4ll0k/SecretFinder.git"
                    ;;
                "subjack")
                    echo "go install github.com/haccer/subjack@latest"
                    ;;
                *)
                    echo "sudo apt install $tool"
                    ;;
            esac
        done
        exit 1
    fi
}

# Create directory structure module
create_directory_structure() {
    log "Creating directory structure for $TARGET..."

    OUTPUT_DIR="results/$TARGET/$(date +%Y%m%d_%H%M%S)"

    mkdir -p "$OUTPUT_DIR"/{01_initial_assessment,02_subdomain_enum,03_host_discovery,04_port_scanning,05_crawling,06_vulnerability_scan,07_intelligence,08_technology_stack,09_cloud_assets,10_advanced_recon,final_report}

    # Create subdirectories for each phase
    mkdir -p "$OUTPUT_DIR/02_subdomain_enum"/{passive,active,permutation}
    mkdir -p "$OUTPUT_DIR/03_host_discovery"/{http,https,alive}
    mkdir -p "$OUTPUT_DIR/04_port_scanning"/{tcp,udp,service_scan}
    mkdir -p "$OUTPUT_DIR/05_crawling"/{endpoints,parameters,js_files}
    mkdir -p "$OUTPUT_DIR/06_vulnerability_scan"/{nuclei,secrets,misconfigs}
    mkdir -p "$OUTPUT_DIR/07_intelligence"/{osint,wayback,github}
    mkdir -p "$OUTPUT_DIR/08_technology_stack"/{cms,frameworks,versions}
    mkdir -p "$OUTPUT_DIR/09_cloud_assets"/{s3,azure,gcp}
    mkdir -p "$OUTPUT_DIR/10_advanced_recon"/{asn,certificates,dns}

    log "Directory structure created at: $OUTPUT_DIR"
}

# Setup DNS resolvers module
setup_dns_resolvers() {
    log "Setting up DNS resolvers..."

    # Download public DNS resolvers
    curl -s https://public-dns.info/nameservers.txt | head -100 > "$OUTPUT_DIR/resolvers.txt"

    # Add popular resolvers
    cat >> "$OUTPUT_DIR/resolvers.txt" << EOF
8.8.8.8
8.8.4.4
1.1.1.1
1.0.0.1
9.9.9.9
149.112.112.112
208.67.222.222
208.67.220.220
EOF

    sort -u "$OUTPUT_DIR/resolvers.txt" -o "$OUTPUT_DIR/resolvers.txt"
    log "DNS resolvers configured: $(wc -l < "$OUTPUT_DIR/resolvers.txt") resolvers"
}

# Fast subdomain enumeration module
module_fast_subdomain_enum() {
    log "Starting fast subdomain enumeration..."

    # Subfinder - fast passive enumeration
    subfinder -d "$TARGET" -all -silent > "$OUTPUT_DIR/02_subdomain_enum/passive/subfinder.txt" 2>/dev/null

    # Assetfinder - additional passive sources
    assetfinder --subs-only "$TARGET" > "$OUTPUT_DIR/02_subdomain_enum/passive/assetfinder.txt" 2>/dev/null

    # Certificate transparency
    curl -s "https://crt.sh/?q=%25.$TARGET&output=json" | jq -r '.[].name_value' | sed 's/\*.//g' | sort -u > "$OUTPUT_DIR/02_subdomain_enum/passive/crtsh.txt" 2>/dev/null

    # Combine results
    cat "$OUTPUT_DIR/02_subdomain_enum/passive/"*.txt | sort -u > "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt"

    SUBDOMAIN_COUNT=$(wc -l < "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt")
    log "Fast enumeration found $SUBDOMAIN_COUNT subdomains"
}

# Host discovery module
module_host_discovery() {
    log "Starting host discovery..."

    # Check which subdomains are alive
    httpx -l "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt" -silent -timeout 10 > "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" 2>/dev/null

    # Separate HTTP and HTTPS
    grep "^http://" "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" > "$OUTPUT_DIR/03_host_discovery/http/http_hosts.txt" 2>/dev/null
    grep "^https://" "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" > "$OUTPUT_DIR/03_host_discovery/https/https_hosts.txt" 2>/dev/null

    LIVE_HOST_COUNT=$(wc -l < "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt")
    log "Host discovery found $LIVE_HOST_COUNT live hosts"
}

# Scope classification function
classify_scope() {
    log "Classifying target scope..."

    if [ "$SUBDOMAIN_COUNT" -lt 50 ] && [ "$LIVE_HOST_COUNT" -lt 10 ]; then
        SCOPE_SIZE="SMALL"
    elif [ "$SUBDOMAIN_COUNT" -le 300 ] && [ "$LIVE_HOST_COUNT" -lt 100 ]; then
        SCOPE_SIZE="MEDIUM"
    else
        SCOPE_SIZE="LARGE"
    fi

    echo "Target: $TARGET" > "$OUTPUT_DIR/01_initial_assessment/scope_classification.txt"
    echo "Subdomains: $SUBDOMAIN_COUNT" >> "$OUTPUT_DIR/01_initial_assessment/scope_classification.txt"
    echo "Live Hosts: $LIVE_HOST_COUNT" >> "$OUTPUT_DIR/01_initial_assessment/scope_classification.txt"
    echo "Scope Size: $SCOPE_SIZE" >> "$OUTPUT_DIR/01_initial_assessment/scope_classification.txt"
    echo "Timestamp: $(date)" >> "$OUTPUT_DIR/01_initial_assessment/scope_classification.txt"

    info "Target classified as: ${SCOPE_SIZE} scope"
    info "Subdomains: $SUBDOMAIN_COUNT | Live hosts: $LIVE_HOST_COUNT"
}

# OSINT module
module_osint() {
    log "Starting OSINT collection..."

    # theHarvester for email and host enumeration
    theHarvester -d "$TARGET" -b google,bing,duckduckgo -l 500 -f "$OUTPUT_DIR/07_intelligence/osint/theharvester_$TARGET" 2>/dev/null

    # Wayback URLs
    waybackurls "$TARGET" | head -10000 > "$OUTPUT_DIR/07_intelligence/wayback/wayback_urls.txt" 2>/dev/null

    # GAU for additional URLs
    gau "$TARGET" | head -10000 > "$OUTPUT_DIR/07_intelligence/wayback/gau_urls.txt" 2>/dev/null

    # Combine wayback data
    cat "$OUTPUT_DIR/07_intelligence/wayback/"*.txt | sort -u > "$OUTPUT_DIR/07_intelligence/wayback/combined_urls.txt"

    log "OSINT collection completed"
}

# Slow subdomain enumeration module
module_slow_subdomain_enum() {
    log "Starting comprehensive subdomain enumeration..."

    # Amass passive enumeration
    amass enum -passive -d "$TARGET" -o "$OUTPUT_DIR/02_subdomain_enum/passive/amass.txt" 2>/dev/null

    # Active DNS brute forcing with common wordlist
    if command -v ffuf &> /dev/null; then
        # Use ffuf for DNS fuzzing if available
        ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt:FUZZ -u "http://FUZZ.$TARGET" -mc 200,204,301,302,307,401,403,405,500 -o "$OUTPUT_DIR/02_subdomain_enum/active/ffuf_dns.json" -of json -t 50 2>/dev/null
    fi

    # Altdns for permutation-based discovery
    if [ -f "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt" ]; then
        altdns -i "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt" -o "$OUTPUT_DIR/02_subdomain_enum/permutation/altdns.txt" -w /usr/share/seclists/Discovery/DNS/alterations.txt 2>/dev/null
    fi

    log "Comprehensive subdomain enumeration completed"
}

# Subdomain categorization module
module_subdomain_categorization() {
    log "Categorizing subdomains by function..."

    # Extract potential categories from subdomain names
    grep -i "admin\|panel\|dashboard" "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt" > "$OUTPUT_DIR/02_subdomain_enum/categories/admin_panels.txt" 2>/dev/null
    grep -i "api\|rest\|graphql" "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt" > "$OUTPUT_DIR/02_subdomain_enum/categories/apis.txt" 2>/dev/null
    grep -i "dev\|test\|staging\|uat" "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt" > "$OUTPUT_DIR/02_subdomain_enum/categories/development.txt" 2>/dev/null
    grep -i "mail\|smtp\|imap\|pop" "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt" > "$OUTPUT_DIR/02_subdomain_enum/categories/mail_servers.txt" 2>/dev/null

    mkdir -p "$OUTPUT_DIR/02_subdomain_enum/categories"

    log "Subdomain categorization completed"
}

# Port scanning module
module_port_scanning() {
    log "Starting port scanning..."

    # Extract IPs from live hosts
    cut -d'/' -f3 "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" | cut -d':' -f1 | sort -u > "$OUTPUT_DIR/04_port_scanning/target_ips.txt"

    # Naabu for fast port discovery
    if [ -s "$OUTPUT_DIR/04_port_scanning/target_ips.txt" ]; then
        naabu -l "$OUTPUT_DIR/04_port_scanning/target_ips.txt" -top-ports 1000 -o "$OUTPUT_DIR/04_port_scanning/tcp/naabu_ports.txt" 2>/dev/null

        # Nmap service detection on discovered ports
        if [ -s "$OUTPUT_DIR/04_port_scanning/tcp/naabu_ports.txt" ]; then
            nmap -sV -sC -iL "$OUTPUT_DIR/04_port_scanning/target_ips.txt" -oA "$OUTPUT_DIR/04_port_scanning/service_scan/nmap_services" 2>/dev/null
        fi
    fi

    log "Port scanning completed"
}

# Crawling and analysis module
module_crawling_and_analysis() {
    log "Starting web crawling and analysis..."

    # Katana for modern crawling
    katana -list "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" -d 3 -o "$OUTPUT_DIR/05_crawling/endpoints/katana_endpoints.txt" 2>/dev/null

    # Gospider for additional crawling
    gospider -S "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" -d 2 -c 10 --other-source -o "$OUTPUT_DIR/05_crawling/endpoints/gospider_output" 2>/dev/null

    # Extract JavaScript files
    grep -i "\.js" "$OUTPUT_DIR/05_crawling/endpoints/katana_endpoints.txt" > "$OUTPUT_DIR/05_crawling/js_files/javascript_files.txt" 2>/dev/null

    # Extract parameters from URLs
    cat "$OUTPUT_DIR/05_crawling/endpoints/katana_endpoints.txt" | grep "?" | sed 's/.*?//g' | tr '&' '\n' | cut -d'=' -f1 | sort -u > "$OUTPUT_DIR/05_crawling/parameters/parameters.txt" 2>/dev/null

    log "Web crawling completed"
}

# Vulnerability scanning module
module_vuln_scanning() {
    log "Starting vulnerability scanning..."

    # Nuclei scanning
    nuclei -l "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" -t ~/nuclei-templates/ -o "$OUTPUT_DIR/06_vulnerability_scan/nuclei/nuclei_results.txt" 2>/dev/null

    # Secret finder on JS files
    if [ -s "$OUTPUT_DIR/05_crawling/js_files/javascript_files.txt" ]; then
        while read -r js_url; do
            python3 ~/tools/SecretFinder/SecretFinder.py -i "$js_url" -o cli >> "$OUTPUT_DIR/06_vulnerability_scan/secrets/js_secrets.txt" 2>/dev/null
        done < "$OUTPUT_DIR/05_crawling/js_files/javascript_files.txt"
    fi

    # S3 bucket enumeration
    s3scanner scan --bucket-file <(echo "$TARGET" | sed 's/\./-/g') > "$OUTPUT_DIR/09_cloud_assets/s3/s3_buckets.txt" 2>/dev/null

    # Subjack for subdomain takeover
    subjack -w "$OUTPUT_DIR/02_subdomain_enum/passive_combined.txt" -o "$OUTPUT_DIR/06_vulnerability_scan/nuclei/subjack_results.txt" 2>/dev/null

    log "Vulnerability scanning completed"
}

# Technology stack analysis module
module_technology_analysis() {
    log "Analyzing technology stack..."

    # WhatWeb for technology detection
    whatweb --log-brief="$OUTPUT_DIR/08_technology_stack/whatweb_results.txt" -i "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" 2>/dev/null

    # HTTPx with technology detection
    httpx -l "$OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt" -tech-detect -title -status-code -o "$OUTPUT_DIR/08_technology_stack/httpx_tech.txt" 2>/dev/null

    log "Technology analysis completed"
}

# Advanced reconnaissance module (for medium/large scopes)
module_advanced_recon() {
    log "Starting advanced reconnaissance..."

    # ASN enumeration
    asnmap -d "$TARGET" -o "$OUTPUT_DIR/10_advanced_recon/asn/asn_info.txt" 2>/dev/null

    # DNS record enumeration
    dnsrecon -d "$TARGET" -t std,rvl,srv,ptr,mx,soa,txt -c "$OUTPUT_DIR/10_advanced_recon/dns/dnsrecon_results.csv" 2>/dev/null

    # Certificate analysis
    echo | openssl s_client -connect "$TARGET:443" 2>/dev/null | openssl x509 -text > "$OUTPUT_DIR/10_advanced_recon/certificates/ssl_cert.txt" 2>/dev/null

    log "Advanced reconnaissance completed"
}

# Execute modules based on scope size
execute_scope_modules() {
    case $SCOPE_SIZE in
        "SMALL")
            log "Executing SMALL scope modules..."
            module_technology_analysis
            module_port_scanning
            module_crawling_and_analysis
            module_vuln_scanning
            ;;
        "MEDIUM")
            log "Executing MEDIUM scope modules..."
            module_slow_subdomain_enum
            module_subdomain_categorization
            module_technology_analysis
            module_port_scanning
            module_crawling_and_analysis
            module_vuln_scanning
            module_advanced_recon
            ;;
        "LARGE")
            log "Executing LARGE scope modules..."
            module_slow_subdomain_enum
            module_subdomain_categorization
            module_technology_analysis
            module_port_scanning
            module_crawling_and_analysis
            module_vuln_scanning
            module_advanced_recon
            ;;
    esac
}

# Generate final report
generate_report() {
    log "Generating final report..."

    local report_file="$OUTPUT_DIR/final_report/reconnaissance_report.md"
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))

    cat > "$report_file" << EOF
# Reconnaissance Report for $TARGET

## Executive Summary
- **Target**: $TARGET
- **Scope Classification**: $SCOPE_SIZE
- **Scan Date**: $(date)
- **Scan Duration**: ${duration} seconds
- **Subdomains Found**: $SUBDOMAIN_COUNT
- **Live Hosts**: $LIVE_HOST_COUNT

## Key Findings

### Subdomains Discovered
- Total subdomains: $SUBDOMAIN_COUNT
- Live hosts: $LIVE_HOST_COUNT
- Admin panels: $([ -f "$OUTPUT_DIR/02_subdomain_enum/categories/admin_panels.txt" ] && wc -l < "$OUTPUT_DIR/02_subdomain_enum/categories/admin_panels.txt" || echo "0")
- APIs detected: $([ -f "$OUTPUT_DIR/02_subdomain_enum/categories/apis.txt" ] && wc -l < "$OUTPUT_DIR/02_subdomain_enum/categories/apis.txt" || echo "0")
- Development environments: $([ -f "$OUTPUT_DIR/02_subdomain_enum/categories/development.txt" ] && wc -l < "$OUTPUT_DIR/02_subdomain_enum/categories/development.txt" || echo "0")

### Security Findings
- Nuclei vulnerabilities: $([ -f "$OUTPUT_DIR/06_vulnerability_scan/nuclei/nuclei_results.txt" ] && wc -l < "$OUTPUT_DIR/06_vulnerability_scan/nuclei/nuclei_results.txt" || echo "0")
- Potential subdomain takeovers: $([ -f "$OUTPUT_DIR/06_vulnerability_scan/nuclei/subjack_results.txt" ] && wc -l < "$OUTPUT_DIR/06_vulnerability_scan/nuclei/subjack_results.txt" || echo "0")
- JavaScript secrets: $([ -f "$OUTPUT_DIR/06_vulnerability_scan/secrets/js_secrets.txt" ] && wc -l < "$OUTPUT_DIR/06_vulnerability_scan/secrets/js_secrets.txt" || echo "0")

### Recommendations
1. Review all discovered admin panels and development environments
2. Analyze high-priority vulnerabilities from Nuclei scan
3. Investigate potential subdomain takeover opportunities
4. Review exposed secrets in JavaScript files
5. Perform manual testing on high-value targets

## File Locations
- All scan results: $OUTPUT_DIR
- Live hosts: $OUTPUT_DIR/03_host_discovery/alive/live_hosts.txt
- Vulnerability scan: $OUTPUT_DIR/06_vulnerability_scan/
- Technology stack: $OUTPUT_DIR/08_technology_stack/

EOF

    log "Report generated: $report_file"
}

# Help function
usage() {
    echo -e "${CYAN}Usage: $0 -d <domain> [OPTIONS]${NC}"
    echo ""
    echo "Options:"
    echo "  -d, --domain     Target domain (required)"
    echo "  -o, --output     Output directory (default: results/)"
    echo "  -s, --scope      Force scope size (small|medium|large)"
    echo "  -v, --verbose    Enable verbose output"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 -d example.com"
    echo "  $0 -d example.com -s large -v"
    echo "  $0 -d example.com -o /tmp/recon_results"
}

# Main function
main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--domain)
                TARGET="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_DIR="$2"
                shift 2
                ;;
            -s|--scope)
                SCOPE_SIZE="$2"
                shift 2
                ;;
            -v|--verbose)
                set -x
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done

    # Validate input
    if [ -z "$TARGET" ]; then
        error "Target domain is required"
        usage
        exit 1
    fi

    # Display banner
    banner

    # Execute modules
    check_dependencies
    create_directory_structure
    setup_dns_resolvers

    # Initial reconnaissance
    module_fast_subdomain_enum
    module_host_discovery
    module_osint

    # Classify scope if not forced
    if [ -z "$SCOPE_SIZE" ]; then
        classify_scope
    else
        log "Using forced scope: $SCOPE_SIZE"
    fi

    # Execute scope-appropriate modules
    execute_scope_modules

    # Generate final report
    generate_report

    log "Reconnaissance completed! Results saved to: $OUTPUT_DIR"
    info "Total runtime: $(($(date +%s) - START_TIME)) seconds"
}

# Run main function with all arguments
main "$@"
