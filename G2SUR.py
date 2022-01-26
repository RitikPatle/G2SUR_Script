#G2SUR
#Program to convert gravsoft grids (.gri) to surfer ascii format (.grd)
#Input:
#   gravsoft grid file (usually .gri) {iFile}
#   surfer file name (should be .grd) {oFile}

# ifile = input("Enter the Input File: ")
# ofile = input("Enter the Output File: ")
ifile = 'ipfile.gri' #Predefined Input File
ofile = 'opfile.grd' #Predefined Output File

#Declaring Variables
nmax = 26000000
ficont = [] #Final List Paragraph Wise
templist = [] #Temporary list
finlist = [] #Final Formatted list

icontraw = open(ifile,'r+') #Raw Input File
icont = icontraw.readlines() #List of lines in a paragraph raw-data
rfi1, rfi2, rla1, rla2, dfi, dla = icont[0].split() #Extracting rfi1, rfi2, rla1, rla2, dfi, dla
icont.pop(0) #removing spaces
icont.pop(0) #removing spaces

#Converting the values of rfi1, rfi2, rla1, rla2, dfi, dla into Float values
rfi1= float(rfi1)
rfi2= float(rfi2)
rla1= float(rla1)
rla2= float(rla2)
dfi= float(dfi)
dla= float(dla)

#Deciding iell and izone
izone = 1
total_no_of_elem = 0
for i in icont:
    if i == '\n':
        izone+=1
    else:
        res = len(i.split())
        total_no_of_elem+=res
iell = total_no_of_elem/izone
iell = int(iell)

#Creating the final formatted list finlist
icont = list(map(lambda s: s.strip(), icont))
icont = list(filter(lambda a: a != '', icont))
icont = list(map(lambda s: s.split(), icont))
for elem in icont:
    for e in elem:
        ficont.append(e)
elem_counter = 1
for i in ficont:
    if elem_counter == iell:
        templist.append(i)
        clist = templist[:]
        finlist.append(clist)
        templist.clear()
        elem_counter = 1
    else:
        templist.append(i)
        elem_counter+=1
#final formatted list finlist created

#Assuming Grids
if abs(rfi1)>100 or abs(rfi2)>100:
    if iell > 0:
        print(f"UTM Grid Assumed., izone: {izone}, iell: {iell}")
    if iell < 0:
        print("Polar Stereographic Grid Assumed.")
    lutm = True
else:
    lutm = False

#Deciding nn,ne
nn = (rfi2 - rfi1)/dfi + 1.5
ne = (rla2 - rla1)/dla + 1.5
nn,ne = int(nn),int(ne)

#To Exit the Program if nn x ne > nmax.
if nn*ne > nmax:
    print('The value of nn*ne > nmax.')
    print('Program Executed Successfully.')
    exit()

#Deciding Zmin Zmax
zmin = 9999.9
zmax = -9999.9
j = 0
for listelem in finlist:
    for cj in listelem:
        cj = float(cj)
        if j > nmax:
            print("Taken Too small grid increase Nmax.")
            print('Program Executed Successfully.')
            exit()
        if cj > 9999:
            cj = 9999
        else:
            if cj < zmin:
                zmin = cj
            if cj > zmax:
                zmax = cj
        j+=1

finlist.reverse() #Reversing the finlist

# Creating & Formating Output File (.grd)
countne = 1
formattedInfo = f'DSAA\n    {ne} {nn}\n    {rla1:.5f} {rla2:.5f}\n    {rfi1:.5f} {rfi2:.5f}\n    {zmin:.2f} {zmax:.2f}\n'
opFileVar = open(ofile, 'w')
print(formattedInfo, file = opFileVar)
for listelem in finlist:
    for elem in listelem:
        elem = float(elem)
        print(format(elem, '.5f'),end=' ',file=opFileVar)
        countne += 1
        if countne == 7:
            print('',file=opFileVar)
            countne = 1
    print('\n',file=opFileVar)
opFileVar.close()
print(f"{ofile} created successfully.")
print('Program Executed Successfully.')
#End of Program

# Short-Notations used in program are ->
#     ifile - Input File                   | ofile - Output File
#     icontraw - List of Raw Input Content | icont - List of Input Content Line Wise
#     ficont - List of Final Input Content | templist - Temporary List to Store Data in finlist Para-wise
#     finlist - Final Formatted List of Elements (Paragraphs) Stored as List Inside a List