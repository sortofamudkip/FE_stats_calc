## for web scraping
from bs4 import BeautifulSoup
from requests import get, RequestException
def simple_get(url):
    try:
        with (get(url, stream=True)) as resp:
        	return resp.content if is_good_response(resp) else None
    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def get_info_web(name): # not used
	soup = BeautifulSoup(simple_get("https://serenesforest.net/blazing-sword/characters/growth-rates/"), features="html.parser")
	tag = soup.find("td", string=name)
	if tag is None:
		print("\nNo information for character {} was found!".format(name))
		exit(0)
	return [x.string for x in tag.find_next_siblings()]

## for stat calculation 
from itertools import combinations, accumulate

def f(stats: list, s: list) -> float:
	prob = stats[0] if s[0] else 1 - stats[0]
	if prob >= 1: prob = 1.
	for i in range(1,len(s)):
		prob *= stats[i] if s[i] else 1 - stats[i]
	return prob

def F(k: int, stats: list) -> float:
	n = len(stats)
	S_k = combinations(range(n), k)
	_sum = 0
	for _ in S_k:
		s = [0 for i in range(n)]
		for x in _:
			s[x] = 1
		# print(s)
		_sum += f(stats, s)
	return _sum

## for data analysis
def get_info_list(all_stats: dict, name: str):
	return all_stats[name]

def ans(all_stats: dict, name: str, print_info=True):
	_stats = get_info_list(all_stats, name)
	stats = [int(x)/100.0 for x in _stats]
	results = [F(i, stats) for i in range(len(stats)+1)]
	accu = list(accumulate(results))
	reverse = list(accumulate(results[::-1]))[::-1]
	expected = sum([i*results[i] for i in range(len(stats))])
	if print_info:
		print("Printing stats for {}:".format(name))
		print(" #    chance   cumulative      reverse")
		for i in range(len(stats)+1):
			print("{:2d}:  {:6.2f}%      {:6.2f}%      {:6.2f}%".format(
				i, 100*results[i], 
				100*accu[i],
				100*reverse[i]))
		print("{} is expected to level up {:.2f} stats on average".format(name, expected))
	return results, accu, reverse, expected


## For item selection
def get_all(url: str) -> dict: 
	soup = BeautifulSoup(simple_get(url), features="html.parser")
	tag = soup.find("div", class_="entry")
	tag = [x for x in tag.table.tbody.children if x != "\n"]
	characters = {}
	for y in tag:
		y = [z for z in y if z != "\n"]
		if y[0].string != "Name" and y[0].string != "Character": 
			characters[y[0].string] = [z.string for z in y][1:]
	return characters 

## Writing to file

if __name__ == "__main__":
	choice_dict = {
	"FE6": "https://serenesforest.net/binding-blade/characters/growth-rates/", 
	"FE7": "https://serenesforest.net/blazing-sword/characters/growth-rates/", 
	"FE8": "https://serenesforest.net/the-sacred-stones/characters/growth-rates/"}
	choice = input("What character is your game in? ({})\n".format(" ".join(choice_dict.keys())))
	if choice in choice_dict: url = choice_dict[choice]
	else: print("Invalid name."); exit(0)

	import sys
	saved_stdout = sys.stdout
	sys.stdout = open(choice + "_result.txt", "w")
	all_chars = get_all(url)
	total = 0
	for char in all_chars:
		result, accu, reverse, expected = ans(all_chars, char, True)
		total += expected

	print("Average over all characters: {}".format(total/len(all_chars)))
	sys.stdout = saved_stdout

	print("Input the name of the character you'd like to retrieve info for:")
	ans(all_chars, input())
	print("Average over all characters: {}".format(total/len(all_chars)))

