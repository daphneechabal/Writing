#!/usr/bin/env python
# The line above is important, so keep it! It allows the script to be read via the bash terminal.
#
###########################################################################################
#Beginning of the editing section.
#Fill in the variables as specified in ANTs_instructions word document.
#
runnum =
vol =
mid =
tr =
vox_x =
vox_y =
vox_z =
path = "/"
path_length =
BOLDfile = ""
STRUCfile = ".nii.gz"
path_template = "/"
template = ".nii.gz"
resampled_template = ".nii.gz"
#
# End of editing section
# From now on, do not modify the script unless you know python and understand all the steps!
###########################################################################################
midvol = ["0" for digits in range(4-len(str(mid)))] + [str(mid)]
midvol = ''.join(midvol)
import string, os, sys, glob, os.path
allpp_path = glob.glob(path+"*[0-9][0-9][0-9]")
directory = set([int(num.split('/')[path_length][-3:]) for num in allpp_path])
print ""
print ""
print "Beginning Step 1. Splitting functional data files into single-volume files for all participants."
print ""
print ""
for participant_number in directory:
    name = str(participant_number)
    name = "001"
    os.chdir(path)
    if os.path.exists(name):
        for run in range(1,runnum+1):
            run = str(run)
            if os.path.isfile(path + name + "/func/" + BOLDfile + run+ ".nii.gz") == True:
                if os.path.isfile(path + name + "/junk/" + name + "_" + run + "_0001.nii.gz") == False:
                    print "Split structural files into " + str(vol) + " single-volume files for participant " + name + ", run " + run
                    os.system("fslsplit " + path + name + "/func/" + BOLDfile + run +".nii.gz " + path + name + "/junk/" + name + "_" + run + "_ -t")
                    print "             Done."
                else:
                    print "  !  !  !  !  !  !  !  !  !  !  !"
                    print "You already split your structural files for participant " + name + ", run " + run
                    print "  !  !  !  !  !  !  !  !  !  !  !"
print "Done with splitting structural files."
print ""
print ""
print ""
print "Unto Step 2."
print ""
print ""
print ""
print "Beginning Step 2. Calculating transformations from mid-volume functionals to structurals!"
print ""
print ""
for participant_number in directory:
    name = str(participant_number)
    name = "001"
    os.chdir(path)
    if os.path.exists(name):
        for run in range(1,runnum+1):
            run = str(run)
            if os.path.isfile(path + name + "/func/" + BOLDfile + run + ".nii.gz") == True:
                if os.path.isfile(path + name + "/func/run" + run + "_FunctoT1_0GenericAffine.mat") ==False:
                    print "Calculating BOLD -> T1 transformations for participant " + name + ", run " + run
                    os.system("antsRegistrationSyN.sh -d 3 -f " + path + name + "/anat/" + STRUCfile + " \
                    -m " + path + name + "/junk/" + name + "_" + run + "_" + midvol + ".nii.gz \
                    -o " + path + name + "/func/run" + run + "_FunctoT1_ \
                    -t a")
                    print "             Done."
                else:
                    print "  !  !  !  !  !  !  !  !  !  !  !"
                    print "You already calculated BOLD -> T1 transformations for participant " + name + ", run " + run
                    print "  !  !  !  !  !  !  !  !  !  !  !"
print "Done with calculating BOLD -> T1 transformations."
print ""
print ""
print ""
print "Unto Step 3."
print ""
print ""
print ""
print "Beginning Step 3. Calculating transformations from structurals to the template!"
print ""
print ""
for participant_number in directory:
    name = str(participant_number)
    name = "001"
    os.chdir(path)
    if os.path.exists(name):
        if os.path.isfile(path + name + "/anat/" + STRUCfile) == True:
            if os.path.isfile(path + name + "/anat/Struc2Temp_0GenericAffine.mat") ==False:
                print "Calculating T1 -> Template transformations for participant " + name
                os.system("antsRegistrationSyN.sh -d 3 -f " + path_template + template + " \
                -m " + path + name + "/anat/" + STRUCfile + " \
                -o " + path + name + "/anat/Struc2Temp_ \
                -t s")
                print "             Done."
            else:
                print "  !  !  !  !  !  !  !  !  !  !  !"
                print "You already calculated T1 -> Template transformations for participant " + name
                print "  !  !  !  !  !  !  !  !  !  !  !"
        else:
            print "  !  !  !  !  !  !  !  !  !  !  !"
            print "You don't have a skull stripped structural file for participant " + name
            print "Is that normal ?! Go check participant " + name
            print "  !  !  !  !  !  !  !  !  !  !  !"
print "Done with calculating T1 -> Template transformations."
print ""
print ""
print ""
print "Unto Step 4."
print ""
print ""
print ""
print "Beginning Step 4. Concatenating the all step 2. and step 4. transforms with mid-volume functionals as reference!"
print ""
print ""
for participant_number in directory:
    name = str(participant_number)
    name = "001"
    os.chdir(path)
    if os.path.exists(name):
        for run in range(1,runnum+1):
            run = str(run)
            if os.path.isfile(path + name + "/func/" + BOLDfile + run + ".nii.gz") == True:
                if os.path.isfile(path + name + "/junk/run" +  run + "_allApplied.nii.gz") ==False:
                    print "Concatenating all transforms for participant " + name + ", run " + run
                    os.system("antsApplyTransforms -d 3 -i " + path + name + "/junk/" + name + "_" + run + "_" + midvol + ".nii.gz \
                    -r " + path_template + resampled_template + " \
                    -o [" + path + name + "/junk/run" +  run + "_allApplied.nii.gz,1] \
                    -t " + path + name + "/anat/Struc2Temp_1Warp.nii.gz \
                    -t " + path + name + "/anat/Struc2Temp_0GenericAffine.mat \
                    -t " + path + name + "/func/run" + run + "_FunctoT1_0GenericAffine.mat")
                    print "             Done."
                else:
                    print "  !  !  !  !  !  !  !  !  !  !  !"
                    print "You already concatenated all transforms for participant " + name + ", run " + run
                    print "  !  !  !  !  !  !  !  !  !  !  !"
print "Done with concatenations."
print ""
print ""
print ""
print "Unto Step 5."
print ""
print ""
print ""
print "Beginning Step 5. Applying all transformations to every volume of every run of every participant!"
print ""
print ""
for participant_number in directory:
    name = str(participant_number)
    name = "001"
    os.chdir(path)
    if os.path.exists(name):
        for run in range(1,runnum+1):
            run = str(run)
            if os.path.isfile(path + name + "/func/" + BOLDfile + run + ".nii.gz") == True:
                if os.path.isfile(path + name + "/junk/transformed_run" + run + "_" + num + ".nii.gz") ==False:
                    merge = "fslmerge -t " + path + name + "/func/transformed_run" + run + ".nii.gz "
                    for i in range(0,vol-1):
                        ii = str(i)
                        iii = ["0" for digits in range(4-len(ii))] + [ii]
                        num = ''.join(iii)
                        print "Applying all transforms for volume " + num + " of run number " + run + " of participant " + name
                        os.system("antsApplyTransforms -d 3 -i " + path + name + "/junk/" + name + "_" + run + "_" + num + ".nii.gz \
                        -r " + path_template + resampled_template + " \
                        -t " + path + name + "/junk/run" +  run + "_allApplied.nii.gz \
                        -o " + path + name + "/junk/transformed_run" + run + "_" + num + ".nii.gz")
                        print "             Done."
                        merge = merge + path + name + "/junk/transformed_run" + run + "_" + num + ".nii.gz "
                    print "Now merging the normalized simgle-volume functional files into one file."
                    print "And putting that final file in the funcional folder!"
                    os.system(merge)
                    print "             Merging Done."
print ""
print "All the transformations have been applied. You now have your final functional data files."
print ""
print "But before you go, let's make sure the TR (pixdim4) is correct!"
print ""
print "Beginning Step 6. Changing the TR back to what it should be in the header (DOESN'T IMPACT THE DATA)."
print ""
print ""
for participant_number in directory:
    name = str(participant_number)
    name = "001"
    os.chdir(path)
    if os.path.exists(name):
        for run in range(1,runnum+1):
            run = str(run)
            if os.path.isfile(path + name + "/func/" + BOLDfile + run + ".nii.gz") == True:
                os.chdir(path + name + "/func/")
                print "To change header, first unzipping the transformed_run#.nii.gz for participant " + name + ", run " + run
                os.system("gunzip transformed_run" + run + ".nii.gz")
                print "             Done."
                print "File unzipped. Now, changing the header."
                os.system("nifti_tool -mod_hdr -prefix final_run" + run + ".nii -infiles transformed_run" + run + ".nii -mod_field pixdim '1.0 " + str(vox_x) + " " + str(vox_y) + " " + str(vox_z) + " " + str(tr) + " 0.0 0.0 0.0'")
                print "             Done."
                print "Rezipping the final product, final_run#.nii.gz"
                os.system("gzip final_run" + run + ".nii")
                os.system("gzip transformed_run" + run + ".nii")

                print "             Done."
print "Done fixing Nifti headers. You can now model the data in fsl's FEAT safely, after double checking with fslinfo."
print "ANTS finished"
os.chdir(path)
###########################################################################################
#You have finished using ANTs and now have normalized functional data files.
#
#
#You can uncomment the lines below of your choice to delete the files you won't be modelling.
#
###########################################################################################

#for participant_number in directory:
#    name = str(participant_number)
#    os.chdir(path)
#    if os.path.exists(name):
#        os.system("rm -f -r " + path + name + "/junk/")
#        os.system("rm -i " + path + name + "/anat/Struc2Temp_0GenericAffine.mat")
#        os.system("rm -i " + path + name + "/anat/Struc2Temp_1Warp.nii.gz")
#        os.system("rm -i " + path + name + "/anat/Struc2Temp_1InverseWarp.nii.gz")
#        os.system("rm -i " + path + name + "/anat/Struc2Temp_Warped.nii.gz")
#        os.system("rm -i " + path + name + "/anat/Struc2Temp_InverseWarped.nii.gz")
#        os.system("rm -i " + path_template + resampled_template)
#        for run in range(1,runnum+1):
#            if os.path.isfile(path + name + "/func/" + BOLDfile + run + ".nii.gz") == True:
#               os.system("rm -i " + path + name + "/func/FunctoT1_Warped.nii.gz")
#               os.system("rm -i " + path + name + "/func/FunctoT1_InverseWarped.nii.gz")
#               os.system("rm -i " + path + name + "/anat/FunctoT1_0GenericAffine.mat")
