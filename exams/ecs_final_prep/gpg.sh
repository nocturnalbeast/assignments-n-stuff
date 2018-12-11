# To generate a key:
gpg --full-generate-key

# To list all keys:
gpg --list-secret-keys
gpg --list-keys

# To export your key to a keyfile:
gpg --armor --export --output keyfile.gpg email_id

# To encrypt your file using your public key:
gpg -e -r email_id file_name

# To decrypt an encrypted file using your private key:
gpg -d -o decrypted_file_name encrypted_file_name