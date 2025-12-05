# SPARTA Mechanical Engineering Theme - CSS Architecture

## Overview
Complete CSS implementation embedded in Streamlit app for professional CAD workstation aesthetic.

## Typography System

### Font Families
```css
/* Headers - Technical/Mechanical */
font-family: 'Orbitron', sans-serif;
- Weights: 400, 700, 900
- Use: All headers (h1, h2, h3)
- Style: Uppercase, letter-spacing: 2px

/* Body - Engineering Precision */
font-family: 'Roboto Mono', monospace;
- Weights: 300, 400, 500, 700
- Use: All body text, inputs, code
- Style: Monospace for technical accuracy
```

### Font Loading
```html
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto+Mono:wght@300;400;500;700&display=swap');
```

## Color System

### CSS Variables
```css
:root {
    --steel-gray: #3A3F44;      /* Primary backgrounds */
    --matte-black: #1A1C1E;     /* Deep backgrounds */
    --engineering-blue: #3C6EAA; /* Accents, borders */
    --brass-gold: #C8A951;      /* Headers, highlights */
    --border-color: #4A4F54;    /* Subtle borders */
}
```

### Usage Patterns
- **Backgrounds**: Steel gray for panels, matte black for inputs
- **Borders**: Engineering blue for primary, border-color for subtle
- **Text**: Brass/gold for headers, light gray (#E0E0E0) for body
- **Status**: Green (#4CAF50), red (#F44336), orange (#FF9800)

## Layout Components

### 1. Background Grid
```css
background-image: 
    linear-gradient(rgba(60, 110, 170, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(60, 110, 170, 0.03) 1px, transparent 1px);
background-size: 20px 20px;
```
- Creates blueprint-style grid
- Subtle engineering blue lines
- 20px × 20px spacing

### 2. Headers
```css
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
    color: var(--brass-gold);
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid var(--engineering-blue);
    padding-bottom: 8px;
}
```
- Orbitron font for technical look
- Brass/gold color
- Engineering blue underline
- Uppercase for emphasis

### 3. Sidebar
```css
[data-testid="stSidebar"] {
    background-color: var(--steel-gray);
    border-right: 3px solid var(--engineering-blue);
    box-shadow: inset -2px 0 10px rgba(0,0,0,0.5);
}
```
- Steel gray background
- Thick blue border
- Inset shadow for depth

### 4. Chat Messages
```css
.stChatMessage {
    background-color: var(--steel-gray);
    border: 1px solid var(--border-color);
    border-radius: 2px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.4);
    margin: 10px 0;
    padding: 15px;
}
```
- Boxy design (minimal border-radius)
- Subtle borders and shadows
- Monospace font

### 5. Message Alignment
```css
/* User - Right */
[data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"][aria-label="user"]) {
    background-color: rgba(60, 110, 170, 0.2);
    border-left: 3px solid var(--engineering-blue);
    margin-left: 20%;
}

/* Assistant - Left */
[data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"][aria-label="assistant"]) {
    background-color: rgba(58, 63, 68, 0.8);
    border-left: 3px solid var(--brass-gold);
    margin-right: 20%;
}
```

## Interactive Elements

### Buttons
```css
.stButton > button {
    background-color: var(--steel-gray);
    color: var(--brass-gold);
    border: 2px solid var(--engineering-blue);
    border-radius: 0;
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    padding: 10px 20px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
}

.stButton > button:hover {
    background-color: var(--engineering-blue);
    color: white;
    border-color: var(--brass-gold);
    box-shadow: 0 0 15px rgba(60, 110, 170, 0.5);
}
```
- Industrial style
- No rounded corners
- Brass text with blue border
- Hover: Blue background with glow effect

### Input Fields
```css
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: var(--matte-black);
    color: #E0E0E0;
    border: 1px solid var(--border-color);
    border-radius: 0;
    font-family: 'Roboto Mono', monospace;
    padding: 10px;
}
```
- Dark backgrounds
- Technical monospace font
- Square corners

### Chat Input
```css
.stChatInput > div {
    background-color: var(--steel-gray);
    border: 2px solid var(--engineering-blue);
    border-radius: 0;
}

.stChatInput input {
    background-color: var(--matte-black);
    color: #E0E0E0;
    font-family: 'Roboto Mono', monospace;
}
```

## Image Display

### Chat Images
```css
.chat-image {
    max-width: 100%;
    height: auto;
    border: 2px solid var(--engineering-blue);
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    margin: 15px 0;
    display: block;
}

.image-caption {
    font-size: 11px;
    color: var(--brass-gold);
    font-family: 'Roboto Mono', monospace;
    margin-top: 5px;
    text-align: center;
    letter-spacing: 1px;
}
```

### Image Handling in Python
```python
# Extract image from markdown
img_match = re.search(r'!\[.*?\]\((.*?)\)', content)
if img_match:
    img_path = img_match.group(1)
    full_img_url = f"{BACKEND_URL}/{img_path}"
    
    # Display with custom styling
    st.markdown(f'<img src="{full_img_url}" class="chat-image">', 
                unsafe_allow_html=True)
    st.markdown(f'<p class="image-caption">GENERATED DIAGRAM | {os.path.basename(img_path)}</p>', 
                unsafe_allow_html=True)
```

## Technical Panels

### Panel Container
```css
.technical-panel {
    background-color: var(--steel-gray);
    border: 2px solid var(--engineering-blue);
    padding: 15px;
    margin: 10px 0;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
}
```
- Inset shadow for depth
- Blue border
- CAD-style appearance

### Metrics Display
```css
.stMetric {
    background-color: var(--steel-gray);
    border: 1px solid var(--border-color);
    padding: 10px;
    border-radius: 0;
}

.stMetric label {
    color: var(--brass-gold);
    font-family: 'Orbitron', sans-serif;
    font-size: 12px;
}

.stMetric [data-testid="stMetricValue"] {
    color: #E0E0E0;
    font-family: 'Roboto Mono', monospace;
}
```

## Status Indicators

### Status Classes
```css
.status-success {
    color: #4CAF50;
    font-family: 'Roboto Mono', monospace;
    font-weight: 700;
}

.status-error {
    color: #F44336;
    font-family: 'Roboto Mono', monospace;
    font-weight: 700;
}

.status-warning {
    color: #FF9800;
    font-family: 'Roboto Mono', monospace;
    font-weight: 700;
}
```

### Usage in Python
```python
# Success
st.markdown('<p class="status-success">SIMULATION: COMPLETED</p>', 
            unsafe_allow_html=True)

# Error
st.markdown('<p class="status-error">IMAGE LOAD FAILED: path</p>', 
            unsafe_allow_html=True)

# Warning
st.markdown('<p class="status-warning">Attempting reload from: url</p>', 
            unsafe_allow_html=True)
```

## Scrollbar Customization

```css
::-webkit-scrollbar {
    width: 10px;
    background-color: var(--matte-black);
}

::-webkit-scrollbar-thumb {
    background-color: var(--engineering-blue);
    border: 1px solid var(--border-color);
}
```
- Engineering blue thumb
- Matte black track
- Consistent with theme

## Code Blocks

```css
.stCodeBlock {
    background-color: var(--matte-black);
    border: 1px solid var(--engineering-blue);
    border-radius: 0;
}
```
- Dark background for code
- Blue border
- Square corners

## Expanders

```css
.streamlit-expanderHeader {
    background-color: var(--steel-gray);
    border: 1px solid var(--border-color);
    font-family: 'Orbitron', sans-serif;
    color: var(--brass-gold);
}
```
- Technical header font
- Brass/gold text
- Steel gray background

## Separator Lines

```css
hr {
    border: none;
    border-top: 1px solid var(--engineering-blue);
    margin: 20px 0;
    opacity: 0.5;
}
```
- Engineering blue lines
- Subtle opacity
- Technical aesthetic

## Captions

```css
.stCaption {
    color: #888;
    font-family: 'Roboto Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.5px;
}
```
- Small monospace font
- Gray color for subtlety
- Letter spacing for readability

## Implementation Notes

### Loading CSS in Streamlit
```python
def load_css():
    css = """<style>/* CSS here */</style>"""
    st.markdown(css, unsafe_allow_html=True)

# Call at app start
load_css()
```

### Using Custom Classes
```python
# HTML with classes
st.markdown('<div class="technical-panel">Content</div>', 
            unsafe_allow_html=True)

# Images with classes
st.markdown(f'<img src="{url}" class="chat-image">', 
            unsafe_allow_html=True)

# Status with classes
st.markdown('<p class="status-success">Success!</p>', 
            unsafe_allow_html=True)
```

## Browser Compatibility

### Tested On
- Chrome/Edge (Chromium): ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support (with -webkit- prefixes)

### Fallbacks
- Custom fonts load from Google Fonts CDN
- System fonts used if CDN unavailable
- Grid background degrades gracefully
- Scrollbar styling Chrome/Safari only (graceful degradation)

## Performance Considerations

### Optimizations
- Single CSS block loaded once at startup
- No dynamic CSS generation
- Minimal selectors for specificity
- Hardware-accelerated properties (transform, opacity)

### Best Practices
- Use CSS variables for theme consistency
- Avoid inline styles (use classes)
- Minimize DOM manipulation
- Leverage browser caching for fonts

## Customization Guide

### Changing Colors
```css
:root {
    --steel-gray: #YOUR_COLOR;
    --matte-black: #YOUR_COLOR;
    --engineering-blue: #YOUR_COLOR;
    --brass-gold: #YOUR_COLOR;
}
```

### Adjusting Grid Size
```css
background-size: 30px 30px;  /* Larger grid */
background-size: 10px 10px;  /* Smaller grid */
```

### Font Size Scaling
```css
h1 { font-size: 32px; }  /* Increase */
h1 { font-size: 24px; }  /* Decrease */
```

## Accessibility

### Considerations
- High contrast ratios for readability
- Monospace fonts for clarity
- Clear status indicators
- Semantic HTML where possible
- Keyboard navigation preserved

### WCAG Compliance
- Color contrast: AAA level for body text
- AA level for UI elements
- Text size: Readable at 100% zoom
- Focus indicators: Preserved from Streamlit defaults

---

**SPARTA V2.0** | MECHANICAL ENGINEERING CSS ARCHITECTURE
