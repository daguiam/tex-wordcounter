#!/bin/bash
# declare STRING variable
GIT_REPO=$1
TMP_DIR='tmp'
CURRENT_DIR=$(PWD)
COMMITS="commits.txt"
TIMESTAMPS="timestamps.txt"

# Creating temporary directory
mkdir $TMP_DIR
cd "$TMP_DIR/thesis-phd"

git log --pretty="%H" > $CURRENT_DIR/$COMMITS
git log --pretty="%cd" > $CURRENT_DIR/$TIMESTAMPS
# declare HASHES=$($COMMITS)

HASHES="$(git log --pretty="%H")"
TIMESTAMPS="$(git log --pretty="%cd")"
echo "$HASHES"
#echo "$TIMESTAMPS"
# git clone $GIT_REPO
git stash

for commit in $(git rev-list --branches)
do
    git checkout $commit
    WORDCOUNT=$(python ../../texwordcounter.py)
    echo $WORDCOUNT >> $CURRENT_DIR/word_count.txt 
    echo $commit, $WORDCOUNT
done


# git log --pretty="%H,%an,%cd" > commits.csv

# Going back to original directory and clean up
cd $CURRENT_DIR
# rm -rf $TMP_DIR