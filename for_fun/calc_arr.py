from collections import Counter

result_list = [
    {'phones': 601802, 'emails': 385007, 'emails&phones': 364726, 'totalResult': 656304},
    {'phones': 756546, 'emails': 256553, 'emails&phones': 250220, 'totalResult': 835833},
    {'phones': 277117, 'emails': 133820, 'emails&phones': 129557, 'totalResult': 306799},
    {'phones': 247640, 'emails': 96893, 'emails&phones': 94515, 'totalResult': 275872},
    {'phones': 256657, 'emails': 120374, 'emails&phones': 117485, 'totalResult': 281373}
]
result = Counter()
for element in result_list:
    result += Counter(element)
print(result)