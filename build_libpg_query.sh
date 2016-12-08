#!/bin/bash -e
# From https://github.com/alculquicondor/psqlparse/blob/master/build_libpg_query.sh

LIBPGQUERYDIR='libpg_query-9.5-latest'
LIBPGQUERYZIP='libpg_query-9.5-latest.zip'

if [ ! -d $LIBPGQUERYDIR ]; then
    curl -L -o $LIBPGQUERYZIP https://github.com/lfittl/libpg_query/archive/9.5-latest.zip
    unzip $LIBPGQUERYZIP
    rm $LIBPGQUERYZIP
fi

cd $LIBPGQUERYDIR
make || exit $?
