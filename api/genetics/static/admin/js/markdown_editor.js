// Initialize EasyMDE Markdown Editor for blog content
document.addEventListener('DOMContentLoaded', function() {
    const contentTextarea = document.querySelector('textarea.markdown-editor');
    
    if (contentTextarea) {
        const easyMDE = new EasyMDE({
            element: contentTextarea,
            autofocus: false,
            autosave: {
                enabled: true,
                uniqueId: "blog_post_content",
                delay: 1000,
            },
            spellChecker: false,
            placeholder: "Write your blog post content in Markdown...",
            toolbar: [
                "bold", "italic", "heading", "|",
                "quote", "unordered-list", "ordered-list", "|",
                "link", "image", "|",
                "code", "table", "|",
                "preview", "side-by-side", "fullscreen", "|",
                "guide"
            ],
            status: ["autosave", "lines", "words", "cursor"],
            renderingConfig: {
                singleLineBreaks: false,
                codeSyntaxHighlighting: true,
            },
            previewRender: function(plainText) {
                // Custom preview rendering if needed
                return this.parent.markdown(plainText);
            },
            minHeight: "400px",
        });
    }
});