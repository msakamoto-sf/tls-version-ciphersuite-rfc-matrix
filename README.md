# tls-version-ciphersuite-rfc-matrix
TLS version : CipherSuite : RFC matrix

最終成果物: https://docs.google.com/spreadsheets/d/1zN7NpyKQyJzmwCfi5mDbSeGyqRqdCRGTVOf2IhSYnSE/edit?usp=sharing

- IANAのCipherSuite 台帳に対して OpenSSL の cipher suite を LEFT OUTER JOIN させて、さらに各 Cipher Suite 毎に初出のRFCを特定 & そのRFCがどのTLS versionへの追加を想定しているかを整理しました。
- 昔の機器とのTLS接続互換性にこだわりたい人向けにどうぞ。
- OpenSSL の cipher suite 名ですが、昔のバージョンでは `EDH-` 始まりになるものがあります。
  - 最新の OpenSSL では `DHE-` 始まりになってたりします。
  - 上記の "main" シートの "OpenSSL name" では新しい方にあわせて `DHE-` 始まりで揃えてます。

ベース資料:

- https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml#tls-parameters-4
- https://testssl.sh/openssl-iana.mapping.html
- `$ openssl ciphers -V -stdname "ALL:eNULL" | sort`
  - CentOS 5.11, openssl-0.9.8
  - CentOS 7.9, openssl-1.0.2k
  - CentOS Stream 8, openssl-1.1.1k