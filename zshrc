# zoomer shell config by huell8

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.config/oh-my-zsh"

export PATH=$PATH:$HOME/.bin
export PATH=$PATH:$HOME/.emacs.d/bin # doom emacs scripts
export PATH=$PATH:$HOME/.cargo/bin # default location of cargo compiled binaries
export PATH=$PATH:$HOME/.local/bin # default location of pip3 installed binaries

# theme
ZSH_THEME="fishy"

zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# plugins
plugins=(
	vi-mode
	dirhistory
	history
	copypath
	copyfile
	copybuffer # Ctrl+O
)

# vi-mode settings
VI_MODE_RESET_PROMPT_ON_MODE_CHANGE=true
VI_MODE_SET_CURSOR=false
VI_MODE_INDICATOR=">>>"

# correction
ENABLE_CORRECTION="true"
HYPHEN_INSENSITIVE="true"
# CASE_SENSITIVE="true"

HISTSIZE=16384
SAVEHIST=16384
HISTFILE=~/.cache/zsh/history
ZSH_COMPDUMP="$HOME/.cache/zcompdump/.zcompdump-${SHORT_HOST}-${ZSH_VERSION}"

source $ZSH/oh-my-zsh.sh

# aliases
alias view="sxiv"
alias emacs="emacsclient -c -a 'emacs'"
alias vim="nvim"
alias ll="ls -lAbhFqv --group-directories-first"
alias ss="escrotum --select --clipboard"
alias ssf="escrotum --select /home/huell/Downloads/screenshot.png"
alias celar="clear"
alias cealr="clear"
alias rm="rm -i"
alias mv="mv -i"
alias cp="cp -i"
# pacman
alias p="sudo pacman"
alias P="yes | sudo pacman"
alias Suy="yes | sudo pacman -Suy"
# global
alias -g LL="2>&1 | less"
alias -g NE="2>/dev/null"
alias -g NUL=">/dev/null 2>&1"


# scripts {
	# riced ls
	alias l="riced_ls"
	function riced_ls() {
		if [ $(ls -A | wc -l) -lt 10 ]; then
			ls -lAbhFqv --group-directories-first
		else
			echo -n "dotfiles hidden; "
			ls -lbhFqv --group-directories-first
		fi
	}
	# python bash calculator for simple operations
	alias math="noglob evaluate_math"
	function evaluate_math() {
		QUERY=''
		for i in "$@"; do
			QUERY="$QUERY$i"
		done
		python3 -c "from math import *; print($QUERY)"
	}
	# nice tui for shutdown, reboot and halt
	alias shutdown="shutdowntui"
	alias poweroff="shutdowntui"
	alias reboot="shutdowntui"
	alias halt="shutdowntui"
	function shutdowntui() {
		echo "(s)hutdown, (r)eboot or (h)alt? (q)uit"
		read RESPONSE

		case "$RESPONSE" in
			s)        EXE="sudo shutdown --poweroff now";;
			shutdown) EXE="sudo shutdown --poweroff now";;
			r)        EXE="sudo shutdown --reboot now";;
			reboot)   EXE="sudo shutdown --reboot now";;
			h)        EXE="sudo shutdown --halt now";;
			halt)     EXE="sudo shutdown --halt now";;
			*)        exit 0;;
		esac

		sh -c "$EXE"
	}
# }
