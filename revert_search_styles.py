import re

with open('static/css/styles.css', 'r') as f:
    css = f.read()

# Replace .search and its descendants
search_pattern = r'/\* Search function  \*/\n\.search \{[\s\S]*?(?=/\* Button Styles \*/)'
new_search = '''/* Search function  */
.search {
    display: flex;
    justify-content: center;
    padding-top: 10px;
}

'''
css = re.sub(search_pattern, new_search, css)

# Remove .clear-btn
clear_btn_pattern = r'\.clear-btn \{[\s\S]*?\}\n\n\.clear-btn:hover \{[\s\S]*?\}\n\n'
css = re.sub(clear_btn_pattern, '', css)

# Remove empty-state and munro-results-container
empty_state_pattern = r'/\* Empty state styles \*/\n\.empty-state \{[\s\S]*?\}\n\n/\* Add margin to results container to push it down from search bar \*/\n\.munro-results-container \{[\s\S]*?\}\n\n'
css = re.sub(empty_state_pattern, '', css)

# Fix .individual-region
# In the current file, there's animport re

with open('static/css/styles.css', 'rit
with op_pa    css = f.read()

# Replace .search and its descendants
se--
# Replace .searc cosearch_pattern = r'/\* Search fu\nnew_search = '''/* Search function  */
.search {
    display: flex;
    justify-conte\n.search {
    display: flex;
    justify-content:      dispti    justify-conte2s    padding-top: 10px;
}

/}