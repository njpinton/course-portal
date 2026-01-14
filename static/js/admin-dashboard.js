/**
 * Admin Dashboard JavaScript Module
 * Handles statistics, stage completion, and submissions display
 */

const AdminDashboard = {
    // Configuration
    config: {
        apiEndpoint: '/api/admin/statistics',
        refreshInterval: 300000 // 5 minutes
    },

    // State
    state: {
        refreshTimer: null
    },

    /**
     * Display an alert message
     */
    showAlert(message, type = 'info') {
        const alertsContainer = document.getElementById('alertsContainer');
        const alert = document.createElement('div');
        alert.className = `alert ${type}`;

        const iconMap = {
            'success': '✓',
            'error': '✕',
            'info': 'ℹ',
            'warning': '⚠'
        };

        alert.innerHTML = `
            <span class="alert-icon">${iconMap[type] || 'ℹ'}</span>
            <span>${message}</span>
            <span class="alert-close" onclick="this.parentElement.remove()">✕</span>
        `;

        alertsContainer.appendChild(alert);

        if (type !== 'error') {
            setTimeout(() => alert.remove(), 5000);
        }
    },

    /**
     * Set card loading state
     */
    setCardLoading(cardId, isLoading) {
        const card = document.getElementById(cardId);
        if (isLoading) {
            card.classList.add('loading');
        } else {
            card.classList.remove('loading');
        }
    },

    /**
     * Format date to readable string
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    /**
     * Update statistics cards
     */
    updateStatistics(data) {
        try {
            const totalGroupsCard = document.getElementById('totalGroupsCard');
            totalGroupsCard.innerHTML = `
                <div class="stat-icon">📊</div>
                <div class="stat-label">Total Groups</div>
                <div class="stat-value">${data.total_groups || 0}</div>
                <div class="stat-subtext">Active groups</div>
            `;
            this.setCardLoading('totalGroupsCard', false);

            const totalSubmissionsCard = document.getElementById('totalSubmissionsCard');
            totalSubmissionsCard.innerHTML = `
                <div class="stat-icon">📝</div>
                <div class="stat-label">Total Submissions</div>
                <div class="stat-value">${data.total_submissions || 0}</div>
                <div class="stat-subtext">All stages combined</div>
            `;
            this.setCardLoading('totalSubmissionsCard', false);

            const avgSubmissionsCard = document.getElementById('avgSubmissionsCard');
            const avgValue = data.total_groups > 0
                ? (data.total_submissions / data.total_groups).toFixed(1)
                : 0;
            avgSubmissionsCard.innerHTML = `
                <div class="stat-icon">📈</div>
                <div class="stat-label">Avg Submissions per Group</div>
                <div class="stat-value">${avgValue}</div>
                <div class="stat-subtext">Average across all groups</div>
            `;
            this.setCardLoading('avgSubmissionsCard', false);
        } catch (error) {
            console.error('Error updating statistics:', error);
            this.showAlert('Failed to update statistics: ' + error.message, 'error');
        }
    },

    /**
     * Update stage completion bars
     */
    updateStages(stages) {
        try {
            const stagesContainer = document.getElementById('stagesContainer');

            if (!stages || stages.length === 0) {
                stagesContainer.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">📭</div>
                        <div class="empty-state-text">No stage data available</div>
                    </div>
                `;
                return;
            }

            let html = '';
            stages.forEach((stage) => {
                const percentage = stage.total_submissions > 0
                    ? Math.round((stage.completed_submissions / stage.total_submissions) * 100)
                    : 0;

                html += `
                    <div class="stage-item">
                        <div class="stage-header">
                            <span class="stage-name">Stage ${stage.stage_number}: ${stage.stage_name}</span>
                            <span class="stage-percentage">${percentage}%</span>
                        </div>
                        <div class="progress-bar-container">
                            <div class="progress-bar" style="width: ${percentage}%">
                                ${percentage > 10 ? percentage + '%' : ''}
                            </div>
                        </div>
                        <div style="margin-top: 8px; font-size: 0.9em; color: #999;">
                            ${stage.completed_submissions} of ${stage.total_submissions} groups completed
                        </div>
                    </div>
                `;
            });

            stagesContainer.innerHTML = html;
        } catch (error) {
            console.error('Error updating stages:', error);
            this.showAlert('Failed to update stage data: ' + error.message, 'error');
        }
    },

    /**
     * Update recent submissions table
     */
    updateSubmissions(submissions) {
        try {
            const tableBody = document.getElementById('submissionsTableBody');
            const countSpan = document.getElementById('submissionsCount');

            if (!submissions || submissions.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="4">
                            <div class="empty-state">
                                <div class="empty-state-icon">📭</div>
                                <div class="empty-state-text">No submissions found</div>
                            </div>
                        </td>
                    </tr>
                `;
                countSpan.textContent = 'No submissions';
                return;
            }

            let html = '';
            submissions.forEach(submission => {
                const groupName = submission.group_name || submission.groups?.group_name || 'Unknown';
                const groupId = submission.group_id;
                const projectTitle = submission.project_title || submission.groups?.project_title || 'N/A';
                html += `
                    <tr>
                        <td class="group-name-cell"><a href="/admin/group/${groupId}" class="group-name-link">${groupName}</a></td>
                        <td>${projectTitle}</td>
                        <td class="stage-cell">Stage ${submission.stage_number}</td>
                        <td class="date-cell">${this.formatDate(submission.submitted_at)}</td>
                    </tr>
                `;
            });

            tableBody.innerHTML = html;
            countSpan.textContent = `${submissions.length} submission(s)`;
            this.initializeTableSorting('submissionsTable');
        } catch (error) {
            console.error('Error updating submissions:', error);
            this.showAlert('Failed to update submissions: ' + error.message, 'error');
        }
    },

    /**
     * Fetch filtered submissions
     */
    async fetchFilteredSubmissions(stageNumber = null) {
        try {
            let url = '/api/admin/submissions?sort=submitted_at';
            if (stageNumber) {
                url += `&stage_number=${stageNumber}`;
            }

            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`API returned status ${response.status}`);
            }

            const data = await response.json();
            const submissions = Array.isArray(data) ? data : (data.submissions || data.data || []);
            this.updateSubmissions(submissions);
        } catch (error) {
            console.error('Error fetching filtered submissions:', error);
            this.showAlert('Failed to load submissions: ' + error.message, 'error');
        }
    },

    /**
     * Initialize table sorting functionality
     */
    initializeTableSorting(tableId) {
        const table = document.getElementById(tableId);
        if (!table) return;

        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            if (index < headers.length - 1 || tableId === 'submissionsTable') {
                header.classList.add('sortable');
                header.addEventListener('click', () => this.sortTable(tableId, index));
            }
        });
    },

    /**
     * Sort table by column
     */
    sortTable(tableId, columnIndex) {
        const table = document.getElementById(tableId);
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const header = table.querySelectorAll('th')[columnIndex];
        const headerText = header.textContent.trim().toLowerCase();

        let isAscending = !header.classList.contains('sort-asc');

        table.querySelectorAll('th').forEach(th => {
            th.classList.remove('sort-asc', 'sort-desc');
        });

        header.classList.add(isAscending ? 'sort-asc' : 'sort-desc');

        rows.sort((a, b) => {
            let aVal = a.querySelectorAll('td')[columnIndex].textContent.trim();
            let bVal = b.querySelectorAll('td')[columnIndex].textContent.trim();

            if (headerText.includes('submitted')) {
                const aDate = new Date(aVal);
                const bDate = new Date(bVal);
                if (!isNaN(aDate.getTime()) && !isNaN(bDate.getTime())) {
                    return isAscending ? aDate - bDate : bDate - aDate;
                }
            }

            const aNum = parseFloat(aVal);
            const bNum = parseFloat(bVal);
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return isAscending ? aNum - bNum : bNum - aNum;
            }

            return isAscending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        });

        rows.forEach(row => tbody.appendChild(row));
    },

    /**
     * Setup filter controls
     */
    setupFilterControls() {
        const applyBtn = document.getElementById('applyFilterBtn');
        const resetBtn = document.getElementById('resetFilterBtn');
        const stageFilter = document.getElementById('stageFilter');

        if (applyBtn) {
            applyBtn.addEventListener('click', () => {
                this.fetchFilteredSubmissions(stageFilter.value || null);
            });
        }

        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                stageFilter.value = '';
                this.fetchFilteredSubmissions(null);
            });
        }

        if (stageFilter) {
            stageFilter.addEventListener('change', () => {
                this.fetchFilteredSubmissions(stageFilter.value || null);
            });
        }
    },

    /**
     * Fetch all dashboard data
     */
    async fetchDashboardData() {
        try {
            const response = await fetch(this.config.apiEndpoint);
            if (!response.ok) {
                throw new Error(`API returned status ${response.status}`);
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            this.updateStatistics(data);
            this.updateStages(data.stages || []);
            this.updateSubmissions(data.recent_submissions || []);

            console.log('Dashboard data refreshed successfully');
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            this.showAlert('Failed to load dashboard data: ' + error.message, 'error');
        }
    },

    /**
     * Start auto-refresh timer
     */
    startAutoRefresh() {
        if (this.state.refreshTimer) {
            clearInterval(this.state.refreshTimer);
        }

        this.state.refreshTimer = setInterval(() => {
            console.log('Auto-refreshing dashboard data...');
            this.fetchDashboardData();
        }, this.config.refreshInterval);
    },

    /**
     * Load groups submission status table
     */
    async loadGroupsSubmissionStatus() {
        try {
            const response = await fetch('/api/admin/groups/submission-status');
            if (!response.ok) {
                throw new Error(`API returned status ${response.status}`);
            }

            const groups = await response.json();
            const tbody = document.getElementById('groupsStatusTableBody');

            if (!groups || groups.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="9" style="text-align: center; padding: 40px 20px; color: #999;">
                            No groups found
                        </td>
                    </tr>
                `;
                return;
            }

            tbody.innerHTML = '';

            groups.forEach(group => {
                const row = document.createElement('tr');
                let stageCells = '';
                for (let i = 1; i <= 6; i++) {
                    const isSubmitted = group.stages[`stage_${i}`];
                    stageCells += `<td class="${isSubmitted ? 'submitted' : ''}">${isSubmitted ? '✓' : ''}</td>`;
                }

                row.innerHTML = `
                    <td>${group.group_name}</td>
                    <td>${group.project_title}</td>
                    ${stageCells}
                    <td>
                        <button class="btn-delete" data-group-id="${group.id}" data-group-name="${group.group_name}">Delete</button>
                    </td>
                `;
                tbody.appendChild(row);
            });

            console.log(`Loaded submission status for ${groups.length} groups`);
        } catch (error) {
            console.error('Error loading groups submission status:', error);
            document.getElementById('groupsStatusTableBody').innerHTML = `
                <tr>
                    <td colspan="9" style="text-align: center; padding: 40px 20px; color: #dc3545;">
                        Error loading groups. Please try again.
                    </td>
                </tr>
            `;
            this.showAlert('Failed to load groups submission status: ' + error.message, 'error');
        }
    },

    /**
     * Delete a group
     */
    async deleteGroup(groupId, groupName) {
        if (!confirm(`Are you sure you want to delete the group "${groupName}"?\n\nThis will permanently delete:\n- The group and all its data\n- All group members\n- All submissions\n- All documents\n\nThis action cannot be undone!`)) {
            return;
        }

        try {
            const response = await fetch(`/api/groups/${groupId}`, { method: 'DELETE' });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to delete group');
            }

            this.showAlert(`Group "${groupName}" deleted successfully`, 'success');
            await this.loadGroupsSubmissionStatus();
            await this.fetchDashboardData();
        } catch (error) {
            console.error('Error deleting group:', error);
            this.showAlert('Failed to delete group: ' + error.message, 'error');
        }
    },

    /**
     * Open feedback form
     */
    openFeedbackForm() {
        const feedback = prompt(
            'Please share your feedback or report an issue:\n\n(Your message will help us improve the application)',
            ''
        );
        if (feedback && feedback.trim()) {
            alert('Thank you for your feedback! We appreciate your input.');
            console.log('Feedback:', feedback);
        }
    },

    /**
     * Initialize dashboard
     */
    async init() {
        try {
            console.log('Initializing admin dashboard...');

            this.setupFilterControls();
            await this.fetchDashboardData();
            await this.loadGroupsSubmissionStatus();
            await this.fetchFilteredSubmissions(1);
            this.startAutoRefresh();

            // Event delegation for delete buttons
            const groupsTable = document.getElementById('groupsStatusTableBody');
            if (groupsTable) {
                groupsTable.addEventListener('click', (e) => {
                    if (e.target.classList.contains('btn-delete')) {
                        this.deleteGroup(
                            e.target.getAttribute('data-group-id'),
                            e.target.getAttribute('data-group-name')
                        );
                    }
                });
            }

            console.log('Admin dashboard initialized successfully');
        } catch (error) {
            console.error('Failed to initialize dashboard:', error);
            this.showAlert('Failed to initialize dashboard: ' + error.message, 'error');
        }
    },

    /**
     * Cleanup
     */
    cleanup() {
        if (this.state.refreshTimer) {
            clearInterval(this.state.refreshTimer);
            this.state.refreshTimer = null;
        }
    }
};

// Event listeners
document.addEventListener('DOMContentLoaded', () => AdminDashboard.init());

window.addEventListener('beforeunload', () => AdminDashboard.cleanup());

document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        AdminDashboard.cleanup();
    } else {
        AdminDashboard.fetchDashboardData();
        AdminDashboard.startAutoRefresh();
    }
});

// Global functions for onclick handlers
window.refreshDashboard = () => AdminDashboard.fetchDashboardData();
window.openFeedbackForm = () => AdminDashboard.openFeedbackForm();
