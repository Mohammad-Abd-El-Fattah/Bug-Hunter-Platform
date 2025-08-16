// Bug Hunter Enhanced Dashboard - Reusable Components

// File Upload Component
class FileUploader {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            maxSize: 10 * 1024 * 1024, // 10MB
            allowedTypes: ['text/plain', 'application/x-sh', 'text/x-shellscript'],
            onUpload: null,
            onProgress: null,
            onError: null,
            ...options
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupDropZone();
    }

    setupEventListeners() {
        const fileInput = this.element.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }
    }

    setupDropZone() {
        const dropZone = this.element.querySelector('.file-upload-zone');
        if (!dropZone) return;

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            const files = Array.from(e.dataTransfer.files);
            this.processFiles(files);
        });
    }

    handleFileSelect(event) {
        const files = Array.from(event.target.files);
        this.processFiles(files);
    }

    processFiles(files) {
        files.forEach(file => {
            if (this.validateFile(file)) {
                this.uploadFile(file);
            }
        });
    }

    validateFile(file) {
        // Check file size
        if (file.size > this.options.maxSize) {
            this.handleError(`File ${file.name} is too large. Maximum size is ${this.formatBytes(this.options.maxSize)}.`);
            return false;
        }

        // Check file type
        if (this.options.allowedTypes.length > 0 && !this.options.allowedTypes.includes(file.type)) {
            this.handleError(`File ${file.name} has an invalid type. Allowed types: ${this.options.allowedTypes.join(', ')}.`);
            return false;
        }

        return true;
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            if (this.options.onProgress) {
                this.options.onProgress(0);
            }

            const result = await API.uploadFile(file, this.options.type || 'script');
            
            if (this.options.onProgress) {
                this.options.onProgress(100);
            }

            if (this.options.onUpload) {
                this.options.onUpload(result, file);
            }

            API.showToast(`File ${file.name} uploaded successfully!`, 'success');
        } catch (error) {
            this.handleError(`Failed to upload ${file.name}: ${error.message}`);
        }
    }

    handleError(message) {
        if (this.options.onError) {
            this.options.onError(message);
        } else {
            API.showToast(message, 'error');
        }
    }

    formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Script Editor Component
class ScriptEditor {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            language: 'bash',
            theme: 'dark',
            onChange: null,
            ...options
        };
        this.init();
    }

    init() {
        this.setupEditor();
        this.setupEventListeners();
    }

    setupEditor() {
        this.element.classList.add('script-editor');
        this.element.setAttribute('spellcheck', 'false');
        
        // Add line numbers
        this.addLineNumbers();
    }

    setupEventListeners() {
        this.element.addEventListener('input', () => {
            this.updateLineNumbers();
            if (this.options.onChange) {
                this.options.onChange(this.getValue());
            }
        });

        this.element.addEventListener('scroll', () => {
            this.syncLineNumbers();
        });

        this.element.addEventListener('keydown', (e) => {
            this.handleKeyDown(e);
        });
    }

    addLineNumbers() {
        const container = document.createElement('div');
        container.className = 'script-editor-container';
        container.style.position = 'relative';
        
        const lineNumbers = document.createElement('div');
        lineNumbers.className = 'line-numbers';
        lineNumbers.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 40px;
            height: 100%;
            background: #2a2a2a;
            color: #666;
            font-family: inherit;
            font-size: inherit;
            line-height: inherit;
            padding: 1rem 0.5rem;
            border-right: 1px solid #444;
            user-select: none;
            overflow: hidden;
        `;

        this.element.parentNode.insertBefore(container, this.element);
        container.appendChild(lineNumbers);
        container.appendChild(this.element);
        
        this.element.style.paddingLeft = '50px';
        this.lineNumbers = lineNumbers;
        
        this.updateLineNumbers();
    }

    updateLineNumbers() {
        if (!this.lineNumbers) return;
        
        const lines = this.element.value.split('\n').length;
        const numbers = Array.from({length: lines}, (_, i) => i + 1).join('\n');
        this.lineNumbers.textContent = numbers;
    }

    syncLineNumbers() {
        if (!this.lineNumbers) return;
        this.lineNumbers.scrollTop = this.element.scrollTop;
    }

    handleKeyDown(e) {
        // Tab support
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = this.element.selectionStart;
            const end = this.element.selectionEnd;
            
            this.element.value = this.element.value.substring(0, start) + 
                                '    ' + 
                                this.element.value.substring(end);
            
            this.element.selectionStart = this.element.selectionEnd = start + 4;
            this.updateLineNumbers();
        }
    }

    getValue() {
        return this.element.value;
    }

    setValue(value) {
        this.element.value = value;
        this.updateLineNumbers();
    }

    clear() {
        this.setValue('');
    }
}

// Log Viewer Component
class LogViewer {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            autoScroll: true,
            maxLines: 1000,
            refreshInterval: 2000,
            executionId: null,
            ...options
        };
        this.logs = [];
        this.refreshTimer = null;
        this.init();
    }

    init() {
        this.element.classList.add('log-viewer');
        this.startRefresh();
    }

    startRefresh() {
        if (!this.options.executionId) return;
        
        this.refreshTimer = setInterval(async () => {
            await this.fetchLogs();
        }, this.options.refreshInterval);
        
        // Initial fetch
        this.fetchLogs();
    }

    stopRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }

    async fetchLogs() {
        try {
            const response = await API.getExecutionLogs(this.options.executionId);
            this.updateLogs(response.logs || []);
        } catch (error) {
            console.error('Failed to fetch logs:', error);
        }
    }

    updateLogs(newLogs) {
        this.logs = [...this.logs, ...newLogs];
        
        // Limit log lines
        if (this.logs.length > this.options.maxLines) {
            this.logs = this.logs.slice(-this.options.maxLines);
        }
        
        this.render();
    }

    render() {
        const logContent = this.logs.map(log => {
            const timestamp = new Date(log.timestamp).toLocaleTimeString();
            return `[${timestamp}] ${log.level.toUpperCase()}: ${log.message}`;
        }).join('\n');
        
        this.element.textContent = logContent;
        
        if (this.options.autoScroll) {
            this.element.scrollTop = this.element.scrollHeight;
        }
    }

    addLog(level, message) {
        this.logs.push({
            timestamp: new Date().toISOString(),
            level: level,
            message: message
        });
        this.render();
    }

    clear() {
        this.logs = [];
        this.render();
    }

    destroy() {
        this.stopRefresh();
    }
}

// Progress Bar Component
class ProgressBar {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            animated: true,
            showText: true,
            ...options
        };
        this.progress = 0;
        this.init();
    }

    init() {
        this.element.innerHTML = `
            <div class="progress-container">
                <div class="progress-bar" style="width: 0%"></div>
            </div>
            ${this.options.showText ? '<div class="progress-text">0%</div>' : ''}
        `;
        
        this.progressBar = this.element.querySelector('.progress-bar');
        this.progressText = this.element.querySelector('.progress-text');
    }

    setProgress(value) {
        this.progress = Math.max(0, Math.min(100, value));
        
        if (this.options.animated) {
            this.progressBar.style.transition = 'width 0.3s ease';
        }
        
        this.progressBar.style.width = `${this.progress}%`;
        
        if (this.progressText) {
            this.progressText.textContent = `${Math.round(this.progress)}%`;
        }
        
        // Add completion class
        if (this.progress >= 100) {
            this.element.classList.add('completed');
        } else {
            this.element.classList.remove('completed');
        }
    }

    reset() {
        this.setProgress(0);
    }
}

// Target Selector Component
class TargetSelector {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            multiple: false,
            onSelectionChange: null,
            ...options
        };
        this.selectedTargets = [];
        this.init();
    }

    init() {
        this.loadTargets();
        this.setupEventListeners();
    }

    async loadTargets() {
        try {
            const response = await API.getTargets();
            this.renderTargets(response.data || []);
        } catch (error) {
            console.error('Failed to load targets:', error);
            this.renderEmptyState();
        }
    }

    renderTargets(targets) {
        if (targets.length === 0) {
            this.renderEmptyState();
            return;
        }

        const targetsHtml = targets.map(target => `
            <div class="target-selector" data-target-id="${target.id}">
                <div class="target-selector-header">
                    <div class="target-selector-icon">
                        <i class="bi bi-globe"></i>
                    </div>
                    <div>
                        <h6 class="target-selector-title">${target.domain}</h6>
                        <div class="target-selector-url">${target.url || target.domain}</div>
                    </div>
                    ${!this.options.multiple ? '<input type="radio" name="target" class="form-check-input">' : 
                      '<input type="checkbox" class="form-check-input">'}
                </div>
                <div class="target-selector-meta">
                    <span>Scope: ${target.scope_type || 'In-scope'}</span>
                    <span>Platform: ${target.platform || 'Web'}</span>
                    <span>Added: ${target.created_at || 'Recently'}</span>
                </div>
            </div>
        `).join('');

        this.element.innerHTML = targetsHtml;
    }

    renderEmptyState() {
        this.element.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-target text-muted" style="font-size: 3rem;"></i>
                <h6 class="text-muted mt-3">No targets available</h6>
                <p class="text-muted">Add targets from the Platforms page</p>
                <a href="/platforms" class="btn btn-outline-primary">
                    <i class="bi bi-plus-lg me-1"></i>Add Targets
                </a>
            </div>
        `;
    }

    setupEventListeners() {
        this.element.addEventListener('change', (e) => {
            if (e.target.type === 'radio' || e.target.type === 'checkbox') {
                this.handleSelectionChange(e);
            }
        });

        this.element.addEventListener('click', (e) => {
            const targetSelector = e.target.closest('.target-selector');
            if (targetSelector && !e.target.matches('input')) {
                const input = targetSelector.querySelector('input');
                if (input) {
                    input.checked = !input.checked;
                    this.handleSelectionChange({ target: input });
                }
            }
        });
    }

    handleSelectionChange(event) {
        const input = event.target;
        const targetSelector = input.closest('.target-selector');
        const targetId = targetSelector.dataset.targetId;

        if (input.type === 'radio') {
            // Clear all selections
            this.element.querySelectorAll('.target-selector').forEach(el => {
                el.classList.remove('active');
            });
            this.selectedTargets = [];

            if (input.checked) {
                targetSelector.classList.add('active');
                this.selectedTargets = [targetId];
            }
        } else {
            // Checkbox handling
            if (input.checked) {
                targetSelector.classList.add('active');
                if (!this.selectedTargets.includes(targetId)) {
                    this.selectedTargets.push(targetId);
                }
            } else {
                targetSelector.classList.remove('active');
                this.selectedTargets = this.selectedTargets.filter(id => id !== targetId);
            }
        }

        if (this.options.onSelectionChange) {
            this.options.onSelectionChange(this.selectedTargets);
        }
    }

    getSelectedTargets() {
        return this.selectedTargets;
    }

    clearSelection() {
        this.selectedTargets = [];
        this.element.querySelectorAll('.target-selector').forEach(el => {
            el.classList.remove('active');
            const input = el.querySelector('input');
            if (input) input.checked = false;
        });
    }
}

// Auto-refresh Component
class AutoRefresh {
    constructor(callback, interval = 5000) {
        this.callback = callback;
        this.interval = interval;
        this.timer = null;
        this.isRunning = false;
    }

    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        this.timer = setInterval(() => {
            if (!document.hidden) {
                this.callback();
            }
        }, this.interval);
    }

    stop() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        this.isRunning = false;
    }

    setInterval(newInterval) {
        this.interval = newInterval;
        if (this.isRunning) {
            this.stop();
            this.start();
        }
    }

    destroy() {
        this.stop();
    }
}

// Export components
window.Components = {
    FileUploader,
    ScriptEditor,
    LogViewer,
    ProgressBar,
    TargetSelector,
    AutoRefresh
};