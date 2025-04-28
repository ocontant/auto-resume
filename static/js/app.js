// Constants
const DEFAULT_TAB = 'personal';
const FORM_INPUT_SELECTOR = '#resume-content-section input[hx-patch], #resume-content-section textarea[hx-patch]';

// DOM Elements
const navTabs = document.getElementById('nav-tabs');
const contentSection = document.getElementById('resume-content-section');
const previewContainer = document.getElementById('resume-preview-container');
const optimizeButton = document.getElementById('optimize-button');
const downloadAtsButton = document.getElementById('download-ats-button');

/**
 * Manages tab functionality
 */
const TabManager = {
  /**
   * Get the active tab from URL parameters
   * @returns {string} The active tab name or default tab
   */
  getTabFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('tab') || DEFAULT_TAB;
  },

  /**
   * Update the URL with the active tab
   * @param {string} tab - The tab name to set in URL
   */
  updateUrlWithTab(tab) {
    const url = new URL(window.location);
    if (url.searchParams.get('tab') === tab) return;
    url.searchParams.set('tab', tab);
    window.history.pushState({tab}, '', url);
  },

  /**
   * Set the visual active state on the tab button
   * @param {string} tabName - The tab name to activate
   */
  setActiveTab(tabName) {
    if (!navTabs) return;

    const buttons = navTabs.querySelectorAll('.tab-btn');

    buttons.forEach(btn => {
      btn.classList.remove('selected');

      if (btn.getAttribute('data-section') === tabName) {
        btn.classList.add('selected');
      }
    });
  },

  /**
   * Initialize tabs based on URL
   */
  initialize() {
    const initialTab = this.getTabFromUrl();
    if (!contentSection) return;
    this.setActiveTab(initialTab);
  }
};

/**
 * Manages loading indicators
 */
const LoadingManager = {
  /**
   * Show loading indicator on the preview container
   */
  showLoadingIndicator() {
    if (!previewContainer) {
      console.error("Preview container not found for showLoadingIndicator.");
      return;
    }

    if (!previewContainer.classList.contains('loading')) {
      previewContainer.classList.add('loading');
    }
  },

  /**
   * Hide loading indicator on the preview container
   */
  hideLoadingIndicator() {
    if (!previewContainer) {
      console.error("Preview container not found for hideLoadingIndicator.");
      return;
    }

    previewContainer.classList.remove('loading');
  }
};

/**
 * Manages resume preview functionality
 */
const PreviewManager = {
  /**
   * Refresh the resume preview
   * @returns {Promise} Promise resolving when preview is refreshed
   */
  refreshPreview() {
    LoadingManager.showLoadingIndicator();

    const resumeEditorDiv = document.querySelector('[data-resume-id]');
    const resumeId = resumeEditorDiv?.dataset.resumeId;

    if (resumeId) {
      return htmx.ajax('GET', `/api/resumes/${resumeId}/preview`, {
        target: '#resume-preview-content',
        swap: 'outerHTML'
      }).then(() => {
        LoadingManager.hideLoadingIndicator();
      }).catch(error => {
        console.error("Preview refresh AJAX failed:", error);
        LoadingManager.hideLoadingIndicator();
      });
    } else {
      LoadingManager.hideLoadingIndicator();
      return Promise.reject(new Error("No resume ID found"));
    }
  },

  /**
   * Update download button state
   * @param {boolean} isOptimized - Whether resume is optimized
   */
  updateDownloadButton(isOptimized) {
    const downloadButton = document.getElementById('download-ats-button');
    if (downloadButton) {
      downloadButton.disabled = !isOptimized;
      downloadButton.title = isOptimized
        ? "Download Optimized Resume as PDF"
        : "Download Optimized Resume as PDF (Requires Optimize first)";
    }
  }
};

/**
 * Document action handlers
 */
const DocumentActions = {
  /**
   * Handle ATS download button click
   * @param {HTMLElement} button - The download button element
   */
  handleAtsDownload(button) {
    const url = button.dataset.url;
    const contentSelector = button.dataset.contentSelector;
    const contentElement = document.querySelector(contentSelector);
    const htmlContent = contentElement ? contentElement.innerHTML : "";

    if (!url || !contentSelector) {
      console.error("Button is missing data-url or data-content-selector");
      return;
    }

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = url;
    form.style.display = 'none';

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'html_content';
    input.value = htmlContent;
    form.appendChild(input);

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
  },

  /**
   * Handle preview refresh actions (add/delete items)
   * @param {Event} event - The click event
   */
  handlePreviewRefreshAction(event) {
    // Check if the clicked element has the refresh-preview-on-success class
    // or is a delete button (which should also have this class ideally)
    const triggerElement = event.target.closest('.refresh-preview-on-success');

    if (triggerElement) {
      PreviewManager.refreshPreview();
    }
  }
};

/**
 * Event handler setup and management
 */
const EventHandlers = {
  /**
   * Initialize all event listeners
   */
  setupEventListeners() {
    // Download ATS button
    if (downloadAtsButton) {
      downloadAtsButton.addEventListener('click', function() {
        DocumentActions.handleAtsDownload(this);
      });
    }

    // HTMX before request (show loading)
    document.addEventListener('htmx:beforeRequest', function(event) {
      const triggerElement = event.detail.elt;
      if (triggerElement && triggerElement.matches(FORM_INPUT_SELECTOR)) {
        LoadingManager.showLoadingIndicator();
      }

      // Handle optimize button loader
      if (triggerElement && triggerElement.id === 'optimize-button') {
        LoadingManager.showLoadingIndicator();
      }
    });

    // HTMX after request (for form inputs)
    document.addEventListener('htmx:afterRequest', function(event) {
      const triggerElement = event.detail.elt;

      if (event.target.matches(FORM_INPUT_SELECTOR)) {
        if (event.detail.successful) {
          const resumeEditorDiv = document.querySelector('[data-resume-id]');
          const resumeId = resumeEditorDiv?.dataset.resumeId;

          if (resumeId) {
            htmx.ajax('GET', `/api/resumes/${resumeId}/preview`, {
              target: '#resume-preview-content',
              swap: 'outerHTML'
            });
          } else {
            LoadingManager.hideLoadingIndicator();
          }
        } else {
          LoadingManager.hideLoadingIndicator();
        }
      }

      // Handle optimize button errors
      if (triggerElement && triggerElement.id === 'optimize-button' && !event.detail.successful) {
        console.error('Optimize request failed:', event.detail);
        LoadingManager.hideLoadingIndicator();
      }
    });

    // HTMX after swap (update UI after content changes)
    document.addEventListener('htmx:afterSwap', function(event) {
      const swapTarget = event.detail.target;
      const triggerElement = event.detail.requestConfig?.elt;

      // Handle resume list updates after upload
      if (swapTarget && swapTarget.id === 'resume-list-items' && triggerElement?.id === 'resume-upload-form') {
        const importForm = document.getElementById('resume-upload-form');
        if (importForm) importForm.reset();
      }

      // Handle preview content updates
      if (swapTarget && swapTarget.id === 'resume-preview-content') {
        LoadingManager.hideLoadingIndicator();

        // Update download button state based on optimization status
        const isOptimized = triggerElement?.id === 'optimize-button';
        PreviewManager.updateDownloadButton(isOptimized);
      }
    });

    // Tab section changes
    if (contentSection) {
      contentSection.addEventListener('htmx:afterSwap', function(event) {
        const source = event.detail.requestConfig?.elt;
        if (source && source.hasAttribute('data-section')) {
          const section = source.getAttribute('data-section');
          TabManager.setActiveTab(section);
          TabManager.updateUrlWithTab(section);
          htmx.process(contentSection);
        }
      });
    }

    // Optimize button specific handler
    if (optimizeButton) {
      optimizeButton.addEventListener('htmx:afterSwap', function() {
        LoadingManager.hideLoadingIndicator();
        PreviewManager.updateDownloadButton(true);
      });
    }

    // Delegate click handler for preview refresh actions
    document.addEventListener('click', DocumentActions.handlePreviewRefreshAction);
  }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  TabManager.initialize();
  EventHandlers.setupEventListeners();
});