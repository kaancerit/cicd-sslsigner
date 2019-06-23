- hosts: localhost
  gather_facts: no
  tasks:
  - name: Create Openssl domain key
    openssl_privatekey: path="/tmp/{{ CNAME }}.key" size=4096 type=RSA
  - name: CSR Create
    openssl_csr:
      path: "/tmp/{{ CNAME }}.csr"
      privatekey_path: "/tmp/{{ CNAME }}.key"
      subject_alt_name: 'DNS:{{ CNAME }},DNS:{{ CNAME }}-1,DNS:{{ CNAME }}-2'
      country_name: TR
      state_or_province_name: ISTANBUL
      locality_name: ISTANBUL
      organization_name: My Company
      organizational_unit_name: My Company
      common_name: "{{ CNAME }}"
  - name: SSL Signing
    casigner:
      url: "http://120.10.1.10/certsrv/"
      user: "domainusername"
      password: "domainpassword"
      domain: "domainname"
      csr: "{{lookup('file', '/tmp/{{ CNAME }}.csr') }}"
      outpath: "/tmp/{{ CNAME }}.p7b"
  - name: Converting from P7B to PEM
    command: openssl pkcs7 -print_certs -in /tmp/{{ CNAME }}.p7b -out /tmp/{{ CNAME }}.cer
  - name: Create JKS
    java_keystore:
      name: "{{ ANAME }}"
      certificate: "{{lookup('file', '/tmp/{{ CNAME }}.cer') }}"
      private_key: "{{lookup('file', '/tmp/{{ CNAME }}.key') }}"
      password: changeit
      dest: /tmp/{{ CNAME }}_identity_keystore.jks
