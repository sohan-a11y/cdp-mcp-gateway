from playwright.async_api import Page

JS_TREE_PARSER = """
() => {
    let elementMap = {};
    let counter = 1;

    function isVisible(elem) {
        if (!elem) return false;
        const style = window.getComputedStyle(elem);
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return false;
        const rect = elem.getBoundingClientRect();
        return rect.width > 0 && rect.height > 0;
    }

    function buildTree(node) {
        if (!node || node.nodeType !== Node.ELEMENT_NODE) return "";
        
        const tagName = node.tagName.toLowerCase();
        if (['script', 'style', 'svg', 'noscript', 'head', 'meta', 'link'].includes(tagName)) return "";
        if (node.getAttribute('aria-hidden') === 'true') return "";
        if (!isVisible(node)) return "";

        const isInteractive = ['a', 'button', 'input', 'textarea', 'select', 'details'].includes(tagName) ||
                              node.hasAttribute('onclick') ||
                              node.getAttribute('role') === 'button' ||
                              node.getAttribute('contenteditable') === 'true';

        let idTag = "";
        let selector = "";

        if (isInteractive) {
            const eid = "e" + counter++;
            idTag = `[${eid}] `;
            
            if (node.id) {
                selector = `#${node.id}`;
            } else if (node.name) {
                selector = `${tagName}[name="${node.name}"]`;
            } else {
                selector = `${tagName}:nth-of-type(${Array.from(node.parentNode.children).indexOf(node) + 1})`;
            }
            elementMap[eid] = selector;
        }

        let directText = "";
        for (let child of node.childNodes) {
            if (child.nodeType === Node.TEXT_NODE) {
                const text = child.textContent.trim();
                if (text) directText += text + " ";
            }
        }
        directText = directText.trim();

        let childrenText = "";
        for (let child of node.children) {
            const childResult = buildTree(child);
            if (childResult) childrenText += childResult + "\n";
        }

        if (isInteractive) {
            let label = directText || node.getAttribute('placeholder') || node.getAttribute('aria-label') || node.value || tagName;
            return `${idTag}<${tagName}> ${label}`.trim();
        }

        if (directText && !childrenText) {
            return directText;
        }

        return childrenText.trim();
    }

    const treeText = buildTree(document.body);
    return {
        tree: treeText,
        map: elementMap,
        title: document.title
    };
}
"""

async def extract_clean_accessibility_tree(page: Page) -> dict:
    result = await page.evaluate(JS_TREE_PARSER)
    return result
