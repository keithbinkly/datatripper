# KB Topic Page Styling Standardization Plan

## Objective
Standardize all knowledge base topic pages to match the `knowledge-engineering.html` template styling.

---

## Template Analysis: knowledge-engineering.html

### Font Stack
```css
font-family: 'IBM Plex Sans', -apple-system, sans-serif;  /* Body */
font-family: 'JetBrains Mono', monospace;  /* Code/monospace elements */
```
**Google Fonts link:**
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

### CSS Variables (Color Palette)
```css
:root {
  --bg-base: #0a0a0a;
  --bg-surface: #0f0f0f;
  --bg-elevated: #161616;
  --bg-hover: #1c1c1c;

  --border-dim: #252525;
  --border-mid: #333;
  --border-bright: #444;
  --border-accent: #5ccfe6;

  --text-dim: #666;
  --text-mid: #999;
  --text-bright: #ccc;
  --text-white: #f0f0f0;

  --cyan: #5ccfe6;
  --orange: #ffab70;
  --green: #87c38a;
  --purple: #c9a0dc;
  --amber: #d4a84b;
  --red: #e06c75;

  --font-xs: 0.75rem;    /* 12px */
  --font-sm: 0.8125rem;  /* 13px */
  --font-base: 0.875rem; /* 14px */
  --font-md: 1rem;       /* 16px */
  --font-lg: 1.125rem;   /* 18px */
  --font-xl: 1.25rem;    /* 20px */
}
```

### Key Structural Components

1. **Header** - ASCII-bordered header with back/next navigation, topic indicator dot, brand title, resource count, stats toggle, and clock
2. **Main Grid** - 3-column layout: Context Panel (560px) | Resources Panel (flex) | Insights Panel (300px)
3. **Panel Component** - Reusable panel with ASCII borders top/bottom, header with icon, and body
4. **Context Panel** (Left) - Lede text, stat boxes, key terms, category description pane with tabs
5. **Resources Panel** (Center) - Scrollable list with collapsible category sections, single-row resource items
6. **Insights Panel** (Right) - Optional stats panel, toggleable
7. **Resource Card Popup** - TUI-styled modal card on resource click
8. **Lightbox** - For image/PDF expansion

### External Libraries
```html
<script src="https://unpkg.com/@popperjs/core@2"></script>
<script src="https://unpkg.com/tippy.js@6"></script>
<script src="https://unpkg.com/animejs@3.2.1/lib/anime.min.js"></script>
<script src="https://unpkg.com/lucide@latest"></script>
```

---

## Pages Requiring Updates

### Priority 1: Main Topic Pages
| Page | Current Style | Accent Color |
|------|---------------|--------------|
| `data-engineering.html` | External CSS (styles.css) + Inter font | `#f97316` (orange) |
| `design-craft.html` | External CSS (styles.css) + Inter font | `#8b5cf6` (purple) |
| `personal-growth.html` | External CSS (styles.css) + Inter font | `#10b981` (green) |

### Priority 2: Terminal Stack & Tools
| Page | Current Style | Notes |
|------|---------------|-------|
| `terminal-stack.html` | Inline (Outfit font, card-based) | Tool showcase, different purpose |
| `tools/claude.html` | Unknown - needs review | May use broken CSS path |
| `tools/ghostty.html` | Unknown | |
| `tools/lazygit.html` | Unknown | |
| `tools/nvim.html` | Unknown | |
| `tools/opencode.html` | Unknown | |
| `tools/terminal.html` | Unknown | |
| `tools/tmux.html` | Unknown | |

---

## Implementation Steps

### Step 1: Extract Template CSS
- Copy the complete `<style>` block from `knowledge-engineering.html` (lines 14-1400+)
- Save as reference file or create shared CSS file

### Step 2: Update data-engineering.html
1. Replace font link (Inter → IBM Plex Sans)
2. Remove external styles.css link
3. Add inline `<style>` block from template
4. Update accent color variable: `--cyan` references → use `#f97316` (orange) for topic-specific elements
5. Restructure HTML to match template layout:
   - ASCII border header
   - 3-column main grid
   - Panel components with ASCII borders
   - Category tabs with descriptions
   - Resource rows (grid-based, not flex)
   - Resource card popup system
6. Add JavaScript for:
   - Clock update
   - Stats toggle
   - Category collapse/expand
   - Resource card popup
   - Lightbox

### Step 3: Update design-craft.html
- Same process as Step 2
- Accent color: `#8b5cf6` (purple)

### Step 4: Update personal-growth.html
- Same process as Step 2
- Accent color: `#10b981` (green)

### Step 5: Review terminal-stack.html
- Determine if this should match topic page style or remain as tool showcase
- If updating: follow same process with tool-specific accent colors

### Step 6: Review tools/*.html pages
- Audit current structure
- Determine if these are sub-pages that should match parent style
- Fix any broken CSS paths

---

## Key Differences to Address

### Current (data-engineering.html, etc.)
```html
<header class="topic-header">
  <a href="../index.html" class="topic-back">&larr;</a>
  <span class="topic-indicator" style="background: #f97316"></span>
  <h1 class="topic-title">Data Engineering</h1>
  <span class="topic-count">86 resources</span>
</header>
```

### Target (knowledge-engineering.html)
```html
<div class="header">
  <div class="ascii-border">╔═══════════════════════════...</div>
  <div class="header-content">
    <div class="header-left">
      <a href="../index.html" class="back-link">←</a>
      <div class="topic-indicator"></div>
      <span class="brand">Knowledge Engineering</span>
      <span class="resource-count">XX resources</span>
    </div>
    <div class="header-right">
      <button class="stats-toggle" id="statsToggle">stats</button>
      <span class="clock" id="clock">--:--</span>
      <a href="next-page.html" class="next-link">→</a>
    </div>
  </div>
  <div class="ascii-border">╚═══════════════════════════...</div>
</div>
```

### Current Resource Link
```html
<a href="..." class="tlink">
  <span class="tlink-dot" style="background:#f97316"></span>
  <span class="tlink-src">dbt Blog</span>
  <span class="tlink-title">Title Here</span>
  <span class="tlink-author">Author</span>
  <span class="tlink-time">15m</span>
  <span class="tlink-desc">Description...</span>
</a>
```

### Target Resource Row
```html
<div class="resource-row" data-url="..." data-title="..." data-source="..." ...>
  <span class="resource-tree">├─</span>
  <span class="resource-dot" style="background: var(--cyan)"></span>
  <span class="resource-title">Title Here</span>
  <span class="resource-source">SOURCE</span>
  <span class="resource-author">Author</span>
  <span class="resource-time">15m</span>
  <span class="resource-arrow">→</span>
</div>
```

---

## Estimated Scope

| Task | Files | Complexity |
|------|-------|------------|
| Extract & document template | 1 | Low |
| Update data-engineering.html | 1 | High (restructure + 86 resources) |
| Update design-craft.html | 1 | High (restructure + 24 resources) |
| Update personal-growth.html | 1 | High (restructure + 52 resources) |
| Review terminal-stack.html | 1 | Medium |
| Review tools/*.html | 7 | Medium |

---

## Success Criteria

1. All topic pages use IBM Plex Sans + JetBrains Mono fonts
2. All pages use inline CSS with consistent variable naming
3. All pages have ASCII-bordered headers and panels
4. All pages have 3-column grid layout (responsive)
5. All resource items use grid-based single-row layout
6. All pages have functional resource card popups
7. All pages have working stats toggle
8. Mobile responsiveness verified on all pages
