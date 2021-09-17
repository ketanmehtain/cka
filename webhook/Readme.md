# Admission Controller - Validation Webhook

This documents is to setup Kubernetes validating Admission Controller using python.

In this case we are restricting use of image to nginx, but you can use your own logic to restrict.
 
## Create Certificates

Run the certgen.sh script to create the self-signed certificates for the admission controller validating webhook.
Note - make sure the commonName and DNS.1 (in ext.cnf) name matches with '-sub "/CN=webhook.default.svc" ' (in certgen.sh)

'''
$ mkdir certs
$ sh certgen.sh
Generating RSA private key, 2048 bit long modulus (2 primes)
......+++++
....................................+++++
e is 65537 (0x010001)
Generating RSA private key, 2048 bit long modulus (2 primes)
.........+++++
..+++++
e is 65537 (0x010001)
Signature ok
subject=CN = webhook.default.svc
Getting CA Private Key

'''

## Update Validation webhook with CA bundle

Use webhook-template file to create webhook.yml and he tbase64 value into the caBundle.

'''
$ ca_pem=$(cat certs/ca.crt | base64 -w 0)
$sed -e 's@${CA_PEM}@'"$ca_pem"'@g' < webhook-template.yml > webhook.yml

'''

## Building the Image.

Build the docker image using Dockerfile and upload it to docker hub.

'''
$ docker build . -t <docker-user-id>/image:0.1

'''










