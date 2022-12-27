" map the leader key
let mapleader="\\" " set to backslash

" vim-plug
call plug#begin()

  " syntax highlighting
  Plug 'peterhoeg/vim-qml'

  " editing
  Plug 'preservim/nerdcommenter'
  Plug 'godlygeek/tabular'

  " lsp ans asyncomplete
  Plug 'prabirshrestha/vim-lsp'
  Plug 'mattn/vim-lsp-settings'
  Plug 'prabirshrestha/asyncomplete-lsp.vim'
  Plug 'prabirshrestha/asyncomplete.vim'
  Plug 'prabirshrestha/async.vim'

  " language servers:
  Plug 'keremc/asyncomplete-clang.vim'

call plug#end()

" asyncomlete
inoremap <expr> <Tab>   pumvisible() ? "\<C-n>" : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <expr> <cr>    pumvisible() ? asyncomplete#close_popup() : "\<cr>"
imap <c-space> <Plug>(asyncomplete_force_refresh)

" asyncomplete-clang
autocmd User asyncomplete_setup call asyncomplete#register_source(
   \ asyncomplete#sources#clang#get_source_options())

" fast save and close
nmap <leader>w :w<CR>
nmap <leader>x :x<CR>
nmap <leader>q :q<CR>

syntax enable                " enable syntax processing

" spaces and tabs
set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab
set autoindent
set copyindent

" search
set incsearch
set hlsearch
set ignorecase
set smartcase

" UI config
set hidden
set number
set relativenumber
set scrolloff=6
set noswapfile
set nowrap

" old vimscript config without a clear category
set encoding=utf-8
set nocompatible
filetype on
filetype plugin on
set noerrorbells
set wildmode=longest,list
set backupdir=~/.cache/vim

