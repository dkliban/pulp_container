Pulp Docker Plugin
==================

The ``pulp_docker`` plugin extends `pulpcore <https://pypi.python.org/pypi/pulpcore/>`__ to support
hosting containers and container metadata, supporting ``docker pull`` and ``podman pull``.

If you are just getting started, we recommend getting to know the :doc:`basic
workflows<workflows/index>`.

How to use these docs
---------------------

The documentation here should be considered **the primary documentation for managing container
related content**. All relevent workflows are covered here, with references to some pulpcore
supplemental docs. Users may also find `pulpcore's conceptual docs
<https://docs.pulpproject.org/en/3.0/nightly/concepts.html>`_ useful.

This documentation falls into two main categories:

  1. :ref:`workflows-index` show the **major features** of the docker plugin, with links to
     reference docs.
  2. `REST API Docs <restapi.html>`_ are automatically generated and provide more detailed
     information for each **minor feature**, including all fields and options.

Container Workflows
-------------------

.. toctree::
   :maxdepth: 1

   installation
   workflows/index
   restapi/index
   release-notes/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
