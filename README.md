# gen_btc_addr

## Overview
`gen_btc_addr.py` is a Python script that generates Bitcoin private keys, public keys, and corresponding addresses in multiple formats including Base58, compressed, and Bech32. This tool also allows the creation of a QR code for easy sharing of the Bech32 address.

## Features
- Generate Bitcoin **private keys** in hexadecimal, Wallet Import Format (WIF), and Base64.
- Generate **public keys** in uncompressed and compressed formats.
- Create Bitcoin **addresses** in **Base58** (uncompressed and compressed) and **Bech32** formats.
- Generate a **QR code** for the Bech32 address for easy sharing.

## Usage

### Command-Line Arguments
- **`-k <private_key>`**: Optionally specify a private key in hexadecimal format.
  
  Example:
  ```sh
  python3 gen_btc_addr.py -k d984c9947ee1345411c1f6d893265c3808b5e9f82a64dc44f55dff491a575a52
  ```

If no private key is provided, a new one will be randomly generated using secure randomness from `/dev/urandom`.

### Running the Script
Run the script from your command line:
```sh
python3 gen_btc_addr.py
```

Upon running the script, you will see the generated **public** and **private** key details, as well as a QR code image for the Bech32 address saved in the current directory.

## Output
The script will generate:

### Public Information
- **Bitcoin Address (Uncompressed, Base58)**
- **Bitcoin Address (Compressed, Base58)**
- **Public Key (uncompressed Hex)**
- **Public Key (compressed Hex)**
- **Bech32 Address** (QR code is generated for this address)

### Private Information
- **Private Key WIF (uncompressed)**
- **Private Key WIF (Compressed)**
- **Private Key (Hexadecimal)**
- **Private Key (Base64)**

## Dependencies
The script requires the following Python modules:
- `ecdsa`
- `hashlib`
- `base58`
- `base64`
- `bech32`
- `qrcode`
- `Pillow` (for QR code image generation)

You can install these dependencies using `pip`:
```sh
pip install ecdsa base58 bech32 qrcode pillow
```

## Example
Example output from running the script:
```
$ python3 gen_btc_addr.py
PUBLIC:
    Bitcoin Address (Uncompressed, Base58): 16RKYWLsRJBDBsRCe6AGb6z6rzZMJWsRnQ
    Bitcoin Address (Compressed, Base58): 1CxsggUdrajHAnbXkNtgrGsdL5gRUtmtBH
    Public Key (uncompressed Hex): 044dbfc6e4fc193956ec5e56dc8d9dacc3e340c342685445c6dd48aefa027f9ac1334738ad469dd0e2c522dc5aabb4ef4c91298fb7541f0c95f362defc07dab5dd (Length: 130)
    Public Key compressed (Hex): 034dbfc6e4fc193956ec5e56dc8d9dacc3e340c342685445c6dd48aefa027f9ac1 (Length: 66)
    Public Bech32 Address: bc1qsvafyrtpewnxt6jp0zqrxd76q58e9e2dj9v4cq
PRIVATE:
    Private Key WIF (uncompressed): 5KU5odYGakWNCCjUF6gup1apk3ghU3o79jKGtWTi6LtZtJaVFh3 (Length: 51)
    Private Key WIF (Compressed): L4WYCpH1my2cYSnTFE7A6VaHizrDcPLW9Xmf8M2tNanc91Amt64B (Length: 52)
    Private Key (Hex): d984c9947ee1345411c1f6d893265c3808b5e9f82a64dc44f55dff491a575a52 (Length: 64)
    Private Key (Base64): 2YTJlH7hNFQRwfbYkyZcOAi16fgqZNxE9V3/SRpXWlI= (Length: 44)
QR Code for Bech32 address saved as: bitcoin-bc1qsvafyrtpewnxt6jp0zqrxd76q58e9e2dj9v4cq-qrCode.png
```

## License
This project is open source and available under the MIT License.

## Author
David Slimp (rock808@David-Slimp.com)

## Changelog
- **20241012** - Version **0.1.0** - Initial version written from scratch without using the bitcoinlib module.
- **20241013** - Version **0.1.1** - Added QR code generation for Bech32 address.


