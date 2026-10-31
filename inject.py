import json
import re

with open('dictionary.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

# Sort dictionary by word length DESC to avoid partial matches (e.g. matching "Ada" inside "Adam") during text replacement
# And filter out single-letter entries or garbage
filtered_dict = {k: v for k, v in dictionary.items() if len(k) > 2 and '' not in k}

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS
css_to_add = """
        /* Glossary Tooltip */
        .tooltip-term {
            border-bottom: 2px dotted #D97706;
            cursor: help;
            color: #b45309;
            font-weight: 600;
            transition: color 0.2s;
        }
        .tooltip-term:hover {
            color: #D97706;
            background-color: #fef3c7;
        }
        #global-tooltip {
            position: absolute;
            background: #292524;
            color: #f5f5f4;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.4;
            max-width: 300px;
            z-index: 99999;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s ease, transform 0.2s ease;
            transform: translateY(5px);
            display: none;
        }
        #global-tooltip.show {
            opacity: 1;
            transform: translateY(0);
            display: block;
        }
        
        .glossary-item {
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #e7e5e4;
            background: #fafaf9;
            transition: all 0.2s;
        }
        .glossary-item:hover {
            border-color: #fcd34d;
            background: #fffbeb;
        }
"""
html = html.replace('</style>', css_to_add + '</style>')

# 2. Add Glossary Link in Navigation
nav_link = '<a href="#glossary" class="hover:text-amber-600 transition">Sözlük</a>\n                <a href="#workflow"'
html = html.replace('<a href="#workflow"', nav_link)

# 3. Add HTML Section
html_section = """
        <!-- Glossary Section -->
        <section id="glossary" class="scroll-mt-24 pb-8">
            <div class="mb-8 text-center md:text-left">
                <h3 class="text-xl font-bold text-stone-800 mb-2">Tapu ve Emlak Sözlüğü</h3>
                <p class="text-stone-600">Karışık hukuki terimlerin ne anlama geldiğini öğrenin.</p>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
                <input type="text" id="glossarySearch" placeholder="Terim ara (örn. İfraz, İpotek)..." class="w-full px-4 py-3 rounded-lg border border-stone-300 focus:ring-2 focus:ring-amber-500 mb-6 bg-stone-50 transition outline-none text-stone-800 placeholder-stone-400">
                <div id="glossaryList" class="grid md:grid-cols-2 lg:grid-cols-3 gap-4 h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                    <!-- JS will populate -->
                </div>
            </div>
        </section>

        <!-- Final Checklist Section -->"""
html = html.replace('<!-- Final Checklist Section -->', html_section)

# 4. Add global tooltip div
tooltip_div = '\n    <div id="global-tooltip"></div>\n    <script>'
html = html.replace('<script>', tooltip_div, 1)

# 5. Add JS Logic
js_code = f"""
        const dictData = {json.dumps(filtered_dict, ensure_ascii=False)};
        
        function initGlossary() {{
            const listContainer = document.getElementById('glossaryList');
            const searchInput = document.getElementById('glossarySearch');
            
            // Populate list
            const renderList = (filter = '') => {{
                listContainer.innerHTML = '';
                const termKeys = Object.keys(dictData).sort();
                let count = 0;
                termKeys.forEach(term => {{
                    if (term.toLowerCase().includes(filter.toLowerCase()) || 
                        dictData[term].toLowerCase().includes(filter.toLowerCase())) {{
                        const div = document.createElement('div');
                        div.className = 'glossary-item flex flex-col gap-1';
                        div.innerHTML = `<strong class="text-amber-700">` + term + `</strong><span class="text-sm text-stone-600">` + dictData[term] + `</span>`;
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
                        const key = Object.keys(dictData).find(k => k.toLowerCase() === term.toLowerCase());
                        if (key) def = dictData[key];
                    }}
                    if (def) {{
                        tooltip.innerHTML = `<strong class="block mb-1 text-amber-500">` + term + `</strong>` + def;
                        tooltip.classList.add('show');
                        
                        // positioning
                        const rect = e.target.getBoundingClientRect();
                        let top = rect.top + window.scrollY - tooltip.offsetHeight - 10;
                        let left = rect.left + window.scrollX + (rect.width/2) - (tooltip.offsetWidth/2);
                        
                        // boundary checks
                        if (top < window.scrollY) top = rect.bottom + window.scrollY + 10;
                        if (left < 0) left = 10;
                        if (left + tooltip.offsetWidth > window.innerWidth) left = window.innerWidth - tooltip.offsetWidth - 10;
                        
                        tooltip.style.top = top + 'px';
                        tooltip.style.left = left + 'px';
                    }}
                }}
            }});
            
            document.body.addEventListener('mouseout', (e) => {{
                if (e.target.classList.contains('tooltip-term')) {{
                    tooltipTimeout = setTimeout(() => {{
                        tooltip.classList.remove('show');
                    }}, 100);
                }}
            }});
        }}
        
        function highlightTermsInText() {{
            const terms = Object.keys(dictData).filter(k => k.length > 3).sort((a,b) => b.length - a.length);
            
            // Create a regex to match any of the terms as whole words
            // Escape terms for regex
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
            
            // Start walking from the workflow section to avoid touching header/hero unless needed
            // Actually, let's just do main content
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

print("Injected UI, CSS, and JS into index.html")
