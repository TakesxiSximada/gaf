gaf - Github Argument Flow
==========================

::

   ________  ___  _________  ___  ___  ___  ___  ________          ________  ________  ________  ___  ___  _____ ______   _______   ________   _________        ________ ___       ________  ___       __
  |\   ____\|\  \|\___   ___\\  \|\  \|\  \|\  \|\   __  \        |\   __  \|\   __  \|\   ____\|\  \|\  \|\   _ \  _   \|\  ___ \ |\   ___  \|\___   ___\     |\  _____\\  \     |\   __  \|\  \     |\  \
  \ \  \___|\ \  \|___ \  \_\ \  \\\  \ \  \\\  \ \  \|\ /_       \ \  \|\  \ \  \|\  \ \  \___|\ \  \\\  \ \  \\\__\ \  \ \   __/|\ \  \\ \  \|___ \  \_|     \ \  \__/\ \  \    \ \  \|\  \ \  \    \ \  \
   \ \  \  __\ \  \   \ \  \ \ \   __  \ \  \\\  \ \   __  \       \ \   __  \ \   _  _\ \  \  __\ \  \\\  \ \  \\|__| \  \ \  \_|/_\ \  \\ \  \   \ \  \       \ \   __\\ \  \    \ \  \\\  \ \  \  __\ \  \
    \ \  \|\  \ \  \   \ \  \ \ \  \ \  \ \  \\\  \ \  \|\  \       \ \  \ \  \ \  \\  \\ \  \|\  \ \  \\\  \ \  \    \ \  \ \  \_|\ \ \  \\ \  \   \ \  \       \ \  \_| \ \  \____\ \  \\\  \ \  \|\__\_\  \
     \ \_______\ \__\   \ \__\ \ \__\ \__\ \_______\ \_______\       \ \__\ \__\ \__\\ _\\ \_______\ \_______\ \__\    \ \__\ \_______\ \__\\ \__\   \ \__\       \ \__\   \ \_______\ \_______\ \____________\
      \|_______|\|__|    \|__|  \|__|\|__|\|_______|\|_______|        \|__|\|__|\|__|\|__|\|_______|\|_______|\|__|     \|__|\|_______|\|__| \|__|    \|__|        \|__|    \|_______|\|_______|\|____________|



install
-------

Next, execute command.::

    $ pip install gaf

How to use
----------

Create labels for gaf::

  $ gaf init

Create issue and new branch::

  $ gaf create TITLE

Fix issue and create pull request::

  $ gaf fix TITLE

Create release branch and bump versin::

  $ gaf release draft VERSION -m TITLE

Create pre release branch and bump versin::

  $ gaf release draft VERSION -m TITLE --pre

Display release branch list::

  $ gaf release list

Accept pull request::

  $ gaf release accept URL

Reject pull request::

  $ gaf release reject URL MESSAGE

Request rebas to pull request::

  $ gaf release be rebase URL

Request squash to pull request::

  $ gaf release be squash URL

Fix release::

  $ gaf release publish

Create hotfix::

  $ gaf hotfix create

Create hotfix::

  $ gaf hotfix finish
