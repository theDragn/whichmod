from tempfile import NamedTemporaryFile
import csv, shutil, os, sys

apply_to_faction_mods = False
apply_to_vanillaish_mods = True

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
    "DissassembleReassemble":"DaRa",
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
    "Ship and Weapon":"SWP",
    "Stop Gap Measure":"SGM",
    "tahlan":"Tahlan",
    "Tiandong":"THI",
    "Torchships":"TADA",
    "Vayra's Sector":"Vayra's Sector",
    "Vayra's Ship Pack":"VSP",
}



for item in os.listdir('.'):
    replace = False
    if os.path.isdir(item) and (apply_to_vanillaish_mods and (item in modnames_vanillaish.keys())):
        modname = modnames_vanillaish.get(item)
        replace = True
    if os.path.isdir(item) and (apply_to_faction_mods and (item in apply_to_faction_mods.keys())):
        modname = modnames_vanillaish.get(item)
        replace = True
    filepath = os.path.join(os.path.dirname(__file__), item, 'data', 'strings','descriptions.csv')
    if os.path.exists(filepath) and replace and os.path.isfile(filepath):
        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
        with open(filepath, newline='') as csvFile:
            reader = csv.reader(csvFile)
            writer = csv.writer(tempfile)

            editList = []
            for row in reader:
                editList.append(row)

            for row in editList:
                if (len(row) >= 2) and (len(row[2]) > 10) and ('[' not in row[2][0]):
                    row[2] = "[" + modname + "] " + row[2]
                writer.writerow(row)
        csvFile.close()
        tempfile.close()
        shutil.move(tempfile.name, filepath)
        print("Updated descriptions for " + modname)
input("Script complete. Press Enter to close.")



