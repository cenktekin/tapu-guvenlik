import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the Logo to scroll to top
old_logo = '''<div class="flex items-center space-x-2">
                <span class="text-2xl">🛡️</span>
                <h1 class="text-xl font-bold text-stone-900 tracking-tight">Tapu Güvenlik 2026</h1>
            </div>'''
new_logo = '''<a href="#" onclick="window.scrollTo({top: 0, behavior: 'smooth'}); return false;" class="flex items-center space-x-2 group cursor-pointer">
                <span class="text-2xl group-hover:scale-110 transition-transform">🛡️</span>
                <h1 class="text-xl font-bold text-stone-900 dark:text-stone-50 tracking-tight group-hover:text-amber-600 dark:group-hover:text-amber-500 transition-colors">Tapu Güvenlik 2026</h1>
            </a>'''
html = html.replace(old_logo, new_logo)

if '<h1 class="text-xl font-bold text-stone-900' in html and 'tracking-tight">Tapu Güvenlik 2026</h1>' in html and old_logo not in html:
    # Manual replace if exact whitespace didn't match
    html = re.sub(r'<div class="flex items-center space-x-2">\s*<span class="text-2xl">🛡️</span>\s*<h1 class="text-xl font-bold text-stone-900 tracking-tight">Tapu Güvenlik 2026</h1>\s*</div>', new_logo, html)


# 2. Inject Tailwind Config for Dark Mode
tailwind_script = '<script src="https://cdn.tailwindcss.com"></script>'
tailwind_config = '''<script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
        }
    </script>'''
if 'tailwind.config =' not in html:
    html = html.replace(tailwind_script, tailwind_config)

# 3. Add Dark Mode Toggle to Nav
nav_end = '</nav>'
toggle_button = '''
                <button id="theme-toggle" type="button" class="ml-4 text-stone-500 dark:text-stone-400 hover:bg-stone-100 dark:hover:bg-stone-700 focus:outline-none focus:ring-4 focus:ring-stone-200 dark:focus:ring-stone-700 rounded-lg text-sm p-2.5 transition-colors">
                    <svg id="theme-toggle-dark-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
                    <svg id="theme-toggle-light-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
                </button>
            </nav>'''
if 'id="theme-toggle"' not in html:
    html = html.replace(nav_end, toggle_button)

# 4. Global Dark Mode Classes Injection
# We need to be careful not to double inject.
def replace_class(html_str, old, new):
    if old + ' ' + new.split()[-1] not in html_str and new not in html_str:
        return re.sub(r'\b' + old + r'\b', new, html_str)
    return html_str

html = replace_class(html, 'bg-white', 'bg-white dark:bg-stone-900')
html = replace_class(html, 'bg-stone-50', 'bg-stone-50 dark:bg-stone-950')
html = replace_class(html, 'bg-stone-100', 'bg-stone-100 dark:bg-stone-900') # adjusted for better contrast over stone-950
html = replace_class(html, 'bg-stone-200', 'bg-stone-200 dark:bg-stone-800')
html = replace_class(html, 'text-stone-800', 'text-stone-800 dark:text-stone-200')
html = replace_class(html, 'text-stone-900', 'text-stone-900 dark:text-stone-50')
html = replace_class(html, 'text-stone-600', 'text-stone-600 dark:text-stone-400')
html = replace_class(html, 'text-stone-700', 'text-stone-700 dark:text-stone-300')
html = replace_class(html, 'border-stone-200', 'border-stone-200 dark:border-stone-800')
html = replace_class(html, 'border-stone-300', 'border-stone-300 dark:border-stone-700')
# Exceptions
html = html.replace('text-stone-900 dark:text-stone-50 px-6 py-3', 'text-stone-100 dark:text-stone-900 px-6 py-3') # The black button hero

# 5. Tooltip and Custom CSS dark mode
custom_css = """
        /* Dark Mode overrides for custom CSS */
        .dark .glass-panel {
            background: rgba(28, 25, 23, 0.95); /* stone-900 */
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .dark .tooltip-term:hover {
            color: #fcd34d; /* amber-300 */
            background-color: #78350f; /* amber-900 */
        }
        .dark #global-tooltip {
            background: #e7e5e4; /* stone-200 */
            color: #1c1917; /* stone-900 */
        }
"""
if '.dark .glass-panel' not in html:
    html = html.replace('</style>', custom_css + '\n    </style>')

# 6. Add Theme Toggle JS Logic at the end of body
theme_script = """
    <script>
        // Init theme
        var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
        var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
            if(themeToggleLightIcon) themeToggleLightIcon.classList.remove('hidden');
        } else {
            document.documentElement.classList.remove('dark');
            if(themeToggleDarkIcon) themeToggleDarkIcon.classList.remove('hidden');
        }

        var themeToggleBtn = document.getElementById('theme-toggle');
        if(themeToggleBtn) {
            themeToggleBtn.addEventListener('click', function() {
                // toggle icons
                themeToggleDarkIcon.classList.toggle('hidden');
                themeToggleLightIcon.classList.toggle('hidden');

                // if set via local storage previously
                if (localStorage.getItem('color-theme')) {
                    if (localStorage.getItem('color-theme') === 'light') {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('color-theme', 'dark');
                    } else {
                        document.documentElement.classList.remove('dark');
                        localStorage.setItem('color-theme', 'light');
                    }
                // if NOT set via local storage previously
                } else {
                    if (document.documentElement.classList.contains('dark')) {
                        document.documentElement.classList.remove('dark');
                        localStorage.setItem('color-theme', 'light');
                    } else {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('color-theme', 'dark');
                    }
                }
                
                // Redraw chart if exists
                if(typeof chartInstance !== 'undefined' && chartInstance) {
                    chartInstance.options.scales.x.ticks.color = document.documentElement.classList.contains('dark') ? '#d6d3d1' : '#57534e';
                    chartInstance.options.scales.y.ticks.color = document.documentElement.classList.contains('dark') ? '#d6d3d1' : '#57534e';
                    chartInstance.update();
                }
            });
        }
    </script>
</body>"""
if 'localStorage.getItem(\'color-theme\')' not in html:
    html = html.replace('</body>', theme_script)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Dark Mode & Navigation injection complete!")
