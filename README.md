# Taiga documentation source #

> *Status:* _Still a work in progress_

Web: http://taigaio.github.io/taiga-doc/dist/   

### Setup initial environment (for developers)

Install requirements: Ruby / asciidoctor + pygments.rb

You can install Ruby through the apt package manager, pacman, rbenv, or rvm. 

    $ gem install asciidoctor pygments.rb
    $ export PATH="~/.gem/ruby/2.1.0/bin:$PATH"
    $ asciidoctor -v // should return Asciidoctor 1.5.1 ...

### (Optional) Setup live preview in browser

> _Prerequisite: Initial environment above must be setup and working_

#### Overview

This step is optional but highly recommended in order to ease the process of editing AsciiDoc files, by rendering the HTML from the source `.adoc` file as soon as any modifications are saved - allowing for instant preview in the browser.

The following instructions are based on the Asciidoctor page: [Editing AsciiDoc with Live Preview][1]

#### Installation

Install Guard and the shell file monitor:

    $ gem install guard guard-shell rb-inotify

#### Ensure Guard is working

Confirm that `Guardfile` is in the base `taiga-doc` directory and then start Guard from that directory:

    $ cd taiga-doc
    $ guard start

Open `index.adoc` in a text editor, make a minor modification and then save the file.
If Guard is working properly, `dist/index.html` will be created/updated automatically.

#### Configure live preview in the browser

> _Note: The [Asciidoctor page][1] suggests using LiveReload with the `guard-livereload` gem but this package is [no longer compatible with LiveReload 2][2]_

Simply use a browser that has auto-reload built-in or install a relevant browser add-on.

Examples include:

* [Web][3] web browser (formerly Epiphany web browser) - has built-in auto-reload functionality
* Firefox + [Auto Reload][4] add-on
* _[Please add other working configurations here]_

#### Test live preview

Open `dist/index.html` in the browser.
As before, save a modification to `index.adoc`.
Once Guard has rendered the new copy of `dist/index.html`, the browser will auto-reload the page.

#### Working with live preview

Some tips/notes about working with live preview:

* Position the text editor and web browser windows side-by-side (or on different screens!), save changes and see the result in the browser almost immediately
* Changes to any of the `.adoc` files within the `api/` directory or its sub-dirs will render `dist/api.html` - due to many `.adoc` files being combined to render the single HTML file, there is a slight lag in the live preview as the conversion process completes
* Otherwise, there is a 1:1 relationship between the `.adoc` file and its rendered `.html` file - changes to these are displayed almost instantaneously


[1]: http://asciidoctor.org/docs/editing-asciidoc-with-live-preview/
[2]: http://feedback.livereload.com/knowledgebase/articles/86181-failed-to-start-port-occupied
[3]: https://wiki.gnome.org/Apps/Web
[4]: https://addons.mozilla.org/en-US/firefox/addon/auto-reload/
