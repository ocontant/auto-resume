document.addEventListener('DOMContentLoaded', () => {
    const navTabs = document.getElementById('nav-tabs');
    const contentSection = document.getElementById('resume-content-section');
    
    const DEFAULT_TAB = 'personal';

    function getTabFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('tab') || DEFAULT_TAB;
    }

    function updateUrlWithTab(tab) {
        const url = new URL(window.location);
        if (url.searchParams.get('tab') === tab) return;
        url.searchParams.set('tab', tab);
        window.history.pushState({ tab }, '', url);
    }

    function setActiveTab(tabName) {
        if (!navTabs) return;

        const buttons = navTabs.querySelectorAll('.tab-btn');

        buttons.forEach(btn => {
            // Remove selected class from all buttons
            btn.classList.remove('selected');

            if (btn.getAttribute('data-section') === tabName) {
                // Add selected class to the target button
                btn.classList.add('selected');
            }
        });
    }

    function initializeTabs() {
        const initialTab = getTabFromUrl();
        
        setActiveTab(initialTab);

        contentSection.addEventListener('htmx:afterSwap', function(event) {
            const source = event.detail.requestConfig ? event.detail.requestConfig.elt : null;
            if (source && source.hasAttribute('data-section')) {
                const section = source.getAttribute('data-section');
                setActiveTab(section); // Update styling
                updateUrlWithTab(source.getAttribute('data-section')); // Update URL
            }
        });
    }

    initializeTabs();
});
