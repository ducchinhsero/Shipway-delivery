// Header and Footer Loader Script
(function() {
  'use strict';
  
  // Load header into the page
  function loadHeader() {
    const headerContainer = document.getElementById('app-header');
    if (!headerContainer) {
      console.warn('Header container not found');
      return;
    }
    
    // Fetch header.html
    fetch('../shared/header.html')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load header');
        }
        return response.text();
      })
      .then(html => {
        headerContainer.innerHTML = html;
        
        // Add event listeners for header interactions
        setupHeaderEvents();
      })
      .catch(error => {
        console.error('Error loading header:', error);
        // Fallback: create minimal header
        headerContainer.innerHTML = `
          <header class="global-header">
            <div class="header-container">
              <div class="logoholder">
                <img src="../auth/img/logo.png" alt="Shipway" class="logoicon">
                <span class="logo-text">Shipway</span>
              </div>
              <div class="header-right">
                <a href="index.html" class="wallet-button">Ví của tôi</a>
                <a href="#" class="logout-button">Đăng xuất</a>
              </div>
            </div>
          </header>
        `;
      });
  }
  
  // Load footer into the page
  function loadFooter() {
    const footerContainer = document.getElementById('app-footer');
    if (!footerContainer) {
      console.warn('Footer container not found');
      return;
    }
    
    // Fetch footer.html
    fetch('../shared/footer.html')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load footer');
        }
        return response.text();
      })
      .then(html => {
        footerContainer.innerHTML = html;
      })
      .catch(error => {
        console.error('Error loading footer:', error);
        // Fallback: create minimal footer
        footerContainer.innerHTML = `
          <footer class="global-footer">
            <div class="footer-container">
              <p>&copy; 2024 Shipway. All rights reserved.</p>
            </div>
          </footer>
        `;
      });
  }
  
  // Setup header event listeners
  function setupHeaderEvents() {
    // Hamburger menu functionality
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const dropdownMenu = document.getElementById('dropdownMenu');
    
    if (hamburgerBtn && dropdownMenu) {
      // Toggle dropdown menu
      hamburgerBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        const isActive = dropdownMenu.classList.contains('active');
        
        // Close all dropdowns first
        closeAllDropdowns();
        
        // Open this dropdown if it was closed
        if (!isActive) {
          dropdownMenu.classList.add('active');
          hamburgerBtn.classList.add('active');
        }
      });
      
      // Close dropdown when clicking outside
      document.addEventListener('click', function(e) {
        if (!hamburgerBtn.contains(e.target) && !dropdownMenu.contains(e.target)) {
          closeAllDropdowns();
        }
      });
      
      // Close dropdown when pressing Escape key
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          closeAllDropdowns();
        }
      });
      
      // Handle dropdown item clicks
      const dropdownItems = dropdownMenu.querySelectorAll('.dropdown-item');
      dropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
          // Special handling for logout
          if (item.classList.contains('logout-item')) {
            e.preventDefault();
            if (confirm('Bạn có chắc muốn đăng xuất?')) {
              localStorage.clear();
              sessionStorage.clear();
              window.location.href = '../onboarding/index.html';
            }
          } else if (item.id === 'profileLink') {
            e.preventDefault();
            alert('Profile page coming soon!');
          }
          
          // Close dropdown after clicking
          closeAllDropdowns();
        });
      });
    }
  }
  
  // Close all dropdown menus
  function closeAllDropdowns() {
    const dropdownMenu = document.getElementById('dropdownMenu');
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    
    if (dropdownMenu) {
      dropdownMenu.classList.remove('active');
    }
    if (hamburgerBtn) {
      hamburgerBtn.classList.remove('active');
    }
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      loadHeader();
      loadFooter();
    });
  } else {
    loadHeader();
    loadFooter();
  }
})();
