sales_data = [[12,17,22],[2,10,3],[5,12,13]]
scoops_sold = 0

for sale in sales_data:
    for score in sale:
        scoops_sold += score
print(scoops_sold)