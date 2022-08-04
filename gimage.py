# google drive내의 이미지의 공유 링크를 html 이미지 첨부 링크로 변환하는 프로그램입니다.
# google drive의 이미지 공유 링크를 copy&paste하면 clipboard로 변환된 링크를 저장합니다.

import clipboard

share_link = str(input("type share link : "))

split_1 = share_link.split('file/d/')
id = split_1[1].split('/')[0]

html_link = split_1[0] + 'uc?export=view&id=' + id

clipboard.copy(html_link)
print("clipboard에 링크가 저장되었습니다.. paste it!")