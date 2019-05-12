output = ""

with open('../evacuationzone.txt', 'r') as linkFile:
    cnt = 0
    for linkId in linkFile:
        if linkId != "\n":
            output += '<link id="{0}" from="{1}" to="200" length="0.1" freespeed="100000" capacity="100000" permlanes="10000.0" oneway="1" modes="car,bus" ></link>\n'.format(cnt,linkId.strip())
            cnt += 1
print(output)