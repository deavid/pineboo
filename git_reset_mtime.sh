rev=HEAD
if [ "$1" = "" ]; then
    git ls-tree -r -t --full-name --name-only "$rev" | xargs -P8 -n1 $0
else
    f=$1
    MTIME=$(git log --pretty=format:%cI -1 "$rev" -- "$f")
    touch -d $MTIME "$f";

fi
