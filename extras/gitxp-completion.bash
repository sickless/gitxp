#!bash
#
# bash completion support for gitxp
#

_possible_xpaths_of_file()
{
    filename=$1
    current_xpath=$2
    temporaryfile=$(tempfile --suffix=.${filename#*.})
    if [ $3 == "FILE" ]
    then
        cat $filename > $temporaryfile
    elif [ $3 == "HEAD" ]
    then
        git show "HEAD:$filename" > $temporaryfile
    fi
    ending_with_slash=$(echo $current_xpath | grep -c "/$")
    # All xpaths with ctags!
    allxpaths=$(ctags --fields=s -f - $temporaryfile | sed 's/\t.*[^\t]\t.*[^:]:/ /g; s|\.|/|g; s|$/;"||g; s|$/||g; s|'"$filename"'.*$||g' | awk '{ if ($2) print $2"/"$1; else print $1}')
    rm $temporaryfile
    #allxpaths=$(echo $ctags | sed 's/\t.*[^\t]\t.*[^:]:/ /g; s|\.|/|g; s|$/;"||g; s|$/||g; s|'"$filename"'.*$||g' | awk '{ if ($2) print $2"/"$1; else print $1}')
    possible_xpaths=""
    for one_xpath in $allxpaths
    do
        if [[ "/"$one_xpath == $current_xpath* ]] && [ $(echo $current_xpath | tr -cd '/' | wc -c) -eq $(echo "/"$one_xpath | tr -cd '/' | wc -c) ]
        then
            possible_xpaths="$possible_xpaths $filename/$one_xpath"
        fi
    done
    COMPREPLY=($(compgen -W "$possible_xpaths" -- $filename$current_xpath))
    return
}

_gitxp ()
{
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    filename=""
    xpath=""
    ending_with_slash=$(echo $cur |grep -c '/$')
    for part in `echo $cur | tr "/" " "`
    do
        # 1st part: filename path doesn't start by a '/'
        if [ -z "$filename" ] && [ -e "$part" ]
        then
            filename=$part
        elif [ -e "$filename/$part" ];
        then
            filename=$filename/$part
        else
            xpath=$xpath"/"$part
        fi
    done
    # $filename exists and is not a directory: try to show possible xpaths
    if [ -e $filename ] && [ ! -d $filename ]
    then
        # no xpath
        if [ -z $xpath ]
        then
            # add the "/"
            if [ 0 -eq $ending_with_slash ]
            then
                COMPREPLY=($filename/)
                return
            # Filename + '/': set xpath='/'
            else
                xpath="/"
            fi
        fi
        # Get possible ones
        _possible_xpaths_of_file $filename $xpath $1
        # Only one choice from the possible ones and it's the current one? Try to get children
        if [ ${#COMPREPLY[@]} -eq 1 ] && [ ${COMPREPLY[0]} == $filename$xpath ]
        then
            _possible_xpaths_of_file $filename "$xpath/" $1
        fi
    fi
    return
}

_git_addxp()
{
    _gitxp "FILE"
}

_git_delxp()
{
    _gitxp "FILE"
}

_git_resetxp()
{
    _gitxp "HEAD"
}

_git_checkoutxp()
{
    _gitxp "FILE"
}

if [ -z "`type -t __git_find_on_cmdline`" ]; then
	alias __git_find_on_cmdline=__git_find_subcommand
fi

