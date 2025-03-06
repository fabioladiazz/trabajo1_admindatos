import hashlib
password = "acceso3"
hashed_password = hashlib.sha256(password.encode()).hexdigest()
print("SHA-256 hash de 'password1234':", hashed_password)


