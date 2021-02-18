from tempfile import NamedTemporaryFile
import csv, shutil, os, sys

# This script is by theDragn, and is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

# first bit is the folder name (can be any part of the mod folder name, doesn't have to be the whole thing)
# second bit is what you want to go in the description
modnames_factions = {
    "ApproLight":"ApproLight",
    "Blackrock":"BRDY",
    "Celestial Mount":"CMC",
    "COPS":"COPS",
    "Dassault-Mikoyan":"DME",
    "DIABLEAVIONICS":"Diable",
    "Lanestate":"XLU",
    "The Exalted":"Exalted",
    "Foundation":"FoB",
    "Free Stars":"FSU",
    "FDS":"FDS",
    "Galaxy Tigers":"GT",
    "GKSec":"GKSec",
    "GrytpypeMoriarty":"GMDA",
    "HMI_brighton":"HMI Brighton",
    "HMI_Supervillains":"HMI Supervillains",
    "ICE":"ICE",
    "Interstellar Imperium":"II",
    "Kadur Remnant":"Kadur",
    "Kingdom of Terra":"KT",
    "Legacy of Arkgneisis":"LoA",
    "Neutrino corp":"Neutrino",
    "nabaal":"Kiith Nabaal",
    "Oculian Armada":"Oculian",
    "ORA":"ORA",
    "Pearson Exotronics":"Pearson",
    "Polaris_Prime":"Polaris",
    "Roider Union":"Roider Union",
    "scalartech":"Scalartech",
    "SCY":"Scy",
    "Shadowyards":"SRA", # adds some pirate stuff but it's visually distinctive
    "prv Starworks":"PRV", # adds some pirate stuff but it's visually distinctive
    "slyphon":"Slyphon",
    "FED":"FED",
    "Tiandong":"THI", # only adds a single common design- heavy mining laser
    "Tyrador":"TSC",
    "Underworld":"Underworld",
    "XhanEmpire":"Xhan",
    "VIC":"VIC",
    "YRXP":"Yuri", # has a few different design types, so maybe put it in the vanillaish list if you want
}

modnames_vanillaish = {
    "Anvil Industries":"Anvil",
    "Arsenal Expansion":"AE",
    "CWSP":"CWSP",
    "DisassembleReassemble":"DaRa",
    "ED Shipyard":"ED Shipyard",
    "fluffShipPack":"Fluff's Ship Pack",
    "Hegemony Expeditionary":"HEA",
    "HMI":"HMI",
    "HTE":"HTE",
    "JP_RC":"Junk Pirates",
    "LTA":"LTA",
    "Luddic_Enhancement":"Luddic Enhancement",
    "Mayasuran Navy":"Mayasuran Navy",
    "Metelson":"Metelson",
    "Missing":"MSM",
    "PulseIndustry":"Pulse Industry",
    "SEEKER_UC":"Seeker",
    "Ship and":"SWP",
    "Stop Gap Measure":"SGM",
    "tahlan":"Tahlan",
    "Torchships":"TADA",
    "Vayra's Sector":"Vayra's Sector",
    "Vayra's Ship Pack":"VSP",
}

remove = False
apply_to_faction_mods = False
apply_to_vanillaish_mods = False

options = input("""Options:\n
    v:   Modify descriptions for vanilla-ish mods only.
    f:   Modfiy descriptions for faction mods only.
    vf:  Modify descriptions for both faction and vanilla-ish mods.
    rv:  Revert changes to faction mods, returning descriptions to original form.
    rf:  Revert changes to vanilla-ish mods, returning descriptions to original form.
    rvf: Revert changes to all mods, returning descriptions to original form.
    e:   Exit without doing anything.
    Enter selection:""")

output = ''
if 'v' in options:
    apply_to_vanillaish_mods = True
    output = output + 'Changes applied to vanilla-ish mods.\n'
if 'f' in options:
    apply_to_faction_mods = True
    output = output + 'Changes applied to faction mods.\n'
if 'r' in options:
    remove = True
    output = output + 'Returned all descriptions to original form.'
if 'e' in options:
    exit()

for item in os.listdir('.'):
    replace = False
    invkeys = False
    infkeys = False
    actualkey = ''
    for key in modnames_vanillaish.keys():
        if key in item:
            invkeys = True
            actualkey = key
    for key in modnames_factions.keys():
        if key in item:
            infkeys = True
            actualkey = key
    if os.path.isdir(item) and (apply_to_vanillaish_mods and invkeys):
        modname = modnames_vanillaish.get(actualkey)
        replace = True
    if os.path.isdir(item) and (apply_to_faction_mods and infkeys):
        modname = modnames_factions.get(actualkey)
        replace = True
    filepath = os.path.join(os.path.dirname(__file__), item, 'data', 'strings','descriptions.csv')
    try:
        if os.path.exists(filepath) and replace and os.path.isfile(filepath):
            tempfile = NamedTemporaryFile('w+t', newline='', delete=False, encoding='utf-8')
            editsdone = False
            with open(filepath, newline='',errors='replace',encoding='utf-8') as csvFile:
                reader = csv.reader(csvFile,quoting=csv.QUOTE_ALL)
                writer = csv.writer(tempfile)
                for row in reader:
                    if len(row) >= 2 and len(row[1]) > 13:
                        raise Exception("malformed row: " + row[0])
                    if (len(row) >= 2) and (len(row[2]) > 10) and ('[' not in row[2][0]) and (row[1]=='SHIP' or row[1]=='WEAPON'):
                        row[2] = "[" + modname + "] " + row[2]
                        editsdone = True
                    if remove and (len(row) >= 2) and (len(row[2]) > 10) and '[' in row[2] and ']' in row[2] and modname in row[2]:
                        string = row[2]
                        row[2] = string[string.find(']')+2:len(string)]
                        editsdone = True
                    writer.writerow(row)
            csvFile.close()
            tempfile.close()
            if editsdone:
                shutil.move(tempfile.name, filepath)
            print("Updated descriptions for " + modname)
    except Exception as e:
        print("ERROR: in " + modname + ", " + str(e))
        print("Encountered an error with " + modname + ", skipping.")
print(output)
input("Done. Press Enter to close.")



