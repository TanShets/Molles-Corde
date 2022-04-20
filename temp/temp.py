fp = open("temp.txt", "w")
names = [
    # "q-t_interval", "t_interval", "p_interval", "qrs", "T", "P", "QRST", "J",
    # "Q wave", "R wave", "S wave", "R' wave", "S' wave", "no_of_deflections"
    # "JJ wave Amp", "Q wave Amp", "R wave Amp", "S wave Amp", "R' wave Amp", "S' wave Amp",
    # "P wave Amp", "T wave Amp", "QRSA", "QRSTA"
    # "Ragged R wave", "Diphasic Derivation of R wave",
    # "Ragged P wave", "Diphasic Derivation of P wave",
    # "Ragged T wave", "Diphasic Derivation of T wave"
    # "sbp", "tobacco", "ldl", "adiposity", "typea", "alcohol"
    # "famhist"
    "ap_hi", "ap_lo"
]

for i in names:
    fp.write(f'<fieldset class = "form-group">\n')
    fp.write(f'\t<label for = "{i}">{i}?</label>\n')
    fp.write(f'\t<input name = "{i}" type = "number" id = "{i}" step = "any">\n')
    # fp.write(f'\t<select name = "{i}" id = "{i}">\n')
    # fp.write('\t\t<option value = "1">Yes</option>\n')
    # fp.write('\t\t<option value = "0">No</option>\n')
    # fp.write("\t</select>\n")
    fp.write("</fieldset>\n")
fp.close()