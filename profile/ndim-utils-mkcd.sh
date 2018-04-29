# make directory (tree) (if necessary), and then change to it
mkcd() {
    if [ "$#" -gt 1 ]; then
	echo "mkcd: Can only create and change to one directory." 1>&2
	return 2
    fi
    mkdir -p "$1" && cd "$1"
}
