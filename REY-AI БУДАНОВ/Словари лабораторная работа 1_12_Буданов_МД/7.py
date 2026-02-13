songs = ["Like a Rolling Stone", "Satisfaction", "Imagine", "What's Going On", "Respect", "Good Vibrations"]
playcounts = [78, 29, 44, 21, 89, 5]
plays = dict(zip(songs,playcounts))
print(plays)
plays['Purple Haze'] = 1
library = {'The Best Songs': plays,'Sunday Feelings': {}}
print(library)
