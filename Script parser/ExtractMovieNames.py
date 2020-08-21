import json

INPUT_FILE_NAME = 'Bechdel/allmovies.json'
OUTPUT_FILE_NAME = 'Bechdel/2ratedmovies.csv'

in_file = open(INPUT_FILE_NAME, 'r')
out_file = open(OUTPUT_FILE_NAME, 'w')

re = in_file.read()

data = json.loads(re)

sorted_list = []

for movie in data:
    if movie['rating'] is 2:
        sorted_list.append(movie['title'].replace(',', ''))
        print('one gone')

sorted_list.sort()

out_file.write(sorted_list[0])
for title in sorted_list[1:]:
    out_file.write(',' + title)

in_file.close()
out_file.close()