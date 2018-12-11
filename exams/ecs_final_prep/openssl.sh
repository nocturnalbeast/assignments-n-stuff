# Encode in base64
openssl enc -base64 -in inputfile -out outputfile

# Decode from base64
openssl enc -d -base64 -in encodedfile -out decodedfile

# Viewing password and user entries
cat /etc/passwd
cat /etc/shadow

# Useful cut command to filter output
cut -d ":" -f 1

# Getting entry of the specified user
getent passwd | grep username

# Encrypting a file with DES and no salt
openssl enc -des -nosalt -in inputfile -out encryptedfile

# Decrypting an encrypted file with DES and no salt
openssl enc -d -des -nosalt -in encryptedfile -out outputfile

# Generating an RSA key pair
openssl genrsa -out keyfile length_of_key

# Displaying the RSA key pair
openssl rsa -in keyfile -text -noout

# Extracting the public key from the keyfile that contains both public and private key
openssl rsa -in keyfile -pubout -out publickeyfile

# Displaying the public RSA key
openssl rsa -in publickeyfile -pubin -text -noout

# Encrypting a file using the public RSA key
openssl rsautl -encrypt -pubin -inkey publickeyfile -in inputfile -out encryptedfile

# Decrypting an encrypted file using the private RSA key
openssl -rsautl -decrypt -inkey keyfile -in encryptedfile

# Encrypting a file using symmetric encryption method
openssl aes-256-cbc -salt -a -e -in inputfile -out encryptedfile

# Decrypting the encrypted file using a symmetric encryption method
openssl aes-256-cbc -salt -a -d -in encryptedfile -out outputfile

# Generating MD5 digest of a file
openssl dgst -md5 -out hashfile inputfile

# Generating signed digest of a file using private key
openssl dgst -sha512 -sign keyfile -out signeddigestfile inputfile

# Verifying the integrity of a file with the signed digest and the public key
openssl dgst -sha512 -verify publickeyfile -signature signeddigestfile inputfile

# Generating an X.509 certificate with the private key
openssl req -new -key keyfile -out certificatefile

# Viewing the contents of the X.509 certificate
openssl req -in certificatefile -text

# Signing a new certificate using the certificate and the private key
openssl x509 -req -in certificatefile -signkey keyfile -out newcertificatefile