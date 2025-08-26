from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from pathlib import Path

def generate_keys():
    key_dir = Path("Keys")
    key_dir.mkdir(exist_ok=True)

    # ES256 = ECDSA with curve secp256r1 (prime256v1)
    private_key = ec.generate_private_key(ec.SECP256R1())

    # Save private key
    with open(key_dir / "ec_private.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save public key
    public_key = private_key.public_key()
    with open(key_dir / "ec_public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    print("ES256 Keys generated successfully in 'Keys/' directory.")

if __name__ == "__main__":
    generate_keys()