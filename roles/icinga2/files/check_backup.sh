#!/bin/bash

PROGNAME=$(basename $0)
PROGPATH=$(echo $0 | sed -e 's,[\\/][^\\/][^\\/]*$,,')

. $PROGPATH/utils.sh

print_usage() {
    echo "Usage: $PROGNAME -R repo [-d log_dir] [-w warning_age] [-c critical_age]"
    echo "Usage: $PROGNAME --help"
}

print_help() {
    echo ""
    exit $STATE_OK
}

logdir=/var/log/backup-status
wage=93600 # 26h
cage=187200 # 52h
repo=""

while test -n "$1"; do
    case "$1" in
	--help|-h)
	    print_help
	    exit $STATE_OK
	    ;;
        --repo|-R)
	    repo=$2
	    shift
	    ;;
	--dir|-d)
	    logdir=$2
	    shift
	    ;;
	--wage|-w)
	    wage=$2
	    shift
	    ;;
	--cage|-c)
	    cage=$2
	    shift
	    ;;
	*)
	    echo "Unknown argument: $1"
	    print_usage
	    exit $STATE_UNKNOWN
	    ;;
    esac
    shift
done

if [ "$repo" == "" ] or [ -d "$logdir/$repo" ]; then
    echo "Unknown repo $repo."
    exit $STATE_UNKNOWN

fi
perf=""
message=""
warning=0
critical=0
unknown=0

for i in $logdir/$repo/*; do
    IFS='|' read -ra STATE < $i
    ENTRY=$(basename $i)
    END=${STATE[0]}
    START=${STATE[1]}
    BACKUP_RC=${STATE[2]}
    PRUNE_RC=${STATE[3]}
    AGE=$(( $(date +%s) - ${START} ))
    DURATION=$(( ${END} - ${START} ))

    case "$BACKUP_RC" in
	0)
	    ;;
	1)
	    warning=1
	    message="${message} - [ Backup of ${ENTRY} returned 1. ]"
            ;;
	*)
	    critical=1
	    message="${message} - [ Backup of ${ENTRY} returned ${BACKUP_RC}. ]"
	    ;;
    esac

    case "$PRUNE_RC" in
	0)
	    ;;
	1)
	    warning=1
	    message="${message} - [ Prune of ${ENTRY} returned 1. ]"
            ;;
	*)
	    critical=1
	    message="${message} - [ Prune of ${ENTRY} returned ${PRUNE_RC}. ]"
	    ;;
    esac

    if [ "${AGE}" -gt "${cage}" ]; then
	critical=1
	message="${message} - [ Age of ${ENTRY} is CRITICAL ]"
    elif [ "${AGE}" -gt "${wage}" ]; then
	warning=1
	message="${message} - [ Age of ${ENTRY} is WARNING ]"
    fi

    perf="${perf}${ENTRY}/age=${AGE}s;${wage};${cage};0;${cage} "
    perf="${perf}${ENTRY}/duration=${DURATION}s;;0;3600 "

done

if [ "$critical" == "1" ]; then
    echo "BACKUP CRITICAL${message}|${perf}"
    exit $STATE_CRITICAL
elif [ "$warning" == "1" ]; then
    echo "BACKUP WARNING${message}|${perf}"
    exit $STATE_WARNING
else
    echo "BACKUP OK|${perf}"
    exit $STATE_OK
fi

exit $STATE_UNKNOWN
