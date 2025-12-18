/**
 * Frontier TUI Controller v2.0
 * Premium interactions: Keyboard nav, animations, context cards, Quick Peek
 * Dependencies: Tippy.js, Anime.js (optional, graceful fallback)
 */

class TUIController {
  constructor() {
    this.focusedIndex = -1;
    this.quickPeekActive = false;
    this.zenMode = false;
    this.helpVisible = false;

    // Collect all interactive rows
    this.rows = [];
    this.init();
  }

  init() {
    // Wait for DOM
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }

  setup() {
    this.collectRows();
    this.setupKeyboardNav();
    this.setupCollapsibleSections();
    this.setupQuickPeek();
    this.setupContextCards();
    this.createHelpOverlay();
    console.log('TUI v2.0: System Online');
  }

  // ═══════════════════════════════════════════
  // KEYBOARD NAVIGATION
  // ═══════════════════════════════════════════

  collectRows() {
    // Support both .tlink (topic pages) and .resource-row (knowledge-engineering)
    this.rows = Array.from(document.querySelectorAll('.tlink, .resource-row'));
    // Make rows focusable
    this.rows.forEach((row, i) => {
      row.setAttribute('tabindex', '0');
      row.dataset.rowIndex = i;
    });
  }

  setupKeyboardNav() {
    document.addEventListener('keydown', (e) => {
      // Ignore if typing in input
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      switch(e.key) {
        case 'j':
          e.preventDefault();
          this.navigateRows(1);
          break;
        case 'k':
          e.preventDefault();
          this.navigateRows(-1);
          break;
        case 'o':
          e.preventDefault();
          this.openFocusedRow();
          break;
        case 'Enter':
          if (this.focusedIndex >= 0) {
            e.preventDefault();
            this.toggleQuickPeek(this.rows[this.focusedIndex]);
          }
          break;
        case ' ':
          if (this.focusedIndex >= 0) {
            e.preventDefault();
            this.toggleQuickPeek(this.rows[this.focusedIndex]);
          }
          break;
        case 'Escape':
          this.closeQuickPeek();
          this.hideHelp();
          break;
        case '?':
          e.preventDefault();
          this.toggleHelp();
          break;
        case 'z':
          this.toggleZenMode();
          break;
        case 'g':
          if (this._lastKey === 'g') {
            e.preventDefault();
            this.jumpToTop();
            this._lastKey = null;
          } else {
            this._lastKey = 'g';
            setTimeout(() => this._lastKey = null, 500);
          }
          break;
        case 'G':
          e.preventDefault();
          this.jumpToBottom();
          break;
      }
    });
  }

  navigateRows(direction) {
    if (this.rows.length === 0) return;

    // Filter to visible rows only
    const visibleRows = this.rows.filter(r =>
      r.offsetParent !== null && !r.classList.contains('section-hidden')
    );
    if (visibleRows.length === 0) return;

    // Find current position in visible rows
    let currentIndex = -1;
    if (this.focusedIndex >= 0) {
      currentIndex = visibleRows.indexOf(this.rows[this.focusedIndex]);
    }

    // Calculate new index
    let newIndex = currentIndex + direction;
    if (newIndex < 0) newIndex = 0;
    if (newIndex >= visibleRows.length) newIndex = visibleRows.length - 1;

    // Update focus
    const newRow = visibleRows[newIndex];
    this.focusRow(newRow);
  }

  focusRow(row) {
    // Remove previous focus
    this.rows.forEach(r => r.classList.remove('tui-focused'));

    // Add focus to new row
    row.classList.add('tui-focused');
    this.focusedIndex = this.rows.indexOf(row);

    // Scroll into view smoothly
    row.scrollIntoView({ behavior: 'smooth', block: 'center' });
    row.focus();

    // Update preview pane if it exists (knowledge-engineering page)
    const resourceId = row.dataset.resourceId;
    if (resourceId && typeof updateResourcePreview === 'function') {
      updateResourcePreview(resourceId);
    }

    // Animate focus (if anime.js available)
    if (typeof anime !== 'undefined') {
      anime({
        targets: row,
        boxShadow: ['0 0 0 0 rgba(92, 207, 230, 0)', '0 0 0 2px rgba(92, 207, 230, 0.3)', '0 0 0 0 rgba(92, 207, 230, 0)'],
        duration: 600,
        easing: 'easeOutQuad'
      });
    }
  }

  openFocusedRow() {
    if (this.focusedIndex >= 0) {
      const row = this.rows[this.focusedIndex];
      let url = row.href || row.querySelector('a')?.href;

      // For knowledge-engineering, get URL from resourceData
      const resourceId = row.dataset.resourceId;
      if (!url && resourceId && typeof resourceData !== 'undefined' && resourceData[resourceId]) {
        url = resourceData[resourceId].url;
      }

      if (url) window.open(url, '_blank');
    }
  }

  jumpToTop() {
    const visibleRows = this.rows.filter(r => r.offsetParent !== null);
    if (visibleRows.length > 0) {
      this.focusRow(visibleRows[0]);
    }
  }

  jumpToBottom() {
    const visibleRows = this.rows.filter(r => r.offsetParent !== null);
    if (visibleRows.length > 0) {
      this.focusRow(visibleRows[visibleRows.length - 1]);
    }
  }

  // ═══════════════════════════════════════════
  // COLLAPSIBLE SECTIONS (Animated)
  // ═══════════════════════════════════════════

  setupCollapsibleSections() {
    document.querySelectorAll('.tcat').forEach(header => {
      // Skip if already has listener (from inline JS)
      if (header.dataset.tuiEnhanced) return;
      header.dataset.tuiEnhanced = 'true';

      header.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleSection(header);
      });
    });
  }

  toggleSection(header) {
    const isCollapsing = !header.classList.contains('collapsed');
    header.classList.toggle('collapsed');

    // Get content items
    const content = this.getSectionContent(header);

    if (typeof anime !== 'undefined' && content.length > 0) {
      if (isCollapsing) {
        // Animate collapse with stagger
        anime({
          targets: content,
          opacity: [1, 0],
          translateY: [0, -10],
          duration: 200,
          delay: anime.stagger(20, { direction: 'reverse' }),
          easing: 'easeOutQuad',
          complete: () => {
            content.forEach(item => item.classList.add('section-hidden'));
          }
        });
      } else {
        // Animate expand with stagger
        content.forEach(item => item.classList.remove('section-hidden'));
        anime({
          targets: content,
          opacity: [0, 1],
          translateY: [-10, 0],
          duration: 200,
          delay: anime.stagger(20),
          easing: 'easeOutQuad'
        });
      }
    } else {
      // Fallback: instant toggle
      content.forEach(item => {
        item.classList.toggle('section-hidden', isCollapsing);
      });
    }
  }

  getSectionContent(header) {
    const content = [];
    let sibling = header.nextElementSibling;
    while (sibling && !sibling.classList.contains('tcat')) {
      if (sibling.classList.contains('tlink') || sibling.classList.contains('section-content')) {
        content.push(sibling);
      }
      sibling = sibling.nextElementSibling;
    }
    return content;
  }

  // ═══════════════════════════════════════════
  // QUICK PEEK (Inline Expand)
  // ═══════════════════════════════════════════

  setupQuickPeek() {
    // Click handler for rows (desktop)
    this.rows.forEach(row => {
      row.addEventListener('dblclick', (e) => {
        // Double-click to toggle quick peek
        e.preventDefault();
        this.toggleQuickPeek(row);
      });
    });
  }

  toggleQuickPeek(row) {
    // If page has showResourceCard (knowledge-engineering), use that instead
    const resourceId = row.dataset.resourceId;
    if (resourceId && typeof showResourceCard === 'function') {
      showResourceCard(resourceId, row);
      return;
    }

    // Otherwise use inline quick peek for .tlink pages
    if (row.classList.contains('quick-peek-active')) {
      this.closeQuickPeek();
    } else {
      this.openQuickPeek(row);
    }
  }

  openQuickPeek(row) {
    // Close any existing
    this.closeQuickPeek();

    // Get description from existing .tlink-desc
    const desc = row.querySelector('.tlink-desc');
    const title = row.querySelector('.tlink-title')?.textContent || '';
    const author = row.querySelector('.tlink-author')?.textContent || '';
    const time = row.querySelector('.tlink-time')?.textContent || '';
    const url = row.href;

    // Only show inline peek if we have content
    if (!desc?.textContent?.trim()) {
      // No description - just open the resource
      if (url) window.open(url, '_blank');
      return;
    }

    // Create quick peek content
    const peekContent = document.createElement('div');
    peekContent.className = 'quick-peek-content';
    peekContent.innerHTML = `
      <div class="qp-header">
        <span class="qp-title">${title}</span>
        <span class="qp-meta">${author} · ${time}</span>
      </div>
      <div class="qp-body">
        ${desc.textContent}
      </div>
      <div class="qp-actions">
        <a href="${url}" target="_blank" class="qp-open">Open Resource →</a>
        <button class="qp-close">Close</button>
      </div>
    `;

    // Insert after row
    row.after(peekContent);
    row.classList.add('quick-peek-active');
    this.quickPeekActive = true;

    // Close button handler
    peekContent.querySelector('.qp-close').addEventListener('click', () => {
      this.closeQuickPeek();
    });

    // Animate in
    if (typeof anime !== 'undefined') {
      anime({
        targets: peekContent,
        opacity: [0, 1],
        maxHeight: ['0px', '200px'],
        duration: 250,
        easing: 'easeOutQuad'
      });
    }
  }

  closeQuickPeek() {
    const activeRow = document.querySelector('.quick-peek-active');
    const peekContent = document.querySelector('.quick-peek-content');

    if (peekContent) {
      if (typeof anime !== 'undefined') {
        anime({
          targets: peekContent,
          opacity: [1, 0],
          maxHeight: ['200px', '0px'],
          duration: 200,
          easing: 'easeOutQuad',
          complete: () => peekContent.remove()
        });
      } else {
        peekContent.remove();
      }
    }

    if (activeRow) {
      activeRow.classList.remove('quick-peek-active');
    }
    this.quickPeekActive = false;
  }

  // ═══════════════════════════════════════════
  // CONTEXT CARDS (Tippy.js)
  // ═══════════════════════════════════════════

  setupContextCards() {
    // Only setup if Tippy is available and we have author data
    if (typeof tippy === 'undefined') return;
    if (!window.KB_AUTHORS) return;

    document.querySelectorAll('[data-author-id]').forEach(el => {
      const authorId = el.dataset.authorId;
      const author = window.KB_AUTHORS[authorId];
      if (!author) return;

      tippy(el, {
        content: this.createAuthorCard(author),
        allowHTML: true,
        placement: 'bottom-start',
        theme: 'tui',
        animation: 'scale-subtle',
        delay: [300, 100], // 300ms show delay (hover intent)
        interactive: true,
        appendTo: document.body
      });
    });
  }

  createAuthorCard(author) {
    return `
      <div class="context-card">
        <div class="cc-name">${author.name || 'Unknown'}</div>
        <div class="cc-role">${author.perspectiveType || 'Contributor'}</div>
        <div class="cc-details">
          <span class="cc-org">${author.affiliation || 'Independent'}</span>
          <span class="cc-loc">${author.location?.country || ''}</span>
          ${author.yearsInField ? `<span class="cc-exp">${author.yearsInField}y experience</span>` : ''}
        </div>
      </div>
    `;
  }

  // ═══════════════════════════════════════════
  // HELP OVERLAY
  // ═══════════════════════════════════════════

  createHelpOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'tui-help-overlay';
    overlay.className = 'tui-help-overlay';
    overlay.innerHTML = `
      <div class="tui-help-modal">
        <div class="tui-help-header">
          <span class="tui-help-title">Keyboard Shortcuts</span>
          <button class="tui-help-close">×</button>
        </div>
        <div class="tui-help-body">
          <div class="tui-help-section">
            <div class="tui-help-section-title">Navigation</div>
            <div class="tui-help-row"><kbd>j</kbd><span>Next resource</span></div>
            <div class="tui-help-row"><kbd>k</kbd><span>Previous resource</span></div>
            <div class="tui-help-row"><kbd>g g</kbd><span>Jump to top</span></div>
            <div class="tui-help-row"><kbd>G</kbd><span>Jump to bottom</span></div>
          </div>
          <div class="tui-help-section">
            <div class="tui-help-section-title">Actions</div>
            <div class="tui-help-row"><kbd>o</kbd><span>Open resource (new tab)</span></div>
            <div class="tui-help-row"><kbd>Enter</kbd><span>Quick peek</span></div>
            <div class="tui-help-row"><kbd>Space</kbd><span>Quick peek</span></div>
            <div class="tui-help-row"><kbd>Esc</kbd><span>Close / Cancel</span></div>
          </div>
          <div class="tui-help-section">
            <div class="tui-help-section-title">View</div>
            <div class="tui-help-row"><kbd>z</kbd><span>Toggle zen mode</span></div>
            <div class="tui-help-row"><kbd>?</kbd><span>Show this help</span></div>
          </div>
        </div>
        <div class="tui-help-footer">
          Press <kbd>?</kbd> or <kbd>Esc</kbd> to close
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    // Close handlers
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) this.hideHelp();
    });
    overlay.querySelector('.tui-help-close').addEventListener('click', () => {
      this.hideHelp();
    });
  }

  toggleHelp() {
    if (this.helpVisible) {
      this.hideHelp();
    } else {
      this.showHelp();
    }
  }

  showHelp() {
    const overlay = document.getElementById('tui-help-overlay');
    if (!overlay) return;

    overlay.classList.add('visible');
    this.helpVisible = true;

    if (typeof anime !== 'undefined') {
      anime({
        targets: overlay.querySelector('.tui-help-modal'),
        opacity: [0, 1],
        scale: [0.95, 1],
        duration: 200,
        easing: 'easeOutQuad'
      });
    }
  }

  hideHelp() {
    const overlay = document.getElementById('tui-help-overlay');
    if (!overlay) return;

    if (typeof anime !== 'undefined') {
      anime({
        targets: overlay.querySelector('.tui-help-modal'),
        opacity: [1, 0],
        scale: [1, 0.95],
        duration: 150,
        easing: 'easeOutQuad',
        complete: () => {
          overlay.classList.remove('visible');
          this.helpVisible = false;
        }
      });
    } else {
      overlay.classList.remove('visible');
      this.helpVisible = false;
    }
  }

  // ═══════════════════════════════════════════
  // ZEN MODE
  // ═══════════════════════════════════════════

  toggleZenMode() {
    this.zenMode = !this.zenMode;
    document.body.classList.toggle('zen-mode', this.zenMode);

    // Update status if exists
    const statusMode = document.getElementById('status-mode');
    if (statusMode) {
      statusMode.textContent = this.zenMode ? 'ZEN' : 'NORMAL';
    }
  }
}

// ═══════════════════════════════════════════
// BOOT
// ═══════════════════════════════════════════
window.tui = new TUIController();
