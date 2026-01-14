/**
 * Layout JavaScript - Sidebar management and global utilities
 * Extracted from base_layout.html
 */

const SidebarManager = {
    elements: {
        sidebar: null,
        overlay: null,
        menuBtn: null,
        closeBtn: null,
        appLayout: null
    },

    /**
     * Initialize sidebar elements
     */
    init() {
        this.elements.sidebar = document.getElementById('sidebar');
        this.elements.overlay = document.getElementById('sidebar-overlay');
        this.elements.menuBtn = document.querySelector('.mobile-menu-btn');
        this.elements.closeBtn = this.elements.sidebar?.querySelector('.sidebar-close-btn');
        this.elements.appLayout = document.querySelector('.app-layout');

        // Restore collapsed state from localStorage
        const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (isCollapsed && window.innerWidth >= 769) {
            this.collapse();
        }

        // Setup keyboard listener
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen()) {
                this.close();
            }
        });
    },

    /**
     * Check if sidebar is open
     */
    isOpen() {
        return this.elements.sidebar?.classList.contains('open') || false;
    },

    /**
     * Open the sidebar with accessibility support
     */
    open() {
        const { sidebar, overlay, menuBtn, closeBtn } = this.elements;

        if (sidebar) sidebar.classList.add('open');
        if (overlay) overlay.classList.add('visible');
        if (menuBtn) menuBtn.setAttribute('aria-expanded', 'true');

        // Focus the close button for accessibility
        if (closeBtn) closeBtn.focus();

        // Prevent body scroll on mobile
        document.body.style.overflow = 'hidden';
    },

    /**
     * Close the sidebar with accessibility support
     */
    close() {
        const { sidebar, overlay, menuBtn } = this.elements;

        if (sidebar) sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('visible');
        if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');

        // Restore body scroll
        document.body.style.overflow = '';

        // Return focus to menu button
        if (menuBtn) menuBtn.focus();
    },

    /**
     * Toggle sidebar state
     */
    toggle() {
        if (this.isOpen()) {
            this.close();
        } else {
            this.open();
        }
    },

    /**
     * Check if sidebar is collapsed (desktop only)
     */
    isCollapsed() {
        return this.elements.sidebar?.classList.contains('collapsed') || false;
    },

    /**
     * Collapse the sidebar to icons only (desktop)
     */
    collapse() {
        const { sidebar, appLayout } = this.elements;

        if (sidebar) sidebar.classList.add('collapsed');
        if (appLayout) appLayout.classList.add('sidebar-collapsed');

        localStorage.setItem('sidebarCollapsed', 'true');
    },

    /**
     * Expand the sidebar to full width (desktop)
     */
    expand() {
        const { sidebar, appLayout } = this.elements;

        if (sidebar) sidebar.classList.remove('collapsed');
        if (appLayout) appLayout.classList.remove('sidebar-collapsed');

        localStorage.setItem('sidebarCollapsed', 'false');
    },

    /**
     * Toggle collapsed state (desktop)
     */
    toggleCollapse() {
        if (this.isCollapsed()) {
            this.expand();
        } else {
            this.collapse();
        }
    }
};

// Global functions for onclick handlers in HTML
function openSidebar() {
    SidebarManager.open();
}

function closeSidebar() {
    SidebarManager.close();
}

function toggleSidebar() {
    SidebarManager.toggle();
}

function toggleSidebarCollapse() {
    SidebarManager.toggleCollapse();
}

/**
 * Generic modal utilities
 */
const ModalManager = {
    /**
     * Open a modal by ID
     */
    open(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';

            // Focus first focusable element
            const focusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            if (focusable) focusable.focus();
        }
    },

    /**
     * Close a modal by ID
     */
    close(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }
    },

    /**
     * Setup modal close handlers
     */
    setupCloseHandlers(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        // Close on overlay click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.close(modalId);
            }
        });

        // Close on Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                this.close(modalId);
            }
        });

        // Close button
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.close(modalId));
        }
    }
};

// Global function for onclick handlers
function closeModal(modalId) {
    ModalManager.close(modalId);
}

function openModal(modalId) {
    ModalManager.open(modalId);
}

/**
 * Toast notification utility
 */
const ToastManager = {
    container: null,

    init(containerId = 'toastContainer') {
        this.container = document.getElementById(containerId);
    },

    show(message, type = 'info', duration = 5000) {
        if (!this.container) {
            this.container = document.getElementById('toastContainer');
        }
        if (!this.container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="this.parentElement.remove()" aria-label="Close notification">&times;</button>
        `;

        this.container.appendChild(toast);

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                toast.classList.add('toast-fade-out');
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }

        return toast;
    }
};

// Global function
function showToast(message, type = 'info', duration = 5000) {
    return ToastManager.show(message, type, duration);
}

/**
 * CSRF Protection utilities
 * Gets CSRF token from meta tag and provides helper for fetch requests
 */
const CSRFManager = {
    /**
     * Get CSRF token from meta tag
     */
    getToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : null;
    },

    /**
     * Get headers object with CSRF token for fetch requests
     * @param {Object} additionalHeaders - Additional headers to include
     */
    getHeaders(additionalHeaders = {}) {
        const token = this.getToken();
        const headers = { ...additionalHeaders };
        if (token) {
            headers['X-CSRFToken'] = token;
        }
        return headers;
    },

    /**
     * Wrapper for fetch that automatically adds CSRF token
     * @param {string} url - The URL to fetch
     * @param {Object} options - Fetch options
     */
    async fetch(url, options = {}) {
        const token = this.getToken();
        const headers = options.headers || {};

        // Add CSRF token for state-changing methods
        if (['POST', 'PUT', 'DELETE', 'PATCH'].includes((options.method || 'GET').toUpperCase())) {
            if (token) {
                headers['X-CSRFToken'] = token;
            }
        }

        return fetch(url, { ...options, headers });
    }
};

// Global function for getting CSRF token
function getCsrfToken() {
    return CSRFManager.getToken();
}

// Global function for CSRF-protected fetch
function csrfFetch(url, options = {}) {
    return CSRFManager.fetch(url, options);
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    SidebarManager.init();
    ToastManager.init();
});
