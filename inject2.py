import json
import re

# 1. Load dictionary data
with open('dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

# Sort dictionary by word length DESC to avoid partial matches (e.g. matching "Ada" inside "Adam") during text replacement
# And filter out single-letter entries or garbage
filtered_dict = {k: v for k, v in dictionary.items() if len(k) > 2 and '' not in k}

# 2. Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 3. Clean up previous injections to avoid duplication
html = re.sub(r'\s*/\* Glossary Tooltip \*/.*?(?=</style>)', '\n    ', html, flags=re.DOTALL)
html = re.sub(r'<a href="#glossary"[^>]*>Sözlük</a>\s*', '', html)
html = re.sub(r'\s*<!-- Glossary Section -->.*?<!-- Final Checklist Section -->', '\n\n        <!-- Final Checklist Section -->', html, flags=re.DOTALL)
html = re.sub(r'\s*<div id="global-tooltip"></div>\s*<script>', '\n\n    <script>', html)
html = re.sub(r'\s*const dictData = \{.*?(?=// Re-wrap original DOMContentLoaded)', '', html, flags=re.DOTALL)
html = html.replace('// Re-wrap original DOMContentLoaded\n        document.addEventListener(\'DOMContentLoaded\', () => {', 'document.addEventListener(\'DOMContentLoaded\', () => {')


# 4. Inject new CSS
css_to_add = """
        /* Glossary Tooltip */
        .tooltip-term {
            border-bottom: 2px dotted #D97706;
            cursor: help;
            color: #b45309;
            font-weight: 600;
            transition: color 0.2s, background-color 0.2s;
        }
        .tooltip-term:hover {
            color: #D97706;
            background-color: #fef3c7;
        }
        #global-tooltip {
            position: absolute;
            background: #292524;
            color: #f5f5f4;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.5;
            max-width: 320px;
            z-index: 99999;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease, transform 0.3s ease;
            transform: translateY(10px) scale(0.95);
            display: none;
        }
        #global-tooltip.show {
            opacity: 1;
            transform: translateY(0) scale(1);
            display: block;
        }
        
        /* New Animated Glossary Item */
        .glossary-item {
            transition: all 0.2s ease;
            border-bottom: none !important; /* override global tooltip-term */
        }
        .glossary-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
"""
html = html.replace('</style>', css_to_add + '</style>')

# 5. Inject Nav Link
nav_link = '<a href="#glossary" class="hover:text-amber-600 transition">Sözlük</a>\n                <a href="#workflow"'
html = html.replace('<a href="#workflow"', nav_link)

# 6. Inject HTML Section
html_section = """
        <!-- Glossary Section -->
        <section id="glossary" class="scroll-mt-24 pb-8">
            <div class="mb-8 text-center md:text-left">
                <h3 class="text-xl font-bold text-stone-800 mb-2">Tapu ve Emlak Sözlüğü</h3>
                <p class="text-stone-600">Terimlerin ne anlama geldiğini öğrenmek için üzerlerine gelin.</p>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
                <input type="text" id="glossarySearch" placeholder="Terim ara (örn. İfraz, İpotek)..." class="w-full px-4 py-3 rounded-lg border border-stone-300 focus:ring-2 focus:ring-amber-500 mb-6 bg-stone-50 transition outline-none text-stone-800 placeholder-stone-400">
                <div id="glossaryList" class="flex flex-wrap gap-3 h-[300px] overflow-y-auto pr-2 custom-scrollbar content-start">
                    <!-- JS will populate -->
                </div>
            </div>
        </section>

        <!-- Final Checklist Section -->"""
html = html.replace('<!-- Final Checklist Section -->', html_section)

# 7. Inject Tooltip Div
tooltip_div = '\n    <div id="global-tooltip"></div>\n    <script>'
html = html.replace('<script>', tooltip_div, 1)

# 8. Inject new JS
js_code = f"""
        const dictData = {json.dumps(filtered_dict, ensure_ascii=False)};
        
        function initGlossary() {{
            const listContainer = document.getElementById('glossaryList');
            const searchInput = document.getElementById('glossarySearch');
            
            // Populate list
            const renderList = (filter = '') => {{
                listContainer.innerHTML = '';
                
                // Sort keys alphabetically using Turkish locale
                const termKeys = Object.keys(dictData).sort((a, b) => a.localeCompare(b, 'tr'));
                
                let count = 0;
                termKeys.forEach(term => {{
                    // Filter using Turkish locale lowercase
                    const termLower = term.toLocaleLowerCase('tr');
                    const filterLower = filter.toLocaleLowerCase('tr');
                    const defLower = dictData[term].toLocaleLowerCase('tr');
                    
                    if (termLower.includes(filterLower) || defLower.includes(filterLower)) {{
                        const div = document.createElement('div');
                        div.className = 'glossary-item tooltip-term px-4 py-2 bg-stone-100 border border-stone-200 rounded-full text-sm font-semibold text-stone-700 cursor-help select-none';
                        div.setAttribute('data-term', term);
                        div.textContent = term;
                        listContainer.appendChild(div);
                        count++;
                    }}
                }});
                if (count === 0) {{
                    listContainer.innerHTML = '<p class="text-stone-500 italic p-4">Sonuç bulunamadı.</p>';
                }}
            }};
            
            renderList();
            
            searchInput.addEventListener('input', (e) => {{
                renderList(e.target.value);
            }});
            
            // Tooltip logic
            const tooltip = document.getElementById('global-tooltip');
            let tooltipTimeout;
            
            document.body.addEventListener('mouseover', (e) => {{
                if (e.target.classList.contains('tooltip-term')) {{
                    clearTimeout(tooltipTimeout);
                    const term = e.target.getAttribute('data-term');
                    let def = dictData[term];
                    // Also try case-insensitive match if exact fails
                    if (!def) {{
                        const key = Object.keys(dictData).find(k => k.toLocaleLowerCase('tr') === term.toLocaleLowerCase('tr'));
                        if (key) def = dictData[key];
                    }}
                    if (def) {{
                        tooltip.innerHTML = `<strong class="block mb-2 text-amber-500 font-bold border-b border-stone-700 pb-1">` + term + `</strong>` + def;
                        tooltip.classList.add('show');
                        
                        // positioning
                        const rect = e.target.getBoundingClientRect();
                        let top = rect.top + window.scrollY - tooltip.offsetHeight - 14;
                        let left = rect.left + window.scrollX + (rect.width/2) - (tooltip.offsetWidth/2);
                        
                        // boundary checks
                        if (top < window.scrollY) top = rect.bottom + window.scrollY + 14;
                        if (left < 10) left = 10;
                        if (left + tooltip.offsetWidth > window.innerWidth - 10) left = window.innerWidth - tooltip.offsetWidth - 10;
                        
                        tooltip.style.top = top + 'px';
                        tooltip.style.left = left + 'px';
                    }}
                }}
            }});
            
            document.body.addEventListener('mouseout', (e) => {{
                if (e.target.classList.contains('tooltip-term')) {{
                    tooltipTimeout = setTimeout(() => {{
                        tooltip.classList.remove('show');
                    }}, 150);
                }}
            }});
        }}
        
        function highlightTermsInText() {{
            const terms = Object.keys(dictData).filter(k => k.length > 3).sort((a,b) => b.length - a.length);
            
            // Create a regex to match any of the terms as whole words
            const escapeRegExp = (string) => string.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
            const pattern = new RegExp('\\\\b(' + terms.map(escapeRegExp).join('|') + ')\\\\b', 'gi');
            
            const excludeTags = ['SCRIPT', 'STYLE', 'NOSCRIPT', 'IFRAME', 'OBJECT', 'INPUT', 'TEXTAREA', 'BUTTON'];
            
            function walkTextNodes(node) {{
                if (node.nodeType === 3) {{ // Text node
                    const text = node.nodeValue;
                    if (text.trim().length > 0) {{
                        // Prevent matching if parent is already a tooltip or inside glossary
                        let isInsideGlossary = false;
                        let curr = node.parentNode;
                        while(curr && curr.tagName !== 'BODY') {{
                            if (curr.id === 'glossary' || curr.classList.contains('tooltip-term')) {{
                                isInsideGlossary = true; break;
                            }}
                            curr = curr.parentNode;
                        }}
                        
                        if (!isInsideGlossary && pattern.test(text)) {{
                            const span = document.createElement('span');
                            span.innerHTML = text.replace(pattern, (match) => `<span class="tooltip-term" data-term="${{match.toUpperCase()}}">${{match}}</span>`);
                            node.parentNode.replaceChild(span, node);
                        }}
                    }}
                }} else if (node.nodeType === 1) {{ // Element node
                    if (!excludeTags.includes(node.tagName)) {{
                        // Convert childNodes to array before iterating since we might modify it
                        Array.from(node.childNodes).forEach(walkTextNodes);
                    }}
                }}
            }}
            
            const mainContent = document.querySelector('main');
            if (mainContent) walkTextNodes(mainContent);
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            highlightTermsInText();
            initGlossary();
        }});
"""

html = html.replace("document.addEventListener('DOMContentLoaded', () => {", js_code + "\n        // Re-wrap original DOMContentLoaded\n        document.addEventListener('DOMContentLoaded', () => {")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Injected new V2 UI, CSS, and JS into index.html")
