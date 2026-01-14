/**
 * Group Portal JavaScript
 * Handles group creation, member management, and group display
 */

// Application State
const state = {
    isAdmin: false,
    currentView: 'kanban',
    groups: [],
    availableStudents: [],
    selectedMembers: [],
    selectedGroupId: null
};

// DOM Elements (initialized on DOMContentLoaded)
let elements = {};

// Initialize state from server data
function initState(isAdmin) {
    state.isAdmin = isAdmin;
}

// Initialize DOM elements
function initElements() {
    elements = {
        createGroupForm: document.getElementById('createGroupForm'),
        createGroupSection: document.getElementById('createGroupSection'),
        showCreateGroupBtn: document.getElementById('showCreateGroupBtn'),
        groupsList: document.getElementById('groupsList'),
        groupSearch: document.getElementById('groupSearch'),
        studentSearch: document.getElementById('studentSearch'),
        studentsList: document.getElementById('studentsList'),
        selectedMembers: document.getElementById('selectedMembers'),
        classAlert: document.getElementById('classAlert'),
        classAlertText: document.getElementById('classAlertText'),
        modal: document.getElementById('groupDetailsModal'),
        modalTitle: document.getElementById('modalGroupName'),
        modalContent: document.getElementById('modalContent'),
        modalClose: document.querySelector('.modal-close'),
        viewKanban: document.getElementById('viewKanban'),
        viewList: document.getElementById('viewList'),
        toastContainer: document.getElementById('toastContainer')
    };
}

// Toast Notification System
function showToast(message, type = 'info', title = '') {
    const icons = { success: '&#10004;', error: '&#10006;', warning: '&#9888;', info: '&#8505;' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span class="toast-icon" aria-hidden="true">${icons[type]}</span>
        <div class="toast-content">
            ${title ? `<div class="toast-title">${title}</div>` : ''}
            <div class="toast-message">${message}</div>
        </div>
        <button type="button" class="toast-close" aria-label="Dismiss notification"><span aria-hidden="true">&times;</span></button>
    `;
    elements.toastContainer.appendChild(toast);
    const timeout = setTimeout(() => removeToast(toast), 5000);
    toast.querySelector('.toast-close').addEventListener('click', () => {
        clearTimeout(timeout);
        removeToast(toast);
    });
}

function removeToast(toast) {
    toast.style.animation = 'toastSlideIn 0.3s ease-out reverse';
    setTimeout(() => toast.remove(), 300);
}

// Toggle Create Group Form
function setupCreateGroupToggle() {
    elements.showCreateGroupBtn.addEventListener('click', () => {
        const isHidden = elements.createGroupSection.classList.contains('hidden');
        elements.createGroupSection.classList.toggle('hidden');
        elements.showCreateGroupBtn.setAttribute('aria-expanded', isHidden);
        elements.showCreateGroupBtn.innerHTML = isHidden
            ? '<span aria-hidden="true">&minus;</span> Hide Form'
            : '<span aria-hidden="true">+</span> Create New Group';
        if (isHidden) {
            elements.createGroupSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            document.getElementById('groupName').focus();
        }
    });
}

// Student Search Functions
async function loadStudents() {
    try {
        const response = await fetch('/api/students/ungrouped/all');
        if (!response.ok) throw new Error('Failed to fetch students');
        state.availableStudents = await response.json();
        if (state.availableStudents.length > 0) {
            elements.classAlert.classList.remove('hidden');
            elements.classAlertText.textContent = `${state.availableStudents.length} ungrouped students available`;
        } else {
            elements.classAlert.classList.remove('hidden');
            elements.classAlertText.textContent = 'No ungrouped students available';
        }
    } catch (error) {
        console.error('Error loading students:', error);
        showToast('Failed to load students', 'error');
    }
}

function filterStudents(searchTerm) {
    const dropdown = elements.studentsList;
    dropdown.innerHTML = '';
    const term = searchTerm.toLowerCase();
    const filtered = state.availableStudents.filter(student => {
        if (!term) return true;
        const fullName = `${student.first_name || ''} ${student.last_name || ''}`.toLowerCase();
        const campusId = (student.campus_id || '').toLowerCase();
        return fullName.includes(term) || campusId.includes(term);
    });

    if (filtered.length === 0) {
        dropdown.innerHTML = '<li class="search-dropdown-empty" style="padding: 16px; text-align: center; color: var(--text-muted);">No students found</li>';
        dropdown.classList.add('active');
        return;
    }

    filtered.slice(0, 20).forEach(student => {
        const fullName = `${student.first_name || ''} ${student.last_name || ''}`.trim() || 'Unnamed';
        const isSelected = state.selectedMembers.some(m => m.studentId === student.id);
        const li = document.createElement('li');
        li.className = 'search-dropdown-item';
        li.setAttribute('role', 'option');
        li.setAttribute('tabindex', '0');
        if (isSelected) li.style.opacity = '0.5';
        li.innerHTML = `
            <div class="search-dropdown-item-name">${fullName}</div>
            <div class="search-dropdown-item-meta">${student.campus_id || 'No ID'} - ${student.program || 'N/A'}</div>
        `;
        li.addEventListener('click', () => addMember(student, fullName));
        li.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                addMember(student, fullName);
            }
        });
        dropdown.appendChild(li);
    });
    dropdown.classList.add('active');
    elements.studentSearch.setAttribute('aria-expanded', 'true');
}

function addMember(student, fullName) {
    if (state.selectedMembers.some(m => m.studentId === student.id)) {
        showToast(`${fullName} is already in the group`, 'warning');
        return;
    }
    state.selectedMembers.push({ studentId: student.id, name: fullName, campusId: student.campus_id });
    renderMembers();
    elements.studentSearch.value = '';
    elements.studentsList.classList.remove('active');
    elements.studentSearch.setAttribute('aria-expanded', 'false');
    showToast(`${fullName} added to group`, 'success');
}

function renderMembers() {
    const container = elements.selectedMembers;
    if (state.selectedMembers.length === 0) {
        container.innerHTML = '<p class="members-empty">No members added yet. Search above to add students.</p>';
        container.classList.remove('has-members');
        return;
    }
    container.classList.add('has-members');
    container.innerHTML = '<div class="members-grid"></div>';
    const grid = container.querySelector('.members-grid');
    state.selectedMembers.forEach((member, index) => {
        const card = document.createElement('div');
        card.className = 'member-card';
        card.innerHTML = `
            <div class="member-info">
                <div class="member-name">${member.name}</div>
                <div class="member-id">${member.campusId || 'No ID'}</div>
            </div>
            <button type="button" class="member-remove" aria-label="Remove ${member.name}">
                <span aria-hidden="true">&times;</span>
            </button>
        `;
        card.querySelector('.member-remove').addEventListener('click', () => {
            state.selectedMembers.splice(index, 1);
            renderMembers();
            showToast(`${member.name} removed`, 'info');
        });
        grid.appendChild(card);
    });
}

function setupStudentSearch() {
    elements.studentSearch.addEventListener('focus', () => {
        if (state.availableStudents.length > 0) filterStudents(elements.studentSearch.value);
    });
    elements.studentSearch.addEventListener('input', (e) => {
        if (state.availableStudents.length > 0) filterStudents(e.target.value);
    });
    document.addEventListener('click', (e) => {
        if (!elements.studentSearch.contains(e.target) && !elements.studentsList.contains(e.target)) {
            elements.studentsList.classList.remove('active');
            elements.studentSearch.setAttribute('aria-expanded', 'false');
        }
    });
}

// Groups Display Functions
async function loadGroups() {
    try {
        const response = await fetch('/api/groups');
        const groups = await response.json();
        if (groups.error) {
            elements.groupsList.innerHTML = `<div class="alert alert-error">${groups.error}</div>`;
            return;
        }
        state.groups = groups;
        renderGroups();
    } catch (error) {
        elements.groupsList.innerHTML = `<div class="alert alert-error">Failed to load groups</div>`;
        console.error('Error fetching groups:', error);
    }
}

function renderGroups() {
    const { groups, currentView } = state;
    if (groups.length === 0) {
        elements.groupsList.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">&#128203;</div>
                <div class="empty-state-title">No groups yet</div>
                <p>Create the first group to get started!</p>
            </div>`;
        return;
    }
    if (currentView === 'kanban') {
        renderCardView(groups);
    } else {
        renderTableView(groups);
    }
    attachViewDetailsHandlers();
}

function renderCardView(groups) {
    const html = groups.map(group => {
        const memberCount = group.group_members?.length || 0;
        const memberNames = group.group_members?.map(m => m.member_name?.split(' ')[0]).filter(Boolean).join(', ') || 'No members';
        return `
            <article class="group-card">
                <h3 class="group-card-title">${escapeHtml(group.group_name)}</h3>
                <p class="group-card-meta"><strong>Project:</strong> ${escapeHtml(group.project_title || 'N/A')}</p>
                <p class="group-card-meta"><strong>Members:</strong> ${memberCount}</p>
                ${memberCount > 0 ? `
                    <div class="group-card-team">
                        <div style="font-weight: 600; font-size: 0.9em; margin-bottom: 4px;">&#128101; Team</div>
                        <div style="font-size: 0.9em; color: var(--text-secondary);">${escapeHtml(memberNames)}</div>
                    </div>
                ` : ''}
                <p class="group-card-meta"><strong>Created:</strong> ${formatDate(group.created_at)}</p>
                <button type="button" class="btn btn-primary btn-sm view-details-btn mt-4" data-group-id="${group.id}">View Details</button>
            </article>`;
    }).join('');
    elements.groupsList.innerHTML = `<div class="groups-grid">${html}</div>`;
}

function renderTableView(groups) {
    const rows = groups.map(group => {
        const memberNames = group.group_members?.map(m => {
            if (m.last_name) return m.last_name;
            if (m.member_name) {
                const parts = m.member_name.trim().split(' ');
                return parts.length > 1 ? parts[parts.length - 1] : m.member_name;
            }
            return null;
        }).filter(Boolean).join(', ') || '';
        return `
            <tr>
                <td>
                    <div class="group-name">${escapeHtml(group.group_name)}</div>
                    ${memberNames ? `<div class="group-members-list">${escapeHtml(memberNames)}</div>` : ''}
                </td>
                <td>${escapeHtml(group.project_title || 'Not specified')}</td>
                <td>${formatDate(group.created_at)}</td>
                <td><button type="button" class="btn btn-primary btn-sm view-details-btn" data-group-id="${group.id}">View Details</button></td>
            </tr>`;
    }).join('');
    elements.groupsList.innerHTML = `
        <table class="table groups-table">
            <thead><tr><th scope="col">Group Name</th><th scope="col">Project Title</th><th scope="col">Created</th><th scope="col">Actions</th></tr></thead>
            <tbody>${rows}</tbody>
        </table>`;
}

function attachViewDetailsHandlers() {
    document.querySelectorAll('.view-details-btn').forEach(btn => {
        btn.addEventListener('click', () => showGroupDetails(btn.dataset.groupId));
    });
}

// View Toggle
function setupViewToggle() {
    elements.viewKanban.addEventListener('click', () => {
        state.currentView = 'kanban';
        elements.viewKanban.classList.add('active');
        elements.viewKanban.setAttribute('aria-selected', 'true');
        elements.viewList.classList.remove('active');
        elements.viewList.setAttribute('aria-selected', 'false');
        renderGroups();
    });
    elements.viewList.addEventListener('click', () => {
        state.currentView = 'list';
        elements.viewList.classList.add('active');
        elements.viewList.setAttribute('aria-selected', 'true');
        elements.viewKanban.classList.remove('active');
        elements.viewKanban.setAttribute('aria-selected', 'false');
        renderGroups();
    });
}

// Group Search Filter
function setupGroupSearch() {
    elements.groupSearch.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase().trim();
        if (!searchTerm) {
            renderGroups();
            return;
        }
        const filteredGroups = state.groups.filter(group => {
            const groupName = (group.group_name || '').toLowerCase();
            const projectTitle = (group.project_title || '').toLowerCase();
            const memberNames = group.group_members?.map(m => (m.member_name || '').toLowerCase()).join(' ') || '';
            return groupName.includes(searchTerm) || projectTitle.includes(searchTerm) || memberNames.includes(searchTerm);
        });
        if (state.currentView === 'kanban') {
            renderCardView(filteredGroups);
        } else {
            renderTableView(filteredGroups);
        }
        attachViewDetailsHandlers();
    });
}

// Modal Functions
async function showGroupDetails(groupId) {
    openModal();
    elements.modalContent.innerHTML = `<div class="loading-state"><div class="spinner"></div><p>Loading group details...</p></div>`;
    try {
        const response = await fetch(`/api/groups/${groupId}`);
        const group = await response.json();
        if (group.error) {
            elements.modalContent.innerHTML = `<div class="alert alert-error">${group.error}</div>`;
            return;
        }
        elements.modalTitle.textContent = group.group_name;
        let summaryHtml = '<p style="color: var(--text-muted);">No summary submitted yet.</p>';
        if (group.submissions?.length > 0) {
            const latest = group.submissions.sort((a, b) => b.stage_number - a.stage_number)[0];
            if (latest.summary_markdown) {
                const summaryText = latest.summary_markdown.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                summaryHtml = `
                    <div style="background: var(--bg-main); padding: 20px; border-radius: var(--radius); border-left: 4px solid var(--up-green);">
                        <h4 style="margin: 0 0 12px 0; color: var(--text-muted); font-size: 0.9em; text-transform: uppercase;">
                            Latest Summary (Stage ${latest.stage_number})
                        </h4>
                        <div style="line-height: 1.6;">${summaryText}</div>
                        ${latest.presentation_link ? `
                            <p style="margin-top: 16px;">
                                <a href="${escapeHtml(latest.presentation_link)}" target="_blank" rel="noopener" style="color: var(--up-green); font-weight: 600;">
                                    &#128279; View Presentation
                                </a>
                            </p>
                        ` : ''}
                    </div>`;
            }
        }
        elements.modalContent.innerHTML = `
            <p style="font-size: 1.1em; margin-bottom: 20px;"><strong>Project:</strong> ${escapeHtml(group.project_title || 'N/A')}</p>
            <h3 style="color: var(--up-green); margin-bottom: 16px;">Project Summary</h3>
            ${summaryHtml}`;
    } catch (error) {
        elements.modalContent.innerHTML = `<div class="alert alert-error">Failed to load group details</div>`;
        console.error('Error fetching group details:', error);
    }
}

function openModal() {
    elements.modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    elements.modalClose.focus();
}

function closeModal() {
    elements.modal.classList.remove('active');
    document.body.style.overflow = '';
}

function setupModal() {
    elements.modalClose.addEventListener('click', closeModal);
    elements.modal.addEventListener('click', (e) => {
        if (e.target === elements.modal) closeModal();
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && elements.modal.classList.contains('active')) closeModal();
    });
}

// Form Submission
function setupFormSubmission() {
    elements.createGroupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(elements.createGroupForm);
        const groupName = formData.get('group_name')?.trim();
        const projectTitle = formData.get('project_title')?.trim();
        const username = formData.get('username')?.trim();
        const password = formData.get('password');

        if (!groupName) {
            showToast('Group Name is required', 'error');
            document.getElementById('groupName').focus();
            return;
        }
        if (!username) {
            showToast('Username is required', 'error');
            document.getElementById('groupUsername').focus();
            return;
        }
        if (!password || password.length < 6) {
            showToast('Password must be at least 6 characters', 'error');
            document.getElementById('groupPassword').focus();
            return;
        }

        const submitBtn = elements.createGroupForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Creating...';

        try {
            const response = await fetch('/api/groups', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    group_name: groupName,
                    project_title: projectTitle,
                    username: username,
                    password: password,
                    members: state.selectedMembers.map(m => m.studentId)
                })
            });
            const result = await response.json();
            if (result.error) {
                showToast(result.error, 'error', 'Error');
            } else {
                showToast('Group created successfully!', 'success');
                elements.createGroupForm.reset();
                state.selectedMembers = [];
                renderMembers();
                loadGroups();
                loadStudents();
                elements.createGroupSection.classList.add('hidden');
                elements.showCreateGroupBtn.setAttribute('aria-expanded', 'false');
                elements.showCreateGroupBtn.innerHTML = '<span aria-hidden="true">+</span> Create New Group';
            }
        } catch (error) {
            showToast('Failed to create group', 'error');
            console.error('Error creating group:', error);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Utility Functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString();
}

// Initialize Application
function initGroupPortal(isAdmin = false) {
    initState(isAdmin);
    initElements();
    setupCreateGroupToggle();
    setupStudentSearch();
    setupViewToggle();
    setupGroupSearch();
    setupModal();
    setupFormSubmission();
    loadGroups();
    loadStudents();
}

// Auto-initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if page has group portal elements
    if (document.getElementById('createGroupForm')) {
        const isAdmin = window.groupPortalConfig?.isAdmin || false;
        initGroupPortal(isAdmin);
    }
});
