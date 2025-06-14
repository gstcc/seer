" vimrc - for local plugin dev
let &runtimepath.=','.escape(fnamemodify(resolve(expand('<sfile>:p')), ':h'), '\,')
filetype plugin indent on
syntax on

" Optional logging
let g:python3_host_prog = expand('./venv/bin/python')

" Automatically register plugins
autocmd VimEnter * UpdateRemotePlugins
