# make directory (tree) (if necessary), and then change to it
mkcd() { mkdir -p "$1" && cd "$1"; }
