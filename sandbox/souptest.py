from urllib.request import urlopen

with urlopen('https://abaft-surgeon.glitch.me/') as req: # open the url page
    print(req.read())