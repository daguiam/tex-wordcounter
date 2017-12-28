#!/bin/bash
# declare STRING variable
GIT_REPO=$1
TMP_DIR='tmp'
CURRENT_DIR=$(PWD)
#print variable on a screen
echo $0 $1 $2
echo "GIT REPO" 

# Creating temporary directory
mkdir $TMP_DIR
cd $TMP_DIR


# git clone $GIT_REPO


# git log --pretty="%H,%an,%cd" > commits.csv

# Going back to original directory and clean up
cd $CURRENT_DIR
# rm -rf $TMP_DIR