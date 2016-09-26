import BrownPrep 
filename = "../../../brown_notags"
filename2 = "../../brown_full_text"
brown = BrownPrep.BrownCleanUp(filename, filename2)
brown.extractText()