// Instagram Audience Analysis Frontend
const API_BASE_URL = 'https://instagram-api.teabag.online/api/v1';

class InstagramApp {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkAPIHealth();
    }

    bindEvents() {
        const form = document.getElementById('addAccountForm');
        form.addEventListener('submit', this.handleAddAccount.bind(this));
    }

    async checkAPIHealth() {
        try {
            const response = await fetch('https://instagram-api.teabag.online/health');
            if (response.ok) {
                console.log('API is healthy');
            }
        } catch (error) {
            console.warn('API health check failed:', error);
        }
    }

    async handleAddAccount(e) {
        e.preventDefault();
        
        const usernameInput = document.getElementById('username');
        const username = usernameInput.value.trim().replace('@', '');
        
        if (!username) return;

        const messageDiv = document.getElementById('message');
        const messageParagraph = messageDiv.querySelector('p');
        
        try {
            this.showMessage('🔄 Starting analysis...', 'info');
            
            const response = await fetch(`${API_BASE_URL}/accounts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username }),
            });

            const data = await response.json();

            if (response.ok) {
                this.showMessage(`✅ Analysis started for @${username}`, 'success');
                usernameInput.value = '';
                
                // Show demographics section
                document.getElementById('demographics').classList.remove('hidden');
                this.loadDemoData();
            } else {
                this.showMessage(`❌ Error: ${data.detail || 'Failed to add account'}`, 'error');
            }
        } catch (error) {
            this.showMessage('❌ Network error. Please check if the API is running.', 'error');
        }
    }

    showMessage(text, type) {
        const messageDiv = document.getElementById('message');
        const messageParagraph = messageDiv.querySelector('p');
        
        messageParagraph.textContent = text;
        messageDiv.classList.remove('hidden');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageDiv.classList.add('hidden');
        }, 5000);
    }

    loadDemoData() {
        // Gender Distribution Chart
        const genderCtx = document.getElementById('genderChart').getContext('2d');
        new Chart(genderCtx, {
            type: 'doughnut',
            data: {
                labels: ['Female', 'Male'],
                datasets: [{
                    data: [55, 45],
                    backgroundColor: ['#8B5CF6', '#06B6D4'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Age Distribution Chart
        const ageCtx = document.getElementById('ageChart').getContext('2d');
        new Chart(ageCtx, {
            type: 'doughnut',
            data: {
                labels: ['18-24', '25-34', '35-44', '45+'],
                datasets: [{
                    data: [30, 40, 20, 10],
                    backgroundColor: ['#10B981', '#F59E0B', '#EF4444', '#6B7280'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    async loadRealDemographics(username) {
        try {
            const response = await fetch(`${API_BASE_URL}/accounts/${username}/demographics`);
            const data = await response.json();
            
            if (response.ok) {
                this.updateCharts(data);
            }
        } catch (error) {
            console.warn('Failed to load real demographics:', error);
        }
    }

    updateCharts(data) {
        // Update charts with real data when available
        console.log('Demographics data:', data);
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    new InstagramApp();
});