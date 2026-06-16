"""JavaScript generation - search and random item JS."""


def generate_search_js(config, taxonomy_index, small_items):
    """Generate the search.js file content dynamically from config taxonomies."""
    # Build JS variable declarations for each taxonomy
    js_vars = f"items = {small_items};\n"
    for taxonomy in config.taxonomies:
        key = taxonomy['key']
        values = taxonomy_index.get_small_values(key)
        js_vars += f"{key} = {values};\n"
    js_vars += "filters = [];\n"

    # Build search sections for each taxonomy
    search_sections = ""
    for taxonomy in config.taxonomies:
        key = taxonomy['key']
        label = taxonomy['label']
        search_limit = taxonomy.get('search_limit', 9)
        section_id = f"{key}Results"

        search_sections += f"""
    // {label}
    output = "";
    outputs = 0;
    for (let i = 0; i < {key}.length; i++) {{
        const keyword = {key}[i];
         if (typeof keyword === 'string' && (searchText === '' || keyword.toLowerCase().includes(searchText))) {{
            const keywordLink = formatJsLink('{config.site_url}', keyword, true);
            output += `<div class="keywords noBG"><div class="keywords border"><a href="${{keywordLink}}"><p>${{keyword}}</p></a></div><div class="keywords keywordSidecar border"><a onClick="addFilter('${{keyword}}')"><p>+</p></a></div></div>`;
            outputs++;
         }}
        if (outputs >= {search_limit}) {{ break; }}
    }}
    document.getElementById("{section_id}").innerHTML = (output === "") ? '<div class="keywords border"><p>No Results</p></div>' : output;
"""

    return f"""
{js_vars}

function stringContainsAll(mainString) {{
    const lowerMainString = mainString.toLowerCase();
    if (!filters || filters.length === 0) {{
        return true;
    }}
    for (let i = 0; i < filters.length; i++) {{
        if (!lowerMainString.includes(filters[i].toLowerCase())) {{
            return false;
        }}
    }}
    return true;
}}

function formatJsLink(basePath, itemName, isKeyword = false) {{
    const removeHtmlExtension = "{str(config.remove_html_extension)}";
    let link;
    if (isKeyword) {{
        link = `${{basePath}}/keywords/${{itemName.split(' ').join('_').toLowerCase()}}`;
    }} else {{
        link = `${{basePath}}/${{itemName}}/${{itemName}}`;
    }}
    if (removeHtmlExtension === "False") {{
        link += ".html";
    }}
    return link;
}}

function search() {{
    const searchText = document.getElementById("searchInput").value.toLowerCase();

    let output = "";
    let outputs = 0;
    for (let i = 0; i < items.length; i++) {{
        const jsonObject = items[i];
        const combinedText = (jsonObject.name || "") + (jsonObject.recipeCuisine || "") + (jsonObject.recipeCategory || "") + (jsonObject.ingredientKeywords || []).toString();

        if (searchText === '' || combinedText.toLowerCase().includes(searchText)) {{
            if (stringContainsAll(combinedText)) {{
                const itemLink = formatJsLink('{config.site_url}', jsonObject.folder, false);
                output += `<div class="keywords noBG"><div class="keywords border"><a href="${{itemLink}}"><p>${{jsonObject.name}}</p></a></div></div>`;
                outputs++;
            }}
        }}
        if (outputs >= {config.search_result_limits.get('items', 9)}) {{ break; }}
    }}
    document.getElementById("itemResults").innerHTML = (output === "") ? '<div class="keywords border"><p>No Results</p></div>' : output;
{search_sections}
}}

function addFilter(filter) {{
    filters.push(filter);
    let output = "";
    for (let i = 0; i < filters.length; i++) {{
         const keywordLink = formatJsLink('{config.site_url}', filters[i], true);
         output += `<div class="keywords noBG"><div class="keywords border"><a href="${{keywordLink}}"><p>${{filters[i]}}</p></a></div><div class="keywords keywordSidecar border"><a onClick="removeFilter('${{filters[i]}}')"><p>-</p></a></div></div>`;
    }}
    document.getElementById("filters").innerHTML = output;
    search();
}}

function removeFilter(filter) {{
    filters = filters.filter(item => item !== filter);
    let output = "";
    for (let i = 0; i < filters.length; i++) {{
         const keywordLink = formatJsLink('{config.site_url}', filters[i], true);
         output += `<div class="keywords noBG"><div class="keywords border"><a href="${{keywordLink}}"><p>${{filters[i]}}</p></a></div><div class="keywords keywordSidecar border"><a onClick="removeFilter('${{filters[i]}}')"><p>-</p></a></div></div>`;
    }}
    if (output === "") {{
        output = '<div class="keywords border"><p>No Filters Selected</p></div>';
    }}
    document.getElementById("filters").innerHTML = output;
    search();
}}
"""


def generate_random_js(config, item_folders):
    """Generate the random.js file content."""
    return f"""
randomItems = {item_folders};
function random() {{
    const removeHtmlExtension = "{str(config.remove_html_extension)}";
    const url = window.location.href;
    const parts = url.split("/");
    const folderName = parts[parts.length - 1];
    const pageName = folderName.replace(".html", "");

    rand = Math.floor(Math.random() * randomItems.length);

    if(randomItems[rand] === pageName) {{
        random();
    }} else {{
        if (removeHtmlExtension === "True") {{
            document.querySelector(".keywords.random.border > a").href = '{config.site_url}/' + randomItems[rand] + '/' + randomItems[rand]
        }} else {{
            document.querySelector(".keywords.random.border > a").href = '{config.site_url}/' + randomItems[rand] + '/' + randomItems[rand] + '.html'
        }}
    }}
}}


function sharePage() {{
  const shareData = {{
    title: "{config.site_name}",
    text: document.getElementsByTagName("title")[0].innerHTML,
    url: window.location.href,
  }};
  try {{
    navigator.share(shareData);
  }} catch (err) {{
    resultPara.textContent = `Error: ${{err}}`;
  }}
}};
"""