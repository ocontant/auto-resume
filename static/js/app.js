// Constants
const DEFAULT_TAB = 'personal';
const FORM_INPUT_SELECTOR = '#resume-content-section input[hx-patch], #resume-content-section textarea[hx-patch]';

// DOM Elements Cache (Initialize after DOMContentLoaded)
let navTabs = null;
let contentSection = null;
let previewContainer = null;
let optimizeButton = null;
let downloadAtsButton = null;

// State
let currentOptimizeXhr = null;

/**
 * Caches frequently accessed DOM elements.
 */
function cacheDOMElements() {
    navTabs = document.getElementById('nav-tabs');
    contentSection = document.getElementById('resume-content-section');
    previewContainer = document.getElementById('resume-preview-container');
    optimizeButton = document.getElementById('optimize-button');
    downloadAtsButton = document.getElementById('download-ats-button');
}

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
    // Set active tab regardless of whether contentSection exists (e.g., on config page)
    if (navTabs) {
        this.setActiveTab(initialTab);
    }
  }
};

/**
 * Manages loading indicators for the preview area.
 */
const LoadingManager = {
  showLoadingIndicator() {
    if (!previewContainer) return;
    previewContainer.classList.add('loading');
  },

  hideLoadingIndicator() {
    if (!previewContainer) return;
    previewContainer.classList.remove('loading');
  }
};

/**
 * Manages resume preview functionality, including optimization cancellation.
 */
const PreviewManager = {
  /**
   * Refresh the resume preview, cancelling ongoing optimization if necessary.
   * @returns {Promise} Promise resolving when preview is refreshed or rejected on error/abort.
   */
  refreshPreview() {
    if (currentOptimizeXhr) {
      console.log('Preview refresh triggered while optimization in progress. Aborting optimization.');
      currentOptimizeXhr.abort(); // Abort the request
      currentOptimizeXhr = null;  // Clear the reference
      this._resetOptimizeButtonState(); // Manually reset button visuals
    }

    if (!previewContainer) {
        console.warn("Preview container not found, skipping refresh.");
        return Promise.resolve(); // Resolve gracefully if no preview area
    }

    LoadingManager.showLoadingIndicator();

    const resumeEditorDiv = document.querySelector('[data-resume-id]');
    const resumeId = resumeEditorDiv?.dataset.resumeId;

    if (resumeId) {
      return htmx.ajax('GET', `/api/resumes/${resumeId}/preview`, {
        target: '#resume-preview-content',
        swap: 'outerHTML'
      }).catch(error => {
        if (error.xhr?.statusText === 'abort') {
            console.log('Preview refresh AJAX aborted.');
        } else {
            console.error("Preview refresh AJAX failed:", error);
        }
        LoadingManager.hideLoadingIndicator();
        return Promise.reject(error);
      });
    } else {
      console.error("No resume ID found for preview refresh.");
      LoadingManager.hideLoadingIndicator();
      return Promise.reject(new Error("No resume ID found"));
    }
  },

  /**
   * Update download button state based on whether the resume is considered optimized.
   * @param {boolean} isOptimized - Whether resume is optimized.
   */
  updateDownloadButton(isOptimized) {
    if (downloadAtsButton) {
      downloadAtsButton.disabled = !isOptimized;
      downloadAtsButton.title = isOptimized
        ? "Download Optimized Resume as PDF"
        : "Download Optimized Resume as PDF (Requires Optimize first)";
    }
  },

  /**
   * Resets the visual state of the optimize button if it was interrupted.
   * @private
   */
  _resetOptimizeButtonState() {
      if (optimizeButton && optimizeButton.classList.contains('htmx-request')) {
          optimizeButton.classList.remove('htmx-request');
          const indicator = optimizeButton.querySelector('.htmx-indicator');
          const content = optimizeButton.querySelector('.button-content');
          if (indicator) indicator.style.display = 'none';
          if (content) content.style.visibility = 'visible';
          // Ensure download button is disabled if optimization was aborted mid-flight
          this.updateDownloadButton(false);
      }
  }
};

/**
 * Handles specific document-level actions like downloads and delegated clicks.
 */
const DocumentActions = {
  /**
   * Handle ATS download button click by submitting preview content via form post.
   * @param {HTMLElement} button - The download button element.
   */
   handleAtsDownload(button) {
    const url = button.dataset.url;
    const contentSelector = button.dataset.contentSelector;
    const contentElement = document.querySelector(contentSelector);
    const htmlContent = contentElement ? contentElement.innerHTML : "";

    if (!url || !contentSelector || !htmlContent) {
      console.error("Download button missing data-url, data-content-selector, or preview content is empty.");
      return;
    }

    const form = document.createElement('form');
    form.method = 'POST';
    form.action = url;
    form.style.display = 'none';

    const contentInput = document.createElement('input');
    contentInput.type = 'hidden';
    contentInput.name = 'html_content';
    contentInput.value = htmlContent;
    form.appendChild(contentInput);

    // Include CSRF token if present (common in Flask/Django)
    const csrfTokenInput = document.querySelector('input[name="csrf_token"]');
    if (csrfTokenInput) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = csrfTokenInput.name;
        csrfInput.value = csrfTokenInput.value;
        form.appendChild(csrfInput);
    }

    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
  },

  /**
   * Handle clicks on elements indicating a preview refresh is needed after success.
   * This uses event delegation on the document body.
   * @param {Event} event - The click event.
   */
  handlePreviewRefreshAction(event) {
    // Triggered by add/delete buttons for list items (e.g., education, experience)
    const triggerElement = event.target.closest('.refresh-preview-on-success');
    if (triggerElement) {
      // The refreshPreview call itself handles potential optimization cancellation.
      PreviewManager.refreshPreview().catch(() => {
          console.warn("Preview refresh after add/delete action failed or was aborted.");
      });
    }
  }
};

/**
 * Sets up and manages all event listeners for the application.
 */
const EventHandlers = {
  /**
   * Initialize all event listeners, delegating from document.body where appropriate.
   */
  setupEventListeners() {
    // Specific button listeners (if they exist on the page)
    if (downloadAtsButton) {
        downloadAtsButton.addEventListener('click', () => DocumentActions.handleAtsDownload(downloadAtsButton));
    }

    // Use event delegation for HTMX events on document.body
    document.body.addEventListener('htmx:beforeSend', this.handleBeforeSend);
    document.body.addEventListener('htmx:beforeRequest', this.handleBeforeRequest);
    document.body.addEventListener('htmx:afterRequest', this.handleAfterRequest);
    document.body.addEventListener('htmx:afterSwap', this.handleAfterSwap);

    // Delegated click handler for add/delete buttons
    document.body.addEventListener('click', DocumentActions.handlePreviewRefreshAction);
  },

  handleBeforeSend(event) {
    const triggerElement = event.detail.elt;
    if (triggerElement?.id === 'optimize-button') {
        if (currentOptimizeXhr) {
            console.warn('Aborting previous stale optimize request.');
            currentOptimizeXhr.abort();
            PreviewManager._resetOptimizeButtonState(); // Ensure old one is visually reset
        }
        currentOptimizeXhr = event.detail.xhr;
        LoadingManager.showLoadingIndicator(); // Show indicator tied to optimize start
    }
  },

  handleBeforeRequest(event) {
    const triggerElement = event.detail.elt;
    // Show loading only for form inputs saves (optimization loader handled in beforeSend)
    if (triggerElement?.matches(FORM_INPUT_SELECTOR)) {
      LoadingManager.showLoadingIndicator();
    }
  },

  handleAfterRequest(event) {
    const triggerElement = event.detail.elt;
    const successful = event.detail.successful;

    // Form input saves: Trigger explicit preview refresh on success
    if (triggerElement?.matches(FORM_INPUT_SELECTOR)) {
      if (successful) {
        PreviewManager.refreshPreview().catch(() => {
            console.warn("Preview refresh after form input save failed or was aborted.");
            LoadingManager.hideLoadingIndicator(); // Hide if refresh fails post-save
        });
        // Indicator hidden by subsequent preview refresh's afterSwap on success
      } else {
        console.error('Form input save request failed:', event.detail.xhr?.statusText, event.detail);
        LoadingManager.hideLoadingIndicator(); // Hide on explicit save failure
      }
    }

    // Optimize button completion (success, failure, or abort)
    if (triggerElement?.id === 'optimize-button') {
      const wasAborted = !successful && event.detail.xhr?.statusText === 'abort';
      currentOptimizeXhr = null; // Clear reference regardless

      if (!successful) {
        if (wasAborted) {
            console.log('Optimize request was aborted.');
        } else {
            console.error('Optimize request failed:', event.detail.xhr?.statusText, event.detail);
        }
        LoadingManager.hideLoadingIndicator(); // Hide indicator on failure/abort
        PreviewManager._resetOptimizeButtonState(); // Ensure button reset visually
        PreviewManager.updateDownloadButton(false); // Ensure download disabled
      }
      // On success: Indicator hiding and download button update are handled by the
      // 'htmx:afterSwap' listener on the #resume-preview-content target.
    }
  },

  handleAfterSwap(event) {
    const swapTarget = event.detail.target;
    const triggerElement = event.detail.requestConfig?.elt;
    const xhr = event.detail.xhr;

    // Resume list updates after upload
    if (swapTarget?.id === 'resume-list-items' && triggerElement?.id === 'resume-upload-form') {
        const importForm = document.getElementById('resume-upload-form');
        if (importForm) importForm.reset();
    }

    // Preview content updates (from any source: optimize, save, add, delete)
    if (swapTarget?.matches('#resume-preview-content')) {
      LoadingManager.hideLoadingIndicator(); // Hide indicator after successful preview swap

      // Determine if the update was triggered by a *successful* optimization
      const optimizeSucceeded = triggerElement?.id === 'optimize-button' && xhr?.status >= 200 && xhr?.status < 300;
      PreviewManager.updateDownloadButton(optimizeSucceeded);

      htmx.process(swapTarget); // Process any new HTMX attributes in the swapped content
    }

     // Tab content swaps
     if (swapTarget?.id === 'resume-content-section' && triggerElement?.hasAttribute('data-section')) {
          const section = triggerElement.getAttribute('data-section');
          TabManager.setActiveTab(section);
          TabManager.updateUrlWithTab(section);
          htmx.process(swapTarget); // Process new tab content
     }
   }
};

// Initialize application logic after the DOM is fully loaded.
document.addEventListener('DOMContentLoaded', () => {
  cacheDOMElements(); // Find and store references to key elements
  TabManager.initialize();
  EventHandlers.setupEventListeners();

  // Set initial state for the download button based on its server-rendered state
  if (downloadAtsButton) {
      PreviewManager.updateDownloadButton(!downloadAtsButton.disabled);
  }
});
