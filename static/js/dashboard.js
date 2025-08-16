// Bug Hunter Enhanced Dashboard - Dashboard specific JavaScript

class Dashboard {
    constructor() {
        this.refreshInterval = null;
        this.charts = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.startAutoRefresh();
        this.initializeCharts();
        this.loadRecentActivity();
    }

    setupEventListeners() {
        // Auto-refresh toggle
        const autoRefreshToggle = document.getElementById('autoRefresh');
        if (autoRefreshToggle) {
            autoRefreshToggle.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.startAutoRefresh();
                } else {
                    this.stopAutoRefresh();
                }
            });
        }

        // Refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshDashboard());
        }

        // Quick action buttons
        this.setupQuickActions();
    }

    setupQuickActions() {
        // New bug report
        const newBugBtn = document.getElementById('newBugReport');
        if (newBugBtn) {
            newBugBtn.addEventListener('click', () => {
                window.location.href = '/bug_reports';
            });
        }

        // Start recon
        const startReconBtn = document.getElementById('startRecon');
        if (startReconBtn) {
            startReconBtn.addEventListener('click', () => {
                window.location.href = '/recon';
            });
        }

        // Add note
        const addNoteBtn = document.getElementById('addNote');
        if (addNoteBtn) {
            addNoteBtn.addEventListener('click', () => {
                window.location.href = '/personal_notes';
            });
        }
    }

    async refreshDashboard() {
        try {
            const stats = await API.getDashboardStats();
            this.updateStatsCards(stats);
            this.updateCharts(stats);
            API.showToast('Dashboard refreshed successfully', 'success');
        } catch (error) {
            API.handleError(error, 'refreshing dashboard');
        }
    }

    updateStatsCards(stats) {
        // Update total bugs
        const totalBugsEl = document.getElementById('totalBugs');
        if (totalBugsEl) {
            this.animateNumber(totalBugsEl, stats.total_bugs || 0);
        }

        // Update active bugs
        const activeBugsEl = document.getElementById('activeBugs');
        if (activeBugsEl) {
            activeBugsEl.textContent = stats.active_bugs || 0;
        }

        // Update total bounties
        const totalBountiesEl = document.getElementById('totalBounties');
        if (totalBountiesEl) {
            const amount = stats.total_bounties || 0;
            totalBountiesEl.textContent = `$${amount.toFixed(2)}`;
        }

        // Update monthly earnings
        const monthlyEarningsEl = document.getElementById('monthlyEarnings');
        if (monthlyEarningsEl) {
            const amount = stats.monthly_earnings || 0;
            monthlyEarningsEl.textContent = `$${amount.toFixed(2)}`;
        }

        // Update platforms count
        const platformsCountEl = document.getElementById('platformsCount');
        if (platformsCountEl) {
            this.animateNumber(platformsCountEl, stats.platforms_count || 0);
        }

        // Update success rate
        const successRateEl = document.getElementById('successRate');
        if (successRateEl) {
            const rate = stats.success_rate || 0;
            this.animateNumber(successRateEl, rate, '%');
        }
    }

    animateNumber(element, targetValue, suffix = '') {
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000; // 1 second
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function for smooth animation
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.round(startValue + (targetValue - startValue) * easeOut);
            
            element.textContent = currentValue + suffix;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    initializeCharts() {
        // Platform distribution chart
        this.initializePlatformChart();
        
        // Vulnerability types chart
        this.initializeVulnerabilityChart();
        
        // Earnings trend chart
        this.initializeEarningsChart();
    }

    initializePlatformChart() {
        const canvas = document.getElementById('platformChart');
        if (!canvas) return;

        // Simple chart implementation using Canvas API
        const ctx = canvas.getContext('2d');
        this.charts.platform = new SimpleChart(ctx, 'doughnut');
    }

    initializeVulnerabilityChart() {
        const canvas = document.getElementById('vulnerabilityChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        this.charts.vulnerability = new SimpleChart(ctx, 'bar');
    }

    initializeEarningsChart() {
        const canvas = document.getElementById('earningsChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        this.charts.earnings = new SimpleChart(ctx, 'line');
    }

    updateCharts(stats) {
        // Update platform distribution
        if (this.charts.platform && stats.platform_distribution) {
            const data = Object.entries(stats.platform_distribution).map(([key, value]) => ({
                label: key,
                value: value
            }));
            this.charts.platform.update(data);
        }

        // Update vulnerability distribution
        if (this.charts.vulnerability && stats.vuln_distribution) {
            const data = Object.entries(stats.vuln_distribution).map(([key, value]) => ({
                label: key,
                value: value
            }));
            this.charts.vulnerability.update(data);
        }

        // Update earnings trend (mock data for now)
        if (this.charts.earnings) {
            const data = this.generateEarningsTrendData(stats.monthly_earnings || 0);
            this.charts.earnings.update(data);
        }
    }

    generateEarningsTrendData(currentMonthEarnings) {
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
        const data = [];
        
        for (let i = 0; i < months.length; i++) {
            const earnings = i === months.length - 1 
                ? currentMonthEarnings 
                : Math.random() * currentMonthEarnings;
            
            data.push({
                label: months[i],
                value: earnings
            });
        }
        
        return data;
    }

    async loadRecentActivity() {
        try {
            // Load recent campaigns
            const campaigns = await API.getReconCampaigns();
            this.updateRecentCampaigns(campaigns.data || []);

            // Load recent bug reports
            const bugs = await API.getBugReports();
            this.updateRecentBugReports(bugs.data || []);
        } catch (error) {
            console.error('Error loading recent activity:', error);
        }
    }

    updateRecentCampaigns(campaigns) {
        const container = document.getElementById('recentCampaigns');
        if (!container) return;

        if (campaigns.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-search text-muted" style="font-size: 3rem;"></i>
                    <h6 class="text-muted mt-3">No recent campaigns</h6>
                    <p class="text-muted">Start your first recon campaign</p>
                    <a href="/recon" class="btn btn-gradient">
                        <i class="bi bi-plus-lg me-1"></i>Start Campaign
                    </a>
                </div>
            `;
            return;
        }

        const campaignsHtml = campaigns.slice(0, 5).map(campaign => `
            <div class="d-flex align-items-center justify-content-between py-2">
                <div class="d-flex align-items-center">
                    <div class="rounded-circle bg-primary bg-opacity-10 p-2 me-3">
                        <i class="bi bi-globe text-primary"></i>
                    </div>
                    <div>
                        <div class="fw-medium">${campaign.target_domain}</div>
                        <small class="text-muted">${campaign.created_at}</small>
                    </div>
                </div>
                <span class="status-badge status-${campaign.status}">
                    ${campaign.status.charAt(0).toUpperCase() + campaign.status.slice(1)}
                </span>
            </div>
        `).join('');

        container.innerHTML = campaignsHtml;
    }

    updateRecentBugReports(bugs) {
        const container = document.getElementById('recentBugReports');
        if (!container) return;

        if (bugs.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-bug text-muted" style="font-size: 3rem;"></i>
                    <h6 class="text-muted mt-3">No bug reports yet</h6>
                    <a href="/bug_reports" class="btn btn-gradient">
                        <i class="bi bi-plus-lg me-1"></i>Add Bug Report
                    </a>
                </div>
            `;
            return;
        }

        const bugsHtml = bugs.slice(0, 5).map(bug => `
            <div class="d-flex align-items-center justify-content-between py-2">
                <div class="d-flex align-items-center">
                    <div class="rounded-circle bg-${this.getSeverityColor(bug.severity)} bg-opacity-10 p-2 me-3">
                        <i class="bi bi-bug text-${this.getSeverityColor(bug.severity)}"></i>
                    </div>
                    <div>
                        <div class="fw-medium">${bug.title}</div>
                        <small class="text-muted">${bug.platform || 'Unknown Platform'}</small>
                    </div>
                </div>
                <div class="text-end">
                    <span class="badge bg-${this.getSeverityColor(bug.severity)}">
                        ${bug.severity?.toUpperCase() || 'UNKNOWN'}
                    </span>
                    ${bug.bounty_amount ? `<div class="text-success fw-medium">$${bug.bounty_amount}</div>` : ''}
                </div>
            </div>
        `).join('');

        container.innerHTML = bugsHtml;
    }

    getSeverityColor(severity) {
        const colors = {
            'critical': 'danger',
            'high': 'warning',
            'medium': 'info',
            'low': 'secondary',
            'info': 'light'
        };
        return colors[severity] || 'secondary';
    }

    startAutoRefresh() {
        if (this.refreshInterval) return;
        
        this.refreshInterval = setInterval(() => {
            // Only refresh if page is visible
            if (!document.hidden) {
                this.refreshDashboard();
            }
        }, 30000); // Refresh every 30 seconds
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    destroy() {
        this.stopAutoRefresh();
        Object.values(this.charts).forEach(chart => {
            if (chart && chart.destroy) {
                chart.destroy();
            }
        });
    }
}

// Simple Chart implementation for basic charts
class SimpleChart {
    constructor(ctx, type) {
        this.ctx = ctx;
        this.type = type;
        this.data = [];
        this.colors = [
            '#667eea', '#764ba2', '#10b981', '#f59e0b', 
            '#ef4444', '#3b82f6', '#8b5cf6', '#06b6d4'
        ];
    }

    update(data) {
        this.data = data;
        this.draw();
    }

    draw() {
        const canvas = this.ctx.canvas;
        const width = canvas.width;
        const height = canvas.height;

        // Clear canvas
        this.ctx.clearRect(0, 0, width, height);

        if (this.data.length === 0) {
            this.drawNoData();
            return;
        }

        switch (this.type) {
            case 'doughnut':
                this.drawDoughnut();
                break;
            case 'bar':
                this.drawBar();
                break;
            case 'line':
                this.drawLine();
                break;
        }
    }

    drawNoData() {
        const canvas = this.ctx.canvas;
        const width = canvas.width;
        const height = canvas.height;

        this.ctx.fillStyle = '#9ca3af';
        this.ctx.font = '14px Inter, sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('No data available', width / 2, height / 2);
    }

    drawDoughnut() {
        const canvas = this.ctx.canvas;
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) - 20;
        const innerRadius = radius * 0.6;

        const total = this.data.reduce((sum, item) => sum + item.value, 0);
        let currentAngle = -Math.PI / 2;

        this.data.forEach((item, index) => {
            const sliceAngle = (item.value / total) * 2 * Math.PI;
            
            // Draw slice
            this.ctx.beginPath();
            this.ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
            this.ctx.arc(centerX, centerY, innerRadius, currentAngle + sliceAngle, currentAngle, true);
            this.ctx.closePath();
            this.ctx.fillStyle = this.colors[index % this.colors.length];
            this.ctx.fill();

            currentAngle += sliceAngle;
        });
    }

    drawBar() {
        const canvas = this.ctx.canvas;
        const padding = 40;
        const chartWidth = canvas.width - 2 * padding;
        const chartHeight = canvas.height - 2 * padding;

        if (this.data.length === 0) return;

        const maxValue = Math.max(...this.data.map(item => item.value));
        const barWidth = chartWidth / this.data.length;

        this.data.forEach((item, index) => {
            const barHeight = (item.value / maxValue) * chartHeight;
            const x = padding + index * barWidth;
            const y = padding + chartHeight - barHeight;

            // Draw bar
            this.ctx.fillStyle = this.colors[index % this.colors.length];
            this.ctx.fillRect(x + barWidth * 0.1, y, barWidth * 0.8, barHeight);

            // Draw label
            this.ctx.fillStyle = '#374151';
            this.ctx.font = '12px Inter, sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(
                item.label, 
                x + barWidth / 2, 
                canvas.height - 10
            );
        });
    }

    drawLine() {
        const canvas = this.ctx.canvas;
        const padding = 40;
        const chartWidth = canvas.width - 2 * padding;
        const chartHeight = canvas.height - 2 * padding;

        if (this.data.length === 0) return;

        const maxValue = Math.max(...this.data.map(item => item.value));
        const stepX = chartWidth / (this.data.length - 1);

        // Draw line
        this.ctx.beginPath();
        this.ctx.strokeStyle = this.colors[0];
        this.ctx.lineWidth = 3;

        this.data.forEach((item, index) => {
            const x = padding + index * stepX;
            const y = padding + chartHeight - (item.value / maxValue) * chartHeight;

            if (index === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }

            // Draw point
            this.ctx.beginPath();
            this.ctx.fillStyle = this.colors[0];
            this.ctx.arc(x, y, 4, 0, 2 * Math.PI);
            this.ctx.fill();
        });

        this.ctx.stroke();
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
        window.dashboard = new Dashboard();
    }
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (window.dashboard) {
        window.dashboard.destroy();
    }
});