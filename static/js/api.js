// Bug Hunter Enhanced Dashboard - API Functions

class API {
    static baseUrl = '';
    static timeout = 30000; // 30 seconds

    // Generic API request handler
    static async request(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: this.timeout
        };

        const config = { ...defaultOptions, ...options };
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), config.timeout);
            
            config.signal = controller.signal;
            
            const response = await fetch(this.baseUrl + url, config);
            clearTimeout(timeoutId);
            
            const data = await response.json().catch(() => ({}));
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
            }
            
            return data;
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('Request timeout');
            }
            throw error;
        }
    }

    // Platform API methods
    static async getPlatforms() {
        return this.request('/api/platforms');
    }

    static async createPlatform(data) {
        return this.request('/api/platforms', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async updatePlatform(id, data) {
        return this.request(`/api/platforms/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deletePlatform(id) {
        return this.request(`/api/platforms/${id}`, {
            method: 'DELETE'
        });
    }

    // Bug Reports API methods
    static async getBugReports() {
        return this.request('/api/bugs');
    }

    static async getBugReport(id) {
        return this.request(`/api/bugs/${id}`);
    }

    static async createBugReport(data) {
        return this.request('/api/bugs', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async updateBugReport(id, data) {
        return this.request(`/api/bugs/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteBugReport(id) {
        return this.request(`/api/bugs/${id}`, {
            method: 'DELETE'
        });
    }

    // Notes API methods
    static async getNotes() {
        return this.request('/api/notes');
    }

    static async getNote(id) {
        return this.request(`/api/notes/${id}`);
    }

    static async createNote(data) {
        return this.request('/api/notes', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async updateNote(id, data) {
        return this.request(`/api/notes/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteNote(id) {
        return this.request(`/api/notes/${id}`, {
            method: 'DELETE'
        });
    }

    static async toggleNotePin(id) {
        return this.request(`/api/notes/${id}/toggle-pin`, {
            method: 'PATCH'
        });
    }

    // Tips & Tricks API methods
    static async getTips() {
        return this.request('/api/tips');
    }

    static async createTip(data) {
        return this.request('/api/tips', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async updateTip(id, data) {
        return this.request(`/api/tips/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteTip(id) {
        return this.request(`/api/tips/${id}`, {
            method: 'DELETE'
        });
    }

    // Reading List API methods
    static async getReadingList() {
        return this.request('/api/reading');
    }

    static async createReading(data) {
        return this.request('/api/reading', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async updateReading(id, data) {
        return this.request(`/api/reading/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteReading(id) {
        return this.request(`/api/reading/${id}`, {
            method: 'DELETE'
        });
    }

    static async markReadingRead(id) {
        return this.request(`/api/reading/${id}/mark-read`, {
            method: 'PATCH'
        });
    }

    // Useful Links API methods
    static async getLinks() {
        return this.request('/api/links');
    }

    static async createLink(data) {
        return this.request('/api/links', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async updateLink(id, data) {
        return this.request(`/api/links/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteLink(id) {
        return this.request(`/api/links/${id}`, {
            method: 'DELETE'
        });
    }

    // Security Checklist API methods
    static async getChecklists() {
        return this.request('/api/checklists');
    }

    static async createChecklist(data) {
        return this.request('/api/checklists', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async updateChecklist(id, data) {
        return this.request(`/api/checklists/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteChecklist(id) {
        return this.request(`/api/checklists/${id}`, {
            method: 'DELETE'
        });
    }

    static async importChecklist(githubUrl) {
        return this.request('/api/checklists/import', {
            method: 'POST',
            body: JSON.stringify({ github_url: githubUrl })
        });
    }

    // Recon API methods
    static async startRecon(data) {
        return this.request('/api/recon/start', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async getReconCampaigns() {
        return this.request('/api/recon/campaigns');
    }

    static async getReconCampaign(id) {
        return this.request(`/api/campaigns/${id}`);
    }

    static async stopReconCampaign(id) {
        return this.request(`/api/campaigns/${id}/stop`, {
            method: 'PATCH'
        });
    }

    static async deleteReconCampaign(id) {
        return this.request(`/api/campaigns/${id}`, {
            method: 'DELETE'
        });
    }

    // Attack API methods
    static async uploadAttackScript(formData) {
        return this.request('/api/attack/upload', {
            method: 'POST',
            headers: {}, // Remove Content-Type for FormData
            body: formData
        });
    }

    static async getAttackScripts() {
        return this.request('/api/attack/scripts');
    }

    static async startAttack(scriptId, target, options = {}) {
        return this.request('/api/attack/start', {
            method: 'POST',
            body: JSON.stringify({
                script_id: scriptId,
                target: target,
                options: options
            })
        });
    }

    static async stopAttack(executionId) {
        return this.request(`/api/attack/${executionId}/stop`, {
            method: 'PATCH'
        });
    }

    static async deleteAttackScript(scriptId) {
        return this.request(`/api/attack/scripts/${scriptId}`, {
            method: 'DELETE'
        });
    }

    // Exploit API methods
    static async uploadExploitScript(formData) {
        return this.request('/api/exploit/upload', {
            method: 'POST',
            headers: {}, // Remove Content-Type for FormData
            body: formData
        });
    }

    static async getExploitScripts() {
        return this.request('/api/exploit/scripts');
    }

    static async startExploit(scriptId, target, options = {}) {
        return this.request('/api/exploit/start', {
            method: 'POST',
            body: JSON.stringify({
                script_id: scriptId,
                target: target,
                options: options
            })
        });
    }

    static async stopExploit(executionId) {
        return this.request(`/api/exploit/${executionId}/stop`, {
            method: 'PATCH'
        });
    }

    static async deleteExploitScript(scriptId) {
        return this.request(`/api/exploit/scripts/${scriptId}`, {
            method: 'DELETE'
        });
    }

    // Script Execution API methods
    static async getExecutionLogs(executionId) {
        return this.request(`/api/executions/${executionId}/logs`);
    }

    static async getExecutionStatus(executionId) {
        return this.request(`/api/executions/${executionId}/status`);
    }

    // News API methods
    static async getNews() {
        return this.request('/api/news');
    }

    static async markNewsRead(newsId) {
        return this.request(`/api/news/${newsId}/mark-read`, {
            method: 'PATCH'
        });
    }

    static async refreshNews() {
        return this.request('/api/news/refresh', {
            method: 'POST'
        });
    }

    // Target API methods
    static async getTargets() {
        return this.request('/api/targets');
    }

    static async createTarget(data) {
        return this.request('/api/targets', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    static async updateTarget(id, data) {
        return this.request(`/api/targets/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    static async deleteTarget(id) {
        return this.request(`/api/targets/${id}`, {
            method: 'DELETE'
        });
    }

    // Dashboard Stats
    static async getDashboardStats() {
        return this.request('/api/dashboard/stats');
    }

    // File upload helper
    static async uploadFile(file, type = 'general') {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', type);
        
        return this.request('/api/upload', {
            method: 'POST',
            headers: {}, // Remove Content-Type for FormData
            body: formData
        });
    }

    // Utility methods
    static showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        if (!toast) return;

        const toastBody = toast.querySelector('.toast-body');
        const toastIcon = toast.querySelector('i');
        
        toastBody.textContent = message;
        
        // Update icon based on type
        const iconClasses = {
            'success': 'bi-check-circle-fill text-success',
            'error': 'bi-exclamation-triangle-fill text-danger',
            'warning': 'bi-exclamation-circle-fill text-warning',
            'info': 'bi-info-circle-fill text-primary'
        };
        
        toastIcon.className = `bi me-2 ${iconClasses[type] || iconClasses['info']}`;
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    }

    static showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi ${this.getNotificationIcon(type)} me-2"></i>
                <span>${message}</span>
                <button class="btn-close btn-close-white ms-2" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    static getNotificationIcon(type) {
        const icons = {
            'success': 'bi-check-circle-fill',
            'error': 'bi-exclamation-triangle-fill',
            'warning': 'bi-exclamation-circle-fill',
            'info': 'bi-info-circle-fill'
        };
        return icons[type] || icons['info'];
    }

    // Error handler
    static handleError(error, context = '') {
        console.error(`API Error ${context}:`, error);
        
        let message = 'An unexpected error occurred';
        if (error.message) {
            message = error.message;
        }
        
        this.showToast(message, 'error');
        return { error: true, message };
    }

    // Loading state handler
    static setLoading(element, loading = true) {
        if (loading) {
            element.classList.add('loading');
            element.disabled = true;
        } else {
            element.classList.remove('loading');
            element.disabled = false;
        }
    }
}

// Export for use in other modules
window.API = API;