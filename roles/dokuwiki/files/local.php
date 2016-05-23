<?php
/**
 * Dokuwiki's Main Configuration File - Local Settings
 * Date: Mon, 17 Feb 2016 17:19:00 +0000
 */

# Il nome della Wiki
$conf['title'] = 'WiLILiK';

# licenza sotto cui è pubblicato il materiale
$conf['license'] = 'cc-by-sa';

# la lingua del sito
$conf['lang'] = 'it';

# usa la Access Control list, basandosi sui file
# - ​conf/​acl.auth.php
# - ​conf/​users.auth.php
# altre informazioni alla pagina https://www.dokuwiki.org/acl
$conf['useacl'] = 1;

# il nome del nostro admin, usato per accedere
# all'interfaccia web di amministrazione
#$conf['superuser'] = '**************';

# setta il plugin per ldap come
# il metodo di autenticazione di default
# il plugin è incluso con l'installazione di DokuWiki
$conf['authtype'] = 'authldap';

$conf['auth']['ldap']['server'] = 'ldap://ldap.lilik.it';
$conf['auth']['ldap']['port'] = 389;
$conf['auth']['ldap']['usertree'] = 'o=People, dc=lilik, dc=it';
$conf['auth']['ldap']['grouptree'] = 'o=Group, dc=lilik, dc=it';
$conf['auth']['ldap']['userfilter'] = '(&(uid=%{user})(objectClass=posixAccount)(memberOf=cn=wiki,o=Group,dc=lilik,dc=it))';
$conf['auth']['ldap']['groupfilter'] = '(&(objectClass=posixGroup)(|(gidNumber=%{gid})(memberUID=%{user})))';

# magic number
$conf['auth']['ldap']['version'] = '3';
