****************************
Mopidy-SpotiTube
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-SpotiTube
    :target: https://pypi.org/project/Mopidy-SpotiTube/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/github/workflow/status/natumbri/mopidy-spotitube/CI
    :target: https://github.com/natumbri/mopidy-spotitube/actions
    :alt: CI build status

.. image:: https://img.shields.io/codecov/c/gh/natumbri/mopidy-spotitube
    :target: https://codecov.io/gh/natumbri/mopidy-spotitube
    :alt: Test coverage

Mopidy extension for playing Spotify users' public playlists using mopidy-youtube


Installation
============

Install by running::

    python3 -m pip install https://github.com/natumbri/mopidy-youtube/archive/master.zip
    (TODO: python3 -m pip install Mopidy-SpotiTube)

TODO: See https://mopidy.com/ext/spotitube/ for alternative installation methods.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-SpotiTube to your Mopidy configuration file::

    [spotitube]
    enabled = true
    spotify_users = 
      spotify_user_id_1
      spotify_user_id_2
      ...
      spotify_user_id_n

where spotify_user_id_1 ... n are each a spotify user id, which can be found in a spotify url::
    https://open.spotify.com/user/{spotify_user_id}

That's it.  No OAuth, no keys, no passwords, no accounts.


Project resources
=================

- `Source code <https://github.com/natumbri/mopidy-spotitube>`_
- `Issue tracker <https://github.com/natumbri/mopidy-spotitube/issues>`_
- `Changelog <https://github.com/natumbri/mopidy-spotitube/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Nik Tumbri <https://github.com/natumbri>`__
- Current maintainer: `Nik Tumbri <https://github.com/natumbri>`__
- `Contributors <https://github.com/natumbri/mopidy-spotitube/graphs/contributors>`_
