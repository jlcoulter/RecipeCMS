"""Default CSS generation from config style variables."""


def generate_css(config):
    """Generate the full CSS string from config style variables.
    Uses the existing style.css structure but injects config values into :root."""
    style = config.style

    # Build CSS custom properties from config
    root_vars = []
    root_vars.append(f"  --light-bg: {style.get('light_bg', '#fffcf7')};")
    root_vars.append(f"  --light-subtitle: {style.get('light_subtitle', 'rgb(56, 56, 56)')};")
    root_vars.append(f"  --light-border: {style.get('light_border', 'rgb(27, 27, 27)')};")
    root_vars.append(f"  --light-text: {style.get('light_text', 'black')};")
    root_vars.append(f"  --light-background: {style.get('light_background', '#ffffff')};")
    root_vars.append(f"  --light-item-background: {style.get('light_item_background', '#ffecdc')};")
    root_vars.append(f"  --dark-bg: {style.get('dark_bg', 'rgb(14 14 14)')};")
    root_vars.append(f"  --dark-subtitle: {style.get('dark_subtitle', 'rgb(210, 210, 210)')};")
    root_vars.append(f"  --dark-border: {style.get('dark_border', 'rgb(41 41 41)')};")
    root_vars.append(f"  --dark-text: {style.get('dark_text', 'rgb(241, 241, 241)')};")
    root_vars.append(f"  --dark-background: {style.get('dark_background', '#2d101f')};")
    root_vars.append(f"  --dark-item-background: {style.get('dark_item_background', '#1b1b1b')};")

    font_family = style.get('font_family', '"Ubuntu", serif')
    font_weight = style.get('font_weight', '700')
    border_radius = style.get('border_radius', '1rem')
    border_width = style.get('border_width', '0.2rem')

    return f""":root {{
  color-scheme: light dark;
{chr(10).join(root_vars)}
}}

body {{
    color: light-dark(var(--light-text), var(--dark-text));
    background-color: light-dark(var(--light-bg), var(--dark-bg));
}}

body, input {{
    font-family: {font_family};
    font-weight: {font_weight};
}}

#head {{
    align-content: flex-start;
    display: flex;
    flex-flow: row wrap;
    margin-left: 0.8rem;
}}

#foot {{
    align-content: flex-start;
    display: flex;
    flex-flow: row wrap;
    margin-left: 0.8rem;
    margin-top: 1rem;
}}

/* -------------- */
/* Item Tile */
/* -------------- */

.recipeTile {{
    max-width: 30rem;
    min-width: 15rem;
    flex: 1 0;
    margin: 1rem 1rem 1rem 1rem;
    background-color: light-dark(var(--light-background), var(--dark-background));
}}

.recipeTile img {{
    max-width: 100%;
    border-radius: 0.7rem 0.7rem 0rem 0rem;
    border-style: hidden;
}}

.recipeTile p {{
    margin-left: 1rem;
    margin-right: 1rem;
}}

.recipeTile a {{
    color: light-dark(var(--light-text), var(--dark-text));
    text-decoration: none;
}}

.recipeTile .title {{
    font-weight: bold;
    font-size: 1.5rem;
    margin-top: 2px;
    margin-bottom: 2px;
}}

.recipeTile .subtitle {{
    color: light-dark(var(--light-subtitle), var(--dark-subtitle));
    margin-top: 2px;
    margin-bottom: 2px;
}}

.innerTile {{
    height: 100%;
    width: 100%;
    margin-bottom: 1rem;
}}

/* Keyword tiles */

.keywordContainer {{
    align-content: flex-start;
    display: flex;
    flex-flow: row wrap;
}}

.keywordSection h1 {{
    margin-top: 0rem;
}}

.keywords {{
    max-width: fit-content;
    flex: 0 0 auto;
    margin: 0.2rem 0.2rem 0.2rem 0.2rem;
    background-color: light-dark(var(--light-bg), var(--dark-bg));
}}

.keywords p {{
    padding: 0.5rem 0.5rem 0.5rem 0.5rem;
    margin: 0;
}}

.keywords a {{
    color: light-dark(var(--light-text), var(--dark-text));
    text-decoration: none;
}}

.keywordBlock {{
    min-width: 13rem;
    margin: 1rem;
    padding: 1rem;
    flex: 1 0;
    background-color: light-dark(var(--light-background), var(--dark-background));
}}

.keywordSection {{
    align-content: flex-start;
    display: flex;
    flex-flow: row wrap;
}}

.keywordContainer h3 {{
    margin-bottom: 0px;
    margin-top: 0.7rem;
}}

.border {{
    border-radius: {border_radius} {border_radius} {border_radius} {border_radius};
    border-style: solid;
    border-width: {border_width};
    border-color: light-dark(var(--light-border), var(--dark-border));
    outline-width: 0.3rem;
    outline-style: solid;
    outline-offset: -0.3rem;
    outline-color: light-dark(var(--light-border), var(--dark-border));
}}

.offset {{
    margin-left: 1rem;
    margin-right: 1rem;
}}

.removeOffsetHeight {{
    margin-bottom: 0rem;
}}

.removeOffsetTop {{
    margin-top: 0rem;
}}

.offsetHeight {{
    margin-bottom: 1rem;
}}

.offsetTop {{
    margin-top: 1rem;
}}

.offsetBottom {{
    margin-bottom: 1rem;
}}

.offsetLeftEight {{
    margin-left: 0.8rem;
}}

.padding {{
    padding: 1rem;
}}

.lightBackground{{
    background-color: light-dark(var(--light-background), var(--dark-background));
}}

#recipePage {{
    align-content: flex-start;
    display: flex;
    flex-flow: row wrap;
}}

#recipe {{
    flex: 1 0;
    max-width: 1500px;
}}

#recipeImg {{
    margin: 1rem;
}}

#recipe img {{
    max-width: 100%;
    border-radius: 0.9rem;
    border-style: none;
    display: block;
}}

#recipeSidecar {{
    flex: 1 0;
    max-width: 800px;
}}

.recipeContainer {{
    align-content: flex-start;
    display: flex;
    flex-flow: row wrap;
}}

.recipeContainer img {{
    max-width: 100%;
}}

.recipeComponent {{
    flex: 1 0;
    margin: 1rem;
    min-width: 12rem;
    padding: 1rem;
    background-color: light-dark(var(--light-item-background), var(--dark-item-background));
}}

/* Search */
#searchHead {{
    padding: 1rem;
    margin-top: 1rem;
    background-color: light-dark(var(--light-background), var(--dark-background));
}}

#searchInput {{
    padding: 1rem;
}}

#searchBase {{
    padding: 1rem;
    background-color: light-dark(var(--light-background), var(--dark-background));
}}
#searchBase h3, #searchHead h3 {{
    margin-bottom: 0rem;
}}

#searchBase h1, #searchHead h1 {{
    margin-top: 0rem;
}}

.noBG {{
    background-color: rgba(255, 255, 255, 0);
}}

.noBG > .keywords{{
    float: left;
    margin: 0rem;
}}

.noBG > .keywords.keywordSidecar {{
    margin-left: -0.6rem;
}}
"""