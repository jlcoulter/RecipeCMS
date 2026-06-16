"""Page layout templates - opener, header, footer."""

from datetime import datetime


def get_opener(config, formatter):
    """Generate the HTML opener: DOCTYPE, head open, meta, CSS links, custom header."""
    font_links = ""
    for font in config.fonts:
        font_links += f"""
                <link rel="preconnect" href="{font.get('preconnect', '')}">
                <link rel="preconnect" href="{font.get('preconnect_crossorigin', '')}" crossorigin>
                <link href="{font.get('css_url', '')}" rel="stylesheet">"""

    custom_css_link = ""
    if True:  # Always check for custom.css at build time; include link if it might exist
        custom_css_link = f'\n                <link rel="stylesheet" href="{config.site_url}/custom.css">'

    return f"""
        <!DOCTYPE html>
        <html lang="en-US">
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />
                {font_links}
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
                <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
                <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
                <link rel="manifest" href="/site.webmanifest">
                <link rel="stylesheet" href="{config.site_url}/style.css">{custom_css_link}
                <script type="text/javascript" src="{config.site_url}/random.js"></script>
                {config.custom_header_html}
        """


def get_header(config, formatter):
    """Generate the header: closing head, body open, nav bar."""
    return f"""
        </head>
        <body onLoad="random()">
            <div id="head">
                <div class="keywords border">
                    <a href="{formatter.format_link(f'{config.site_url}/index.html')}">
                        <p>Home</p>
                    </a>
                </div>
                <div class="keywords border">
                    <a href="{formatter.format_link(f'{config.site_url}/about.html')}">
                        <p>About</p>
                    </a>
                </div>
                <div class="keywords border">
                    <a href="{formatter.format_link(f'{config.site_url}/search.html')}">
                        <p>Search</p>
                    </a>
                </div>
                <div class="keywords random border">
                    <a>
                        <p>Random</p>
                    </a>
                </div>
            </div>
        <div id="body">"""


def get_footer(config, formatter):
    """Generate the footer: nav links, copyright."""
    return f"""
        </div>
        <footer>
            <div id="foot">
                <div class="keywords border">
                    <a href="{formatter.format_link(f'{config.site_url}/all_items.html')}">
                        <p>All {config.item_name_plural}</p>
                    </a>
                </div>
                <div class="keywords border">
                    <a href="{formatter.format_link(f'{config.site_url}/all_keywords.html')}">
                        <p>All Keywords</p>
                    </a>
                </div>
                <div class="keywords border">
                    <a href="{formatter.format_link(f'{config.site_url}/collections.html')}">
                        <p>Collections</p>
                    </a>
                </div>
                <div class="keywords border">
                    <a href="#head">
                        <p>Top</p>
                    </a>
                </div>
                <div class="keywords border">
                    <p>&copy; {datetime.now().year} {config.site_name}</p>
                </div>
            </div>
        </footer>
    </body>
</html>"""