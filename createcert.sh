#!/bin/bash
#===============================================================================
#
#          FILE:  createcert.sh
# 
#         USAGE:  ./createcert.sh 
# 
#   DESCRIPTION:  create server/client certs
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  acidwars (), kerberos@tekkno.me
#       COMPANY:  
#       VERSION:  1.0
#       CREATED:  03/11/2017 12:34:10 AM CET
#      REVISION:  ---
#===============================================================================

openssl genrsa -des3 -out ca.key 4096
openssl req -new -x509 -days 365 -key ca.key -out ca.crt
openssl genrsa -des3 -out client.key 4096
openssl req -new -key client.key -out client.csr
openssl x509 -req -days 365 -in client.csr -CA ca.crt  -CAkey ca.key  -set_serial 01 -out client.crt

