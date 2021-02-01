# Taiga documentation source #

[![Kaleidos Project](http://kaleidos.net/static/img/badge.png)](https://github.com/kaleidos "Kaleidos Project")
[![Managed with Taiga.io](https://img.shields.io/badge/managed%20with-TAIGA.io-709f14.svg)](https://tree.taiga.io/project/taiga/ "Managed with Taiga.io")

Web: https://taigaio.github.io/taiga-doc/dist/

### Setup initial environment (for developers)

Install requirements: Ruby / `asciidoctor` + `pygments.rb` (installed via. `bundler` using the provided `Gemfile`)

You can install Ruby through the apt package manager, pacman, rbenv, or rvm.

Confirm that `Gemfile` is in the base `taiga-doc` directory, and then perform the installation from that directory:

    $ cd taiga-doc
    $ export PATH=$(ruby -e "print Gem.user_dir")"/bin:$PATH"
    $ export GEM_HOME=$(ruby -e 'print Gem.user_dir')
    $ gem install bundler
    $ bundle
    $ asciidoctor -v // should return Asciidoctor 1.5.1 ...

### (Optional) Regenerating curls and json responses

Taiga doc includes a django app that helps us generate the curl commands and
the json responses from the api. To use it, you have to activate your
taiga-back virtualenv, and install the `generate_api_documents`.

    $ workon taiga
    $ cd generate_api_documents_app
    $ pip install -e .

Now add it to your taiga settings installed apps; Modify in taiga-back your
`settings/local.py` and include the line:

```python
INSTALLED_APPS += ["generate_api_documents"]
```

For generating api examples you need to apply this settings:

- Disable debug mode
  ```
  DEBUG=False
  ```
- Enable public register
  ```
  PUBLIC_REGISTER_ENABLED = True
  ```
- Use dummy email backend (recommended)
  ```
  EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
  ```
- Disable API throttling
  ```
  REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
      "anon-write": None,
      "user-write": None,
      "anon-read": None,
      "user-read": None,
      "import-mode": None,
      "import-dump-mode": None,
      "create-memberships": None,
      "login-fail": None,
      "register-success": None,
      "user-detail": None,
      "user-update": None,
  }
  ```
- Enable system stats
  ```
  STATS_ENABLED = True
  ```
- Enable the following importers:
  ```python
  IMPORTERS["github"]
  IMPORTERS["trello"]
  IMPORTERS["jira"]
  ```
  If you copied local.py.example, uncommenting the importers code should be enough.

Now regenerate the taiga-back database with the sample data:

    $ cd taiga-back
    $ workon taiga
    $ bash regenerate.sh
    $ python manage.py runserver

And finally, in a new terminal, run the `generate_api_examples`
 django command:

    $ cd taiga-back
    $ workon taiga
    $ python manage.py generate_api_examples

If you get some error, check your settings and regenerate the database again.

After that, you have to copy the content generated in the output directory to
the api/generated/ directory in taiga-doc:

    $ mv output/* ../taiga-doc/api/generated/

### Generate the documentation

Check the `Makefile` in order to have all the files indexed and now you can rebuild your documentation running `make`:

    $ make

The result will appear in the `dist` directory.

### (Optional) Setup live preview in browser

> _Prerequisite: Initial environment above must be setup and working_

#### Overview

This step is optional but highly recommended in order to ease the process of editing AsciiDoc files, by rendering the HTML from the source `.adoc` file as soon as any modifications are saved - allowing for instant preview in the browser.

The following instructions are based on:
* The Asciidoctor page: [Editing AsciiDoc with Live Preview][1]
* The Guard README: [Guard: README.md][5]

#### Installation

If the `bundler` install completed successfully, all of the gems will already be in place (including both Guard and the shell file monitor).

For notifications to work properly:
> You have to install the libnotify-bin package with your favorite package manager
>
> -- [Guard: System notifications - Libnotify][6]

For example, on a Debian-based system:

    $ sudo apt-get install libnotify-bin

Or in Arch

    $ yaourt -S libnotify

#### Ensure Guard is working

> It's important that you always run Guard through Bundler to avoid errors.
>
> -- [Guard: README.md][5]

Confirm that `Guardfile` is in the base `taiga-doc` directory and then start Guard from that directory:

    $ cd taiga-doc
    $ bundle exec guard

* Open `index.adoc` in a text editor, make a minor modification and then save the file
* If Guard is working properly, `dist/index.html` will be created/updated automatically
* If `libnotify` is configured correctly, a notification will be shown confirming that `index.adoc` has been found and rendered accordingly

#### Configure live preview in the browser

> _Note: The [Asciidoctor page][1] suggests using LiveReload with the `guard-livereload` gem but this package is [no longer compatible with LiveReload 2][2]_

Simply use a browser that has auto-reload built-in or install a relevant browser add-on.

Examples include:

* [Web][3] web browser (formerly Epiphany web browser) - has built-in auto-reload functionality
* Firefox + [Auto Reload][4] add-on
* _[Please add other working configurations here]_

#### Test live preview

* Open `dist/index.html` in the browser
* As before, save a modification to `index.adoc`
* Once Guard has rendered the new copy of `dist/index.html`, the browser will auto-reload the page

#### Working with live preview

Some tips/notes about working with live preview:

* Position the text editor and web browser windows side-by-side (or on different screens!), save changes and see the result in the browser almost immediately
* Changes to any of the `.adoc` files within the `api/` directory or its sub-dirs will render `dist/api.html` - since many `.adoc` files are combined to render the single HTML file, there is a slight lag in the live preview as the conversion process completes
* Otherwise, there is a 1:1 relationship between the `.adoc` file and its rendered `.html` file - changes to these are displayed almost instantaneously

## Documentation

Currently, we have authored three main documentation hubs:

- **[API](https://taigaio.github.io/taiga-doc/dist/api.html)**: Our API documentation and reference for developing from Taiga API.
- **[Documentation](https://taigaio.github.io/taiga-doc/dist/)**: If you need to install Taiga on your own server, this is the place to find some guides.
- **[Taiga Resources](https://resources.taiga.io)**: This page is intended to be the support reference page for the users.

## Bug reports

If you **find a bug** in Taiga you can always report it:

- in [Taiga issues](https://tree.taiga.io/project/taiga/issues). **This is the preferred way**
- in [Github issues](https://github.com/taigaio/taiga-doc/issues)
- send us a mail to support@taiga.io if is a bug related to [tree.taiga.io](https://tree.taiga.io)
- send us a mail to security@taiga.io if is a **security bug**

One of our fellow Taiga developers will search, find and hunt it as soon as possible.

Please, before reporting a bug, write down how can we reproduce it, your operating system, your browser and version, and if it's possible, a screenshot. Sometimes it takes less time to fix a bug if the developer knows how to find it.

## Community

If you **need help to setup Taiga**, want to **talk about some cool enhancemnt** or you have **some questions**, please write us to our [mailing list](https://groups.google.com/d/forum/taigaio).

If you want to be up to date about announcements of releases, important changes and so on, you can subscribe to our newsletter (you will find it by scrolling down at [https://taiga.io](https://www.taiga.io/)) and follow [@taigaio](https://twitter.com/taigaio) on Twitter.

## Contribute to Taiga

There are many different ways to contribute to Taiga's platform, from patches, to documentation and UI enhancements, just find the one that best fits with your skills. Check out our detailed [contribution guide](https://resources.taiga.io/extend/how-can-i-contribute)

## Code of Conduct

Help us keep the Taiga Community open and inclusive. Please read and follow our [Code of Conduct](https://github.com/taigaio/code-of-conduct/blob/master/CODE_OF_CONDUCT.md).

## License

Every code patch accepted in Taiga codebase is licensed under [AGPL v3.0](http://www.gnu.org/licenses/agpl-3.0.html). You must be careful to not include any code that can not be licensed under this license.

Please read carefully [our license](https://github.com/taigaio/taiga-doc/blob/master/LICENSE) and ask us if you have any questions as well as the [Contribution policy](https://github.com/taigaio/taiga-doc/blob/master/CONTRIBUTING.md).


[1]: http://asciidoctor.org/docs/editing-asciidoc-with-live-preview/
[2]: http://feedback.livereload.com/knowledgebase/articles/86181-failed-to-start-port-occupied
[3]: https://wiki.gnome.org/Apps/Web
[4]: https://addons.mozilla.org/en-US/firefox/addon/auto-reload/
[5]: https://github.com/guard/guard#guard
[6]: https://github.com/guard/guard/wiki/System-notifications#libnotify
