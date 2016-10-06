python-fedex legacy documentation
=================================

This directory contains legacy build scripts for python-fedex documentation
using epydoc 3.0.1. The following was used to generate doc:

    cd python-fedex/docs
    epydoc -v -o 2.X.X ../fedex/

The epydoc documentation is hosted at https://pythonhosted.org/fedex/.

Latest documentation is now generated using Sphinx. Updates can be made to the
*.rst files in doc_src:

   cd python-fedex/doc_src
