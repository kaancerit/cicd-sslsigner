# cicd-sslsigner

Sample usage:

ansible-playbook ssl.pb -e CNAME="mysslurl.mycompany.com" -e ANAME="companyidentity"

playbook generates following files,
CSR (Certificate Request)
KEY (Private Key)
P7B (Certificate file in PKCS#7)
PEM (Converted from P7B)
JKS (Java Key Store)

playbook requires following extras,
CNAME (Common Name) (it generates -1 and -2 as a subject alernates names for multiple datacenter usage)
ANAME (Alias Name for JKS) you can remove from playbook if its not required
