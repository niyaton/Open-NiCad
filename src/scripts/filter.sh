#!/bin/bash 
# Generic NiCad filtering script
#
# Usage:  Filter granularity language pcfile.xml nonterminals ...
#           where granularity is one of:  { functions blocks ... }
#           and   language    is one of:  { c java cs py ... }
#           and   pcfile.xml  is an extracted potential clones file
#           and   nonterminals is any set of language nonterminal type names

# Revised 1.10.18

ulimit -s hard

# Find our installation
lib="${0%%/scripts/filter.sh}"
if [ ! -d ${lib} ]
then
    echo "*** Error:  cannot find NiCad installation ${lib}"
    echo ""
    exit 99
fi

# check granularity
if [ "$1" != "" ]
then
    granularity=$1
    shift
else
    echo "Usage:  Filter granularity language pcfile.xml nonterminals ..."
    echo "          where granularity is one of:  { functions blocks ... }"
    echo "          and   language    is one of:  { c java cs py ... }"
    echo "          and   pcfile.xml  is an extracted potential clones file"
    echo "          and   nonterminals is any set of language nonterminal type names"
    exit 99
fi

# check language
if [ "$1" != "" ] 
then
    language=$1
    shift
else
    echo "Usage:  Filter granularity language pcfile.xml nonterminals ..."
    echo "          where granularity is one of:  { functions blocks ... }"
    echo "          and   language    is one of:  { c java cs py ... }"
    echo "          and   pcfile.xml  is an extracted potential clones file"
    echo "          and   nonterminals is any set of language nonterminal type names"
    exit 99
fi

# check we have a potential clones file
if [ "$1" != "" ]
then
    pcfile="${1%%.xml}"
    shift
else
    pcfile=""
fi

if [ ! -s "${pcfile}.xml" ]
then
    echo "Usage:  Filter granularity language pcfile.xml nonterminals ..."
    echo "          where granularity is one of:  { functions blocks ... }"
    echo "          and   language    is one of:  { c java cs py ... }"
    echo "          and   pcfile.xml  is an extracted potential clones file"
    echo "          and   nonterminals is any set of language nonterminal type names"
    exit 99
fi

# check we have at least one nonterminal
if [ "$1" != "" ]
then
    nonterminals="$*"
else
    echo "Usage:  Filter granularity language pcfile.xml nonterminals ..."
    echo "          where granularity is one of:  { functions blocks ... }"
    echo "          and   language    is one of:  { c java cs py ... }"
    echo "          and   pcfile.xml  is an extracted potential clones file"
    echo "          and   nonterminals is any set of language nonterminal type names"
    exit 99
fi 

# check we have the filter we need
if [ ! -s ${lib}/txl/${language}-filter-${granularity}.x ]
then
    echo "*** ERROR: ${granularity} filtering not supported for ${language}"
    exit 99
fi

# Clean up any previous results
/bin/rm -f "${pcfile}-filter.xml"

# Filter potential clones
date
echo "${lib}/tools/streamprocess.x '${lib}/txl/${language}-filter-${granularity}.x stdin - ${nonterminals}' < ${pcfile}.xml > ${pcfile}-filter.xml"
time ${lib}/tools/streamprocess.x "${lib}/txl/${language}-filter-${granularity}.x stdin - ${nonterminals}" < "${pcfile}.xml" > "${pcfile}-filter.xml"

result=$?

echo ""
date
echo ""

exit $result
