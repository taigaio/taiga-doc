# Taiga documentation source #

Status: Still a work in Progress
Web:

### Setup initial environment (for developers)

Install requirements: Ruby / asciidoctor + pygments.rb

You can install Ruby through the apt package manager, pacman, rbenv, or rvm. 

    $ gem install asciidoctor pygments.rb
    $ export PATH="~/.gem/ruby/2.1.0/bin:$PATH"
    $ asciidoctor -v // should return Asciidoctor 1.5.1 ...
