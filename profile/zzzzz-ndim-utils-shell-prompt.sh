# -*- mode: bash; indent-tabs-mode: nil -*-

########################################################################
# Only append the command to PROMPT_COMMAND if it is not already there
########################################################################

__ndim_cond_append_prompt_command() {
    local found=false
    local c
    for c in "${PROMPT_COMMAND[@]}"
    do
        if [[ "x$c" = "x$1" ]]
        then
            found=true
            break
        fi
    done
    if "$found"
    then
        :
    else
        PROMPT_COMMAND+=("$1")
    fi
}


########################################################################
# set up the prompt
########################################################################

# If the cursor is not in the first column, print a newline to start the
# actual prompt in the first column every time.
        # The cursor position is weird when nearing the $COLUMNS:
        # It is about the blinking cursor position, and not about the
        # where to write the next character position.
        # This unfortunately makes it impossible to reliably print
        # a character showing that we have inserted a LF.
        # printf $'\e[9l' #
__ndim_prompt_conditional_newline() {
    local pos
    if [ -t 0 ] && [ -t 1 ]
    then
        if IFS='[;' read -r -s -p $'\e[6n' -d 'R' -a pos <&0 >&1
        then
            local cursor_row="${pos[2]}"
            # printf "%s\n" "${pos[@]@A}" >> ~/moo.log
            # printf $'\e[9h' #
            if [ "$cursor_row" -eq 1 ]
            then
                :
            else
                printf "\n"
            fi
        fi
    fi
}
__ndim_cond_append_prompt_command __ndim_prompt_conditional_newline
            # elif [ $(( ( "$cursor_row" - 1 ) % "$COLUMNS" )) -eq 0 ]
            # then
            #    printf "\n"
            #else
            #    # ⁋ ␊
            #
            #    printf "$(tput dim)⁋$(tput sgr0)\n"
            #fi


if [ "x${ndim_orig_PS0:+set}" = x ]
then
    ndim_orig_PS0="$PS0"
fi
if [ "x${ndim_orig_PS1:+set}" = x ]
then
    ndim_orig_PS1="$PS1"
fi
declare -A ndim_prompts=()
ndim_prompts[system-default]="system default prompt"
ndim_prompts[old]="an old prompt"
ndim_prompts[older]="an older prompt"
ndim_prompts[color-lines]="an older prompt using colored lines"
ndim_prompts[darkblue]="newer dark blue prompt"
ndim_prompts[simple]="[user@host ~]$ _"
ndim_prompts[simple-exit-color]="[user@host ~]$ _ (exit code colors)"
ndim_prompts[extended-exit-color]="[user@host ~]$ _ (exit code colors + extended lines)"
ndim_prompts[ndim-exit-color]="[user@host ~]$ _ (exit code colors + extended lines + yellow command)"
ndim_prompts[ndim-pipestatus]="[user@host ~]$ _ (exit code colors + pipestatus + extended lines + yellow command)"
ndim_prompts[ndim-pipestatus-ml]="[user@host ~]$ _ (exit code colors + pipestatus + extended lines + yellow command + ML)"
ndim-prompt() {
    local k
    local max_len=20
    local t
    for k in "${!ndim_prompts[@]}"; do
        t="$k ${ndim_prompts[$k]}"
        if [[ "${#t}" -gt max_len ]]; then
            max_len="${#t}"
        fi
    done
    max_len="$(( max_len + 15 ))"
    if [[ max_len+2 -gt COLUMNS ]]; then
        max_len="$(( COLUMNS - 2 ))"
    fi
    if [ "x${1:+set}" = x ]
    then
        if tag="$( \
            (for k in "${!ndim_prompts[@]}"; do
                 printf "%s\0%s\0" "$k" "${ndim_prompts[$k]}"; \
             done) | xargs -0 dialog \
            --erase-on-exit \
            --title "Choose a prompt" \
            --menu "Choose a prompt from the list" \
            20 "$max_len" 12 \
            2>&1 > /dev/tty)"
        then
            printf "ndim-prompt: Setting new prompt: %s\n" "$tag"
            ndim-prompt "$tag"
            echo "${PS1@A}"
            return
        else
            printf "ndim-prompt: Keeping the existing prompt.\n"
            echo "${PS1@A}"
            return
        fi
    fi

    # set up git prompt
    GIT_PROMPT_SH="/usr/share/git-core/contrib/completion/git-prompt.sh"
    [ -f "$GIT_PROMPT_SH" ] && source "$GIT_PROMPT_SH"
    GIT_PS1_DESCRIBE_STYLE="branch"
    GIT_PS1_SHOWDIRTYSTATE=yes
    GIT_PS1_SHOWSTASHSTATE=yes
    GIT_PS1_SHOWUNTRACKEDFILES=yes
    GIT_PS1_SHOWUPSTREAM="verbose name git"

    # Define no-op __git_ps1 if not defined already
    if type -t __git_ps1 > /dev/null
    then
        :
    else
        __git_ps1() {
            :
        }
    fi

    unset VIRTUAL_ENV_DISABLE_PROMPT
    export VIRTUAL_ENV_DISABLE_PROMPT

    # readline variables (cf. ~/.inputrc)
    # bind "set active-region-start-color \"\""
    # bind "set active-region-end-color \"\""

    case "$1" in
        system-default)
            PS0="$ndim_orig_PS0"
            PS1="$ndim_orig_PS1"
            ;;
        simple)
            PS0="$ndim_orig_PS0"
            PS1="[\u@\h \W]\\\$ "
            ;;
        simple-exit-color)
            PS0="$ndim_orig_PS0"
            PS1="\$(if [[ \"\$?\" -eq 0 ]]; then printf \"\\[\\e[1;32;38;5;10m\\]\"; else printf \"\\[\\e[1;31;38;5;9m\\]\"; fi)[\u@\h \W]\\\$\[\\e[m\] "
            ;;
        extended-exit-color)
            PS0="$ndim_orig_PS0"
            PS1="\$(if [[ \"\$?\" -eq 0 ]]; then printf \"\\[\\e[1;32;38;5;10m\\]\"; else printf \"\\[\\e[1;31;38;5;9m\\]\"; fi)"
            export VIRTUAL_ENV_DISABLE_PROMPT=1
            PS1+="\${VIRTUAL_ENV:+\"venv \${VIRTUAL_ENV} \n\"}"
            PS1+="\$(__git_ps1 \"git %s\\n\\n\")"
            PS1+="[\u@\h \W]\\\$"
            PS1+="\[\\e[m\] "
            ;;
        ndim-exit-color)
            PS0="$ndim_orig_PS0"
            PS1=""
            export VIRTUAL_ENV_DISABLE_PROMPT=1
            PS1+="\${VIRTUAL_ENV:+\"\\[\\e[1;37;38;5;7m\\]venv\\[\\e[m\\] \\[\\e[1;38;5;15m\\]\${VIRTUAL_ENV}\\[\\e[m\\]\n\"}"
            PS1+="\$(__git_ps1 \"\\[\\e[1;37;38;5;7m\\]git\\[\\e[m\\] \\[\\e[1;38;5;15m\\]%s\\[\\e[m\\]\\n\\n\")"
            PS1+="\$(if [[ \"\$?\" -eq 0 ]]; then printf \"\\[\\e[1;32;38;5;10m\\]\"; else printf \"\\[\\e[1;31;38;5;9m\\]\"; fi)"
            PS1+="[\u@\h \W]\\\$"
            PS1+="\[\\e[0;38;5;11m\] "
            PS0+=$'\e[m'
            ;;
        ndim-pipestatus)
            PS0="$ndim_orig_PS0"
            PS1=""
            PS1+="\$("
            # save exit and pipe status for later
            PS1+="declare -a s=\"\$?\" ps=(\"\${PIPESTATUS[@]}\");"
            # python venv and pipenv etc (if VIRTUAL_ENV is set)
            export VIRTUAL_ENV_DISABLE_PROMPT=1
            PS1+="if [ \"x\${VIRTUAL_ENV:+set}\" = xset ]; then"
            PS1+="  printf \"\\[\\e[1;37;38;5;7m\\]venv\\[\\e[m\\] \\[\\e[1;38;5;15m\\]\${VIRTUAL_ENV}\\[\\e[m\\]\n\";"
            PS1+="fi;"
            # git status (if in git repo)
            PS1+="__git_ps1 \"\\[\\e[1;37;38;5;7m\\]git\\[\\e[m\\] \\[\\e[1;38;5;15m\\]%s\\[\\e[m\\]\\n\";"
            # exit status (if non-0)
            PS1+="if [[ \$s -ne 0 ]]; then"
            PS1+="  printf \"\\[\\e[1;37;38;5;7m\\]exit status\\[\\e[m\\]\";"
            PS1+="  printf \" %s\" \"\\[\\e[1;31;38;5;9m\\]\$s\";"
            PS1+="  printf \"\\[\\e[m\\]\\n\";"
            PS1+="fi;"
            # pipe status (if different from just exit status)
            PS1+="pipefail=false;"
            PS1+="for t in \"\${ps[@]}\"; do"
            PS1+="  if [[ \"\$t\" -ne 0 ]]; then"
            PS1+="    pipefail=:;"
            PS1+="    break;"
            PS1+="  fi;"
            PS1+="done;"
            PS1+="if [ \"\${ps[*]}\" = \"\$s\" ]; then pipefail=false; fi;"
            PS1+="if \"\$pipefail\"; then"
            PS1+="  printf \"\\[\\e[1;37;38;5;7m\\]pipe status\\[\\e[m\\]\";"
            PS1+="  for t in \"\${ps[@]}\"; do"
            PS1+="    if [[ \"\$t\" -eq 0 ]]; then"
            PS1+="      printf \" \\[\\e[1;32;38;5;10m\\]%s\" \"\$t\";"
            PS1+="    else"
            PS1+="      printf \" \\[\\e[1;31;38;5;9m\\]%s\"  \"\$t\";"
            PS1+="    fi;"
            PS1+="  done;"
            PS1+="  printf \"\\[\\e[m\\]\\n\";"
            PS1+="fi;"
            # set color depending on exit status for [user@host ~]
            PS1+="if [[ \"\$s\" -eq 0 ]]; then"
            PS1+="  printf \"\\[\\e[1;32;38;5;10m\\]\";"
            PS1+="else"
            PS1+="  printf \"\\[\\e[1;31;38;5;9m\\]\";"
            PS1+="fi;"
            PS1+=")"
            # print "[user@host ~]$ "
            PS1+="[\u@\h \W]\\\$"
            # set color to yellow for command line, reset color before running command
            # FIXME: Setting colors here means that background programs will print in the prompt color.
            #        There might be a way to configure readline (inputrc) to colorize the input in a better way.
            PS1+="\[\\e[1;33;38;5;11m\] "
            PS0+=$'\e[m'
            ;;
        ndim-pipestatus-ml)
            PS0="$ndim_orig_PS0"
            PS1=""
            PS1+="\[\\e[m\]"
            frame_color="\[\e[m\e[1;37;38;5;15m\]"
            PS1+="\[\e[m\]${frame_color@P}╭ \w\n"
            BL="${frame_color@P}│ \[\e[m\]"
            PS1+="\$("
            # save exit and pipe status for later
            PS1+="declare -a s=\"\$?\" ps=(\"\${PIPESTATUS[@]}\");"
            # python venv and pipenv etc (if VIRTUAL_ENV is set)
            export VIRTUAL_ENV_DISABLE_PROMPT=1
            PS1+="if [ \"x\${VIRTUAL_ENV:+set}\" = xset ]; then"
            PS1+="  printf \"${BL@P}\\[\\e[1;37;38;5;7m\\]venv\\[\\e[m\\] \\[\\e[1;38;5;15m\\]\${VIRTUAL_ENV}\\[\\e[m\\]\n\";"
            PS1+="fi;"
            # git status (if in git repo)
            PS1+="__git_ps1 \"${BL@P}\\[\\e[1;37;38;5;7m\\]git\\[\\e[m\\] \\[\\e[1;38;5;15m\\]%s\\[\\e[m\\]\\n\";"
            # exit status (if non-0)
            PS1+="if [[ \$s -ne 0 ]]; then"
            PS1+="  printf \"${BL@P}\\[\\e[1;37;38;5;7m\\]exit status\\[\\e[m\\]\";"
            PS1+="  printf \" %s\" \"\\[\\e[1;31;38;5;9m\\]\$s\";"
            PS1+="  printf \"\\[\\e[m\\]\\n\";"
            PS1+="fi;"
            # pipe status (if different from just exit status)
            PS1+="pipefail=false;"
            PS1+="for t in \"\${ps[@]}\"; do"
            PS1+="  if [[ \"\$t\" -ne 0 ]]; then"
            PS1+="    pipefail=:;"
            PS1+="    break;"
            PS1+="  fi;"
            PS1+="done;"
            PS1+="if [ \"\${ps[*]}\" = \"\$s\" ]; then pipefail=false; fi;"
            PS1+="if \"\$pipefail\"; then"
            PS1+="  printf \"${BL@P}\\[\\e[1;37;38;5;7m\\]pipe status\\[\\e[m\\]\";"
            PS1+="  for t in \"\${ps[@]}\"; do"
            PS1+="    if [[ \"\$t\" -eq 0 ]]; then"
            PS1+="      printf \" \\[\\e[1;32;38;5;10m\\]%s\" \"\$t\";"
            PS1+="    else"
            PS1+="      printf \" \\[\\e[1;31;38;5;9m\\]%s\"  \"\$t\";"
            PS1+="    fi;"
            PS1+="  done;"
            PS1+="  printf \"\\[\\e[m\\]\\n\";"
            PS1+="fi;"
            # set color depending on exit status for [user@host ~]
            PS1+="if [[ \"\$s\" -eq 0 ]]; then"
            PS1+="  printf \"${frame_color@P}╰ \\[\\e[1;32;38;5;10m\\]\";"
            PS1+="else"
            PS1+="  printf \"${frame_color@P}╰ \\[\\e[1;31;38;5;9m\\]\";"
            PS1+="fi;"
            PS1+=")"
            # print "[user@host ~]$ "
            PS1+="\u@\h \W\\\$"
            # set color to yellow for command line, reset color before running command
            # PS1+="\[\\e[m\] "
            PS1+="\[\\e[1;33;38;5;11m\] "
            PS0+=$'\e[m'
            unset BL
            ;;
        older)
            PS0="$ndim_orig_PS0"
            PS1="\[\\r\\e[K\\e[37;41;1m\][ \t | \\! | \$? | \w\$(__git_ps1 \" | git %s\") ]\[\\e[0m\\e[K\]\n\[\\e[37;44;1m\][\u@\h \W]\\\$\[\\e[0m\] "
            ;;
        old)
            PS0="$ndim_orig_PS0"
            PS1="\[\\r\\e[K\\e[37;41;1m\][ \t | \\! | \${PIPESTATUS[@]} | \w\$(__git_ps1 \" | git %s\") ]\[\\e[0m\\e[K\]\n\[\\e[37;44;1m\][\u@\h \W]\\\$\[\\e[0m\] "
            ;;
        color-lines)
            PS0="$ndim_orig_PS0"
            PS1="\${VIRTUAL_ENV:+\"\\\\\\[\\\\\\r\\\\\\e[K\\\\\\e[37;45;1m\\\\\\]VIRTUAL_ENV \${VIRTUAL_ENV}\\\\\\[\\\\\\e[0m\\\\\\e[K\\\\\\]\\\\\\n\"}\[\\r\\e[K\\e[37;41;1m\][ \t | \\! | \${PIPESTATUS[@]} | \w\$(__git_ps1 \" | git %s\") ]\[\\e[0m\\e[K\]\n\[\\e[37;44;1m\][\u@\h \W]\\\$\[\\e[0m\] "
            ;;
        darkblue)
            PS0="$ndim_orig_PS0"

            # our prompt colors
            text_reset="$(tput sgr0)"
            text_bold="$(tput bold)"
            text_dim=""
            case "$(tput colors)" in
                8) ;;
                *) text_dim="$(tput dim)" ;;
            esac
            text_rev="$(tput rev)"
            text_bg_black="$(tput setab 0)"
            text_bg_darkblue="$(tput setab 0)$(tput setab 17)"
            text_bg_darkgreen="$(tput setab 0)$(tput setab 22)"
            text_bg_darkred="$(tput setab 1)$(tput setab 52)"
            text_bg_magenta="$(tput setab 5)"
            text_fg_red="$(tput setaf 1)$(tput setaf 9)"
            text_fg_green="$(tput setaf 2)$(tput setaf 10)"
            text_fg_yellow="$(tput setaf 3)$(tput setaf 11)"
            text_fg_magenta="$(tput setaf 5)$(tput setaf 13)"
            text_fg_white="$(tput setaf 7)$(tput setaf 15)"

            if [ "$UID" -eq 0 ]
            then
                text_prompt="${text_reset}${text_bg_darkred}${text_fg_white}"
                text_prompt_dim="${text_reset}${text_bg_darkred}"
            else
                text_prompt="${text_reset}${text_bg_darkblue}${text_fg_white}"
                text_prompt_dim="${text_reset}${text_bg_darkblue}"
            fi

            # Print colorized $? and ${PIPESTATUS[@]} as part of $PS1
            colorize_status() {
                local status=$1
                shift
                local pipe_ok=true
                for s
                do
                    if [[ $s != 0 ]]; then pipe_ok=false; break; fi
                done
                # local prefix="\001${text_prompt}${text_dim}\002?\001${text_prompt}"
                local prefix="\001${text_prompt}"
                local color
                local postfix="\001${text_prompt}\002\n"
                if $pipe_ok; then
                    color="${text_fg_green}"
                elif [[ $status == 0 ]]; then
                    color="${text_fg_yellow}${text_bold}"
                else
                    color="${text_fg_red}${text_bold}"
                fi
                if [[ $# -gt 0 ]]; then
                    printf "${prefix}${color}\002$*${postfix}"
                else
                    printf "${prefix}${color}\002$status${postfix}"
                fi
            }

            PS0+="${text_reset}"
            PS1=""

            export VIRTUAL_ENV_DISABLE_PROMPT=1
            PS1+="\${VIRTUAL_ENV:+\"\[${text_prompt_dim}\]venv \${VIRTUAL_ENV} \n\"}"

            PS1+="\[${text_prompt}\]\u@\h:\w"

            PS1+="\$(__git_ps1 \"\[${text_prompt_dim}\] %s\")"
            PS1+="\[${text_prompt}\]\n"

            PS1+="\$(colorize_status \"\$?\" \"\${PIPESTATUS[@]}\") "

            # PS1+="\u@\h"
            PS1+="\\\$\[${text_reset}${text_fg_yellow}\] "
            ;;
        *)
            printf "ndim_prompt: Unknown prompt type: %s\n" "$1"
            return 2
            ;;
    esac
}
ndim-prompt ndim-pipestatus-ml

# End of file.
