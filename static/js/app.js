// Tab switching functionality
function activateTab(clickedTab) {
    // Get all tab buttons 
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    // Remove active classes from all tabs
    tabButtons.forEach(tab => {
        tab.classList.remove('active-tab', 'font-medium', 'border-purple-500', 'text-gray-700');
        tab.classList.add('border-transparent');
        
        // Reset icon color
        const icon = tab.querySelector('i');
        if (icon) {
            icon.classList.remove('text-gray-700');
            icon.classList.add('text-gray-500');
        }
    });
    
    // Add active classes to the clicked tab
    clickedTab.classList.add('active-tab', 'font-medium', 'border-purple-500', 'text-gray-700');
    clickedTab.classList.remove('border-transparent');
    
    // Update icon color
    const clickedIcon = clickedTab.querySelector('i');
    if (clickedIcon) {
        clickedIcon.classList.remove('text-gray-500');
        clickedIcon.classList.add('text-gray-700');
    }
}

// Initialize the default tab on page load
document.addEventListener('DOMContentLoaded', function() {
    const activeTab = document.querySelector('.active-tab');
    if (activeTab) {
        activateTab(activeTab);
    }
});