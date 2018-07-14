import json

# create an avinciClub dictionary
avinciClub = {}

# Assign teacher list to avinciClub dictionary
avinciClub["teachers"] = ["Sarah", "Ben", "Yan"]

# Assign student list to avinciClub dictionary
avinciClub["Students"] = ["Arca","Mary", "Micheal", "Luv", "Justin", "Oliver", "Warren", "Jonathan", "Helena"]
print("avinciClub: ", avinciClub)

# Serialize avinciClub dictionary to json string 
# and write to a file
with open("avinciclub.json", "w") as fWrite:
    json.dump(avinciClub, fWrite)

# Read json string from a file 
# and deserialize it to a new directionary(new_avinciClub)
with open("avinciclub.json") as fRead:
    new_avinciClub = json.loads(fRead.read())
print("new_avinciClub: ", new_avinciClub)