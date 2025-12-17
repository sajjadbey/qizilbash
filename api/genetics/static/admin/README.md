# Admin Static Files

## Markdown Editor

The blog post content field in the Django admin panel uses **EasyMDE** (Easy Markdown Editor) for a rich editing experience.

### Features:
- **Bold**, *Italic*, and other text formatting
- Headers (H1-H6)
- Lists (ordered and unordered)
- Links and images
- Code blocks and inline code
- Tables
- Blockquotes
- Live preview and side-by-side editing
- Fullscreen mode
- Auto-save functionality
- Word and line count

### Implementation:
- **CSS**: Loaded from CDN (https://cdn.jsdelivr.net/npm/easymde@2.18.0/dist/easymde.min.css)
- **JavaScript**: Loaded from CDN (https://cdn.jsdelivr.net/npm/easymde@2.18.0/dist/easymde.min.js)
- **Custom JS**: `js/markdown_editor.js` initializes the editor

### Usage:
The editor is automatically initialized for the blog post content field when you create or edit a blog post in the admin panel.

### Markdown Syntax Guide:
Available via the "?" (guide) button in the editor toolbar.