def repeat_stuff(stuff,num_repeats=10):
    print()
    statement = stuff * num_repeats
    return statement

lyrics = repeat_stuff('Row',3) + "Your boat"
song = repeat_stuff(lyrics)
print(song)