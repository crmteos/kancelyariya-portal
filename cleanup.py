with open('c:/kancelyariya-portal/decrees.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the end of my new script: '});' followed by '        }' and newlines
# My script ends at line 667 with '        }' after '            });'
end_marker = '});\n        }\n'
idx = content.find(end_marker)
if idx >= 0:
    # Keep content up to and including the end marker
    new_content = content[:idx + len(end_marker)]
    # Append clean footer
    new_content += '\n</body>\n</html>'
    
    with open('c:/kancelyariya-portal/decrees.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('File rewritten successfully')
else:
    print('End marker not found')