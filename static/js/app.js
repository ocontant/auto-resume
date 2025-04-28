document.addEventListener('DOMContentLoaded', () => {
    const navTabs = document.getElementById('nav-tabs');
    const contentSection = document.getElementById('resume-content-section');
    const previewContainer = document.getElementById('resume-preview-container');
    const DEFAULT_TAB = 'personal';
    const formInputSelector = '#resume-content-section input[hx-patch], #resume-content-section textarea[hx-patch]';
    const optimizeButton = document.getElementById('optimize-button');

    function getTabFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('tab') || DEFAULT_TAB;
    }

    function updateUrlWithTab(tab) {
        const url = new URL(window.location);
        if (url.searchParams.get('tab') === tab) return;
        url.searchParams.set('tab', tab);
        window.history.pushState({tab}, '', url);
    }

    function setActiveTab(tabName) {
        if (!navTabs) return;

        const buttons = navTabs.querySelectorAll('.tab-btn');

        buttons.forEach(btn => {
            btn.classList.remove('selected');

            if (btn.getAttribute('data-section') === tabName) {
                btn.classList.add('selected');
            }
        });
    }

    function showLoadingIndicator() {
        if (previewContainer) {
            if (!previewContainer.classList.contains('loading')) {
                previewContainer.classList.add('loading');
            }
        } else {
            console.error("Preview container not found for showLoadingIndicator.");
        }
    }

    function hideLoadingIndicator() {
        if (previewContainer) {
            previewContainer.classList.remove('loading');
        } else {
            console.error("Preview container not found for hideLoadingIndicator.");
        }
    }

    function initializeTabs() {
        const initialTab = getTabFromUrl();
        if (!contentSection) return;
        setActiveTab(initialTab);
    }

    function handleAtsDownload(button) {
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
    }

    initializeTabs();

    const downloadAtsButton = document.getElementById('download-ats-button');
    if (downloadAtsButton) {
        downloadAtsButton.addEventListener('click', function () {
            handleAtsDownload(this);
        });
    }

    document.body.addEventListener('htmx:beforeRequest', function (event) {
        const triggerElement = event.detail.elt;
        if (triggerElement && triggerElement.matches(formInputSelector)) {
            showLoadingIndicator();
        }
        // Also handle optimize button loader here for consistency
        if (triggerElement && triggerElement.id === 'optimize-button') {
            showLoadingIndicator();
        }
    });

    // AFTER HTMX finishes the PATCH request for an input field
    document.body.addEventListener('htmx:afterRequest', function (event) {
        const triggerElement = event.detail.elt;
        if (event.target.matches(formInputSelector)) {
            if (event.detail.successful) {
                const resumeEditorDiv = document.querySelector('[data-resume-id]'); // Find element with the attribute directly
                const resumeId = resumeEditorDiv?.dataset.resumeId;
                if (resumeId) {
                    htmx.ajax('GET', `/api/resumes/${resumeId}/preview`, {
                        target: '#resume-preview-content', swap: 'outerHTML'
                        // Hiding loader is handled by the htmx:afterSwap listener now
                    });
                } else {
                    hideLoadingIndicator(); // Hide if no resume ID found
                }
            } else {
                // If the PATCH request itself failed, hide the loader
                hideLoadingIndicator();
            }
        }

        // Handle optimize button errors specifically
        if (triggerElement && triggerElement.id === 'optimize-button' && !event.detail.successful) {
            console.error('Optimize request failed:', event.detail);
            hideLoadingIndicator(); // Hide loader if optimize request fails
        }
    });

    document.body.addEventListener('htmx:afterSwap', function (event) {
        const swapTarget = event.detail.target;
        const triggerElement = event.detail.requestConfig?.elt;

        if (swapTarget && swapTarget.id === 'resume-list-items' && triggerElement?.id === 'resume-upload-form') {
            const importForm = document.getElementById('resume-upload-form');
            if (importForm) {
                importForm.reset();
            }
        }

        if (swapTarget && swapTarget.id === 'resume-preview-content') {
            hideLoadingIndicator();
            const downloadButton = document.getElementById('download-ats-button');
            if (downloadButton) {
                if (triggerElement?.id === 'optimize-button') {
                    downloadButton.disabled = false;
                    downloadButton.title = "Download Optimized Resume as PDF";
                } else {
                    downloadButton.disabled = true;
                    downloadButton.title = "Download Optimized Resume as PDF (Requires Optimize first)";
                }
            }
        }
    });

    document.body.addEventListener('click', function (event) {
        const target = event.target;
        const isAddButton = target.closest('.refresh-preview-on-success');
        const isDeleteButton = target.closest('button[hx-delete][hx-target^="#education-"], button[hx-delete][hx-target^="#experience-"], button[hx-delete][hx-target^="#project-"]');

        if (isAddButton || isDeleteButton) {
            showLoadingIndicator();

            const resumeEditorDiv = document.querySelector('[data-resume-id]');
            const resumeId = resumeEditorDiv?.dataset.resumeId;

            if (resumeId) {
                htmx.ajax('GET', `/api/resumes/${resumeId}/preview`, {
                    target: '#resume-preview-content', swap: 'outerHTML'
                }).then(() => {
                    hideLoadingIndicator();
                }).catch(error => {
                    console.error("Preview refresh AJAX failed:", error);
                    hideLoadingIndicator();
                });
            } else {
                hideLoadingIndicator();
            }
        }
    });

    contentSection?.addEventListener('htmx:afterSwap', function (event) {
        const source = event.detail.requestConfig?.elt;
        if (source && source.hasAttribute('data-section')) {
            const section = source.getAttribute('data-section');
            setActiveTab(section);
            updateUrlWithTab(source.getAttribute('data-section'));
            htmx.process(contentSection);
        }
    });


    optimizeButton.addEventListener('htmx:afterSwap', function (event) {
        const swapTarget = document.getElementById('resume-preview-content'); // Check the actual swap target
        hideLoadingIndicator(); // Hide loader after optimize finishes its swap

        // Enable download button
        const downloadButton = document.getElementById('download-ats-button');
        if (downloadButton) {
            downloadButton.disabled = false;
            downloadButton.title = "Download Optimized Resume as PDF";
        }
    });


});