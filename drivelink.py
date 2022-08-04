share_link = str(input("type share link : "))

split_1 = share_link.split('file/d/')
id = split_1[1].split('/')[0]

html_link = split_1[0] + 'uc?export=view&id=' + id
print(html_link)