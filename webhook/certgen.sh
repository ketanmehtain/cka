openssl genrsa -out certs/ca.key 2048
openssl req -new -x509 -days 365 -key certs/ca.key -out certs/ca.crt -config ext.cnf
openssl genrsa -out certs/webhook-key.pem 2048
openssl req -new -key certs/webhook-key.pem -subj "/CN=webhook.default.svc" -out certs/webhook.csr -config ext.cnf 
openssl x509 -req -days 365 -in certs/webhook.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/webhook-crt.pem
