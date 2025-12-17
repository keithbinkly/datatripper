/**
 * Frontier TUI Controller
 * Handles Data Engine, Filters, Context Cards, and Keyboard Interaction
 */

class KnowledgeStore {
  constructor(data) {
    this.authors = new Map(data.authors.map(a => [a.id, a]));
    this.resources = data.resources || [];
  }

  getAuthor(id) {
    return this.authors.get(id);
  }

  filterResources(filters) {
    // Basic filter implementation for future expansion
    return this.resources;
  }
}

class TUIController {
  constructor() {
    this.store = null;
    this.activeFilters = new Set(['practitioner', 'vendor', 'journalist', 'academic', 'researcher']);
    this.zenMode = false;
    this.cardTimer = null;
    
    // Components
    this.els = {
      root: document.getElementById('app-root'),
      contextCard: document.getElementById('context-card'),
      timeBudget: document.getElementById('time-budget'),
      quickPeek: document.getElementById('quick-peek')
    };

    this.init();
  }

  async init() {
    // Wait for data injection
    if (window.KB_DATA) {
      this.store = new KnowledgeStore(window.KB_DATA);
      this.renderControls();
      this.setupInteractions();
      this.updateTimeBudget();
      console.log('TUI: System Online');
    } else {
      console.error('TUI: Data Source Missing');
    }
  }

  setupInteractions() {
    // 1. Perspective Equalizer
    document.querySelectorAll('.perspective-toggle').forEach(btn => {
      btn.addEventListener('click', (e) => this.toggleFilter(e.currentTarget));
    });

    // 2. Context Cards (Hover Intent)
    document.querySelectorAll('[data-author-id]').forEach(el => {
      el.addEventListener('mouseenter', (e) => this.showCard(e, el.dataset.authorId));
      el.addEventListener('mouseleave', () => this.hideCard());
    });

    // 3. Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === 'z') this.toggleZenMode();
      if (e.key === 'Escape') this.closeQuickPeek();
      if (e.code === 'Space' && document.activeElement.classList.contains('tlink')) {
        e.preventDefault();
        this.openQuickPeek(document.activeElement);
      }
    });
  }

  // --- Logic: Filtering ---

  toggleFilter(btn) {
    const type = btn.dataset.type;
    if (this.activeFilters.has(type)) {
      this.activeFilters.delete(type);
      btn.classList.remove('active');
      btn.querySelector('.perspective-check').textContent = '[ ]';
    } else {
      this.activeFilters.add(type);
      btn.classList.add('active');
      btn.querySelector('.perspective-check').textContent = '[x]';
    }
    this.applyFilters();
  }

  applyFilters() {
    const links = document.querySelectorAll('.tlink');
    let visibleCount = 0;
    let totalMins = 0;

    links.forEach(link => {
      const authorId = link.dataset.authorId;
      const author = this.store.getAuthor(authorId);
      
      // Determine visibility
      const isVisible = author && this.activeFilters.has(author.perspectiveType);
      
      link.style.display = isVisible ? 'flex' : 'none';
      if (isVisible) {
        visibleCount++;
        totalMins += parseInt(link.dataset.time || 0);
      }
    });

    // Update Status Bar
    document.getElementById('status-count').textContent = `${visibleCount} items`;
    document.getElementById('time-budget').textContent = `${Math.ceil(totalMins/60)}h ${totalMins%60}m`;
  }

  // --- Logic: Context Cards ---

  showCard(e, authorId) {
    const author = this.store.getAuthor(authorId);
    if (!author) return;

    this.cardTimer = setTimeout(() => {
      const card = this.els.contextCard;
      const rect = e.target.getBoundingClientRect();
      
      // Populate Data
      card.querySelector('.cc-name').textContent = author.name;
      card.querySelector('.cc-role').textContent = author.perspectiveType;
      card.querySelector('.cc-org').textContent = author.affiliation || 'Independent';
      card.querySelector('.cc-loc').textContent = author.location?.country || 'Unknown';
      card.querySelector('.cc-exp').textContent = author.yearsInField ? `${author.yearsInField}y` : '~';

      // Position
      card.style.top = `${rect.bottom + window.scrollY + 10}px`;
      card.style.left = `${Math.min(rect.left, window.innerWidth - 320)}px`;
      card.classList.add('visible');
    }, 300); // 300ms hover intent
  }

  hideCard() {
    clearTimeout(this.cardTimer);
    this.els.contextCard.classList.remove('visible');
  }

  // --- Logic: Features ---

  toggleZenMode() {
    this.zenMode = !this.zenMode;
    document.body.classList.toggle('zen-mode');
    document.getElementById('status-mode').textContent = this.zenMode ? 'ZEN' : 'NORMAL';
  }

  updateTimeBudget() {
    this.applyFilters(); // Initial calculation
  }

  renderControls() {
    // Optional: Dynamic rendering if needed
  }
}

// Boot
document.addEventListener('DOMContentLoaded', () => {
  window.tui = new TUIController();
});
