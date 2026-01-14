/**
 * Admin Resources Management
 * Handles CRUD operations for course resources (YouTube videos, links, PDFs)
 */

const ResourcesManager = {
    currentCourseId: null,
    resources: [],
    editingId: null,

    /**
     * Initialize the resources manager
     */
    init() {
        this.bindElements();
        this.bindEvents();
        this.loadInitialCourse();
    },

    /**
     * Cache DOM elements
     */
    bindElements() {
        this.elements = {
            courseSelect: document.getElementById('courseSelect'),
            resourcesList: document.getElementById('resourcesList'),
            resourceCount: document.getElementById('resourceCount'),
            addResourceBtn: document.getElementById('addResourceBtn'),
            // Modal elements
            resourceModal: document.getElementById('resourceModal'),
            resourceForm: document.getElementById('resourceForm'),
            modalTitle: document.getElementById('modalTitle'),
            closeModalBtn: document.getElementById('closeModalBtn'),
            cancelBtn: document.getElementById('cancelBtn'),
            saveBtn: document.getElementById('saveBtn'),
            // Form fields
            resourceId: document.getElementById('resourceId'),
            resourceType: document.getElementById('resourceType'),
            resourceTitle: document.getElementById('resourceTitle'),
            resourceDescription: document.getElementById('resourceDescription'),
            youtubeUrl: document.getElementById('youtubeUrl'),
            externalUrl: document.getElementById('externalUrl'),
            resourceActive: document.getElementById('resourceActive'),
            // Type-specific field containers
            youtubeFields: document.getElementById('youtubeFields'),
            linkFields: document.getElementById('linkFields'),
            // Video preview
            videoPreview: document.getElementById('videoPreview'),
            videoThumbnail: document.getElementById('videoThumbnail'),
            videoIdDisplay: document.getElementById('videoIdDisplay'),
            // Delete modal
            deleteModal: document.getElementById('deleteModal'),
            deleteResourceTitle: document.getElementById('deleteResourceTitle'),
            confirmDeleteBtn: document.getElementById('confirmDeleteBtn'),
            cancelDeleteBtn: document.getElementById('cancelDeleteBtn'),
            closeDeleteModalBtn: document.getElementById('closeDeleteModalBtn')
        };
    },

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Course selector
        this.elements.courseSelect.addEventListener('change', () => this.handleCourseChange());

        // Add resource button
        this.elements.addResourceBtn.addEventListener('click', () => this.openAddModal());

        // Modal controls
        this.elements.closeModalBtn.addEventListener('click', () => this.closeModal());
        this.elements.cancelBtn.addEventListener('click', () => this.closeModal());
        this.elements.resourceModal.addEventListener('click', (e) => {
            if (e.target === this.elements.resourceModal) this.closeModal();
        });

        // Form submission
        this.elements.resourceForm.addEventListener('submit', (e) => this.handleSubmit(e));

        // Resource type change
        this.elements.resourceType.addEventListener('change', () => this.handleTypeChange());

        // YouTube URL input - extract video ID
        this.elements.youtubeUrl.addEventListener('input', () => this.handleYoutubeUrlInput());

        // Delete modal controls
        this.elements.closeDeleteModalBtn.addEventListener('click', () => this.closeDeleteModal());
        this.elements.cancelDeleteBtn.addEventListener('click', () => this.closeDeleteModal());
        this.elements.confirmDeleteBtn.addEventListener('click', () => this.confirmDelete());
        this.elements.deleteModal.addEventListener('click', (e) => {
            if (e.target === this.elements.deleteModal) this.closeDeleteModal();
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (this.elements.resourceModal.classList.contains('active')) {
                    this.closeModal();
                }
                if (this.elements.deleteModal.classList.contains('active')) {
                    this.closeDeleteModal();
                }
            }
        });
    },

    /**
     * Load initial course resources
     */
    loadInitialCourse() {
        const courseId = this.elements.courseSelect.value;
        if (courseId) {
            this.currentCourseId = courseId;
            this.loadResources(courseId);
        }
    },

    /**
     * Handle course selection change
     */
    handleCourseChange() {
        const courseId = this.elements.courseSelect.value;
        this.currentCourseId = courseId;
        this.loadResources(courseId);
    },

    /**
     * Load resources for a course
     */
    async loadResources(courseId) {
        this.elements.resourcesList.innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <p>Loading resources...</p>
            </div>
        `;

        try {
            const response = await fetch(`/api/admin/resources?course_id=${courseId}`);
            if (!response.ok) throw new Error('Failed to load resources');

            this.resources = await response.json();
            this.renderResources();
        } catch (error) {
            console.error('Error loading resources:', error);
            this.elements.resourcesList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">&#9888;</div>
                    <div class="empty-state-text">Error loading resources</div>
                    <div class="empty-state-subtext">${error.message}</div>
                </div>
            `;
        }
    },

    /**
     * Render resources list
     */
    renderResources() {
        if (this.resources.length === 0) {
            this.elements.resourcesList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">&#128218;</div>
                    <div class="empty-state-text">No resources yet</div>
                    <div class="empty-state-subtext">Click "Add Resource" to add YouTube videos or other resources</div>
                </div>
            `;
            this.elements.resourceCount.textContent = '';
            return;
        }

        this.elements.resourceCount.textContent = `${this.resources.length} resource${this.resources.length !== 1 ? 's' : ''}`;

        const html = this.resources.map((resource, index) => this.renderResourceCard(resource, index)).join('');
        this.elements.resourcesList.innerHTML = `<div class="resources-grid">${html}</div>`;

        // Bind card action buttons
        this.bindCardActions();

        // Initialize drag and drop
        this.initDragAndDrop();
    },

    /**
     * Render a single resource card
     */
    renderResourceCard(resource, index) {
        const isYoutube = resource.resource_type === 'youtube';
        const thumbnail = isYoutube
            ? `<img src="https://i.ytimg.com/vi/${resource.youtube_video_id}/mqdefault.jpg" alt="${resource.title}">`
            : `<span class="placeholder-icon">${resource.resource_type === 'pdf' ? '&#128196;' : '&#128279;'}</span>`;

        const typeBadge = {
            youtube: '<span class="badge badge-youtube">YouTube</span>',
            link: '<span class="badge badge-link">Link</span>',
            pdf: '<span class="badge badge-pdf">PDF</span>'
        }[resource.resource_type] || '';

        const activeBadge = !resource.is_active ? '<span class="badge badge-inactive">Inactive</span>' : '';

        const videoIdMeta = isYoutube
            ? `<span class="video-id">${resource.youtube_video_id}</span>`
            : '';

        return `
            <div class="resource-card ${!resource.is_active ? 'inactive' : ''}"
                 data-id="${resource.id}"
                 data-index="${index}"
                 draggable="true">
                <div class="drag-handle" title="Drag to reorder">&#9776;</div>
                <div class="resource-thumbnail">${thumbnail}</div>
                <div class="resource-info">
                    <h3 class="resource-title">
                        ${this.escapeHtml(resource.title)}
                        ${typeBadge}
                        ${activeBadge}
                    </h3>
                    <p class="resource-description">${this.escapeHtml(resource.description || 'No description')}</p>
                    <div class="resource-meta">
                        ${videoIdMeta}
                    </div>
                </div>
                <div class="resource-actions">
                    <button class="btn btn-secondary btn-sm edit-btn" data-id="${resource.id}">Edit</button>
                    <button class="btn btn-ghost btn-sm delete-btn" data-id="${resource.id}" data-title="${this.escapeHtml(resource.title)}">Delete</button>
                </div>
            </div>
        `;
    },

    /**
     * Bind edit/delete buttons on cards
     */
    bindCardActions() {
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', () => this.openEditModal(btn.dataset.id));
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', () => this.openDeleteModal(btn.dataset.id, btn.dataset.title));
        });
    },

    /**
     * Initialize drag and drop for reordering
     */
    initDragAndDrop() {
        const cards = document.querySelectorAll('.resource-card');
        let draggedItem = null;

        cards.forEach(card => {
            card.addEventListener('dragstart', (e) => {
                draggedItem = card;
                card.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
            });

            card.addEventListener('dragend', () => {
                card.classList.remove('dragging');
                draggedItem = null;
                this.saveOrder();
            });

            card.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
            });

            card.addEventListener('drop', (e) => {
                e.preventDefault();
                if (draggedItem && draggedItem !== card) {
                    const container = card.parentNode;
                    const allCards = [...container.querySelectorAll('.resource-card')];
                    const draggedIndex = allCards.indexOf(draggedItem);
                    const dropIndex = allCards.indexOf(card);

                    if (draggedIndex < dropIndex) {
                        card.after(draggedItem);
                    } else {
                        card.before(draggedItem);
                    }
                }
            });
        });
    },

    /**
     * Save the new order after drag and drop
     */
    async saveOrder() {
        const cards = document.querySelectorAll('.resource-card');
        const orderedIds = [...cards].map(card => card.dataset.id);

        try {
            const response = await fetch('/api/admin/resources/reorder', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    course_id: this.currentCourseId,
                    ordered_ids: orderedIds
                })
            });

            if (!response.ok) throw new Error('Failed to save order');

            this.showToast('Order saved', 'success');
        } catch (error) {
            console.error('Error saving order:', error);
            this.showToast('Failed to save order', 'error');
            // Reload to reset order
            this.loadResources(this.currentCourseId);
        }
    },

    /**
     * Open modal for adding a new resource
     */
    openAddModal() {
        this.editingId = null;
        this.elements.modalTitle.textContent = 'Add Resource';
        this.elements.resourceForm.reset();
        this.elements.resourceActive.checked = true;
        this.elements.videoPreview.classList.add('hidden');
        this.handleTypeChange();
        this.elements.resourceModal.classList.add('active');
        this.elements.resourceTitle.focus();
    },

    /**
     * Open modal for editing a resource
     */
    openEditModal(resourceId) {
        const resource = this.resources.find(r => r.id === resourceId);
        if (!resource) return;

        this.editingId = resourceId;
        this.elements.modalTitle.textContent = 'Edit Resource';

        // Populate form
        this.elements.resourceId.value = resource.id;
        this.elements.resourceType.value = resource.resource_type;
        this.elements.resourceTitle.value = resource.title;
        this.elements.resourceDescription.value = resource.description || '';
        this.elements.resourceActive.checked = resource.is_active;

        if (resource.resource_type === 'youtube') {
            this.elements.youtubeUrl.value = `https://www.youtube.com/watch?v=${resource.youtube_video_id}`;
            this.updateVideoPreview(resource.youtube_video_id);
        } else {
            this.elements.externalUrl.value = resource.external_url || '';
        }

        this.handleTypeChange();
        this.elements.resourceModal.classList.add('active');
        this.elements.resourceTitle.focus();
    },

    /**
     * Close resource modal
     */
    closeModal() {
        this.elements.resourceModal.classList.remove('active');
        this.editingId = null;
    },

    /**
     * Handle resource type change
     */
    handleTypeChange() {
        const type = this.elements.resourceType.value;

        if (type === 'youtube') {
            this.elements.youtubeFields.classList.remove('hidden');
            this.elements.linkFields.classList.add('hidden');
            this.elements.youtubeUrl.required = true;
            this.elements.externalUrl.required = false;
        } else {
            this.elements.youtubeFields.classList.add('hidden');
            this.elements.linkFields.classList.remove('hidden');
            this.elements.youtubeUrl.required = false;
            this.elements.externalUrl.required = true;
        }
    },

    /**
     * Handle YouTube URL input - extract and preview video ID
     */
    handleYoutubeUrlInput() {
        const url = this.elements.youtubeUrl.value.trim();
        const videoId = this.extractVideoId(url);

        if (videoId) {
            this.updateVideoPreview(videoId);
        } else {
            this.elements.videoPreview.classList.add('hidden');
        }
    },

    /**
     * Extract YouTube video ID from various URL formats
     */
    extractVideoId(url) {
        if (!url) return null;

        // Check if it's already a valid video ID (11 characters)
        if (/^[a-zA-Z0-9_-]{11}$/.test(url)) {
            return url;
        }

        // Try to extract from URL
        const patterns = [
            /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})/
        ];

        for (const pattern of patterns) {
            const match = url.match(pattern);
            if (match) return match[1];
        }

        return null;
    },

    /**
     * Update video preview with thumbnail
     */
    updateVideoPreview(videoId) {
        this.elements.videoThumbnail.src = `https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`;
        this.elements.videoIdDisplay.textContent = `Video ID: ${videoId}`;
        this.elements.videoPreview.classList.remove('hidden');
    },

    /**
     * Handle form submission
     */
    async handleSubmit(e) {
        e.preventDefault();

        const type = this.elements.resourceType.value;
        const data = {
            course_id: this.currentCourseId,
            title: this.elements.resourceTitle.value.trim(),
            description: this.elements.resourceDescription.value.trim(),
            resource_type: type,
            is_active: this.elements.resourceActive.checked
        };

        // Add type-specific fields
        if (type === 'youtube') {
            const videoId = this.extractVideoId(this.elements.youtubeUrl.value.trim());
            if (!videoId) {
                this.showToast('Please enter a valid YouTube URL', 'error');
                return;
            }
            data.youtube_video_id = videoId;
        } else {
            data.external_url = this.elements.externalUrl.value.trim();
        }

        // Disable submit button
        this.elements.saveBtn.disabled = true;
        this.elements.saveBtn.textContent = 'Saving...';

        try {
            let response;
            if (this.editingId) {
                response = await fetch(`/api/admin/resources/${this.editingId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } else {
                response = await fetch('/api/admin/resources', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            }

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Failed to save resource');
            }

            this.showToast(this.editingId ? 'Resource updated' : 'Resource added', 'success');
            this.closeModal();
            this.loadResources(this.currentCourseId);

        } catch (error) {
            console.error('Error saving resource:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.elements.saveBtn.disabled = false;
            this.elements.saveBtn.textContent = 'Save Resource';
        }
    },

    /**
     * Open delete confirmation modal
     */
    openDeleteModal(resourceId, title) {
        this.deletingId = resourceId;
        this.elements.deleteResourceTitle.textContent = title;
        this.elements.deleteModal.classList.add('active');
    },

    /**
     * Close delete modal
     */
    closeDeleteModal() {
        this.elements.deleteModal.classList.remove('active');
        this.deletingId = null;
    },

    /**
     * Confirm and execute delete
     */
    async confirmDelete() {
        if (!this.deletingId) return;

        this.elements.confirmDeleteBtn.disabled = true;
        this.elements.confirmDeleteBtn.textContent = 'Deleting...';

        try {
            const response = await fetch(`/api/admin/resources/${this.deletingId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const result = await response.json();
                throw new Error(result.error || 'Failed to delete resource');
            }

            this.showToast('Resource deleted', 'success');
            this.closeDeleteModal();
            this.loadResources(this.currentCourseId);

        } catch (error) {
            console.error('Error deleting resource:', error);
            this.showToast(error.message, 'error');
        } finally {
            this.elements.confirmDeleteBtn.disabled = false;
            this.elements.confirmDeleteBtn.textContent = 'Delete';
        }
    },

    /**
     * Show toast notification
     */
    showToast(message, type = 'info') {
        if (typeof ToastManager !== 'undefined') {
            ToastManager.show(message, type);
        } else if (typeof showToast === 'function') {
            showToast(message, type);
        } else {
            console.log(`[${type}] ${message}`);
        }
    },

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(str) {
        if (!str) return '';
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    ResourcesManager.init();
});
