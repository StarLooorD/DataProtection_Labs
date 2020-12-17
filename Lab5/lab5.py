from crypto.Hash import SHA256
from crypto.PublicKey import DSA
from crypto.Signature import DSS


def generate_keys(bits, private, public):
    key = DSA.generate(bits=bits)
    with open(private, "wb") as input_file_pr:
        input_file_pr.write(key.exportKey())
    with open(public, "wb") as input_file_pb:
        input_file_pb.write(key.publickey().exportKey())
    return key, key.publickey()


def get_existing_keys(private, public):
    with open(private, 'rb') as file:
        private_key = file.read()
    key = DSA.import_key(private_key)
    with open(public, 'rb') as file:
        public_key = file.read()
    public = DSA.import_key(public_key)
    return key, public


def sign_message(private_key, message):
    h = SHA256.new(message)
    sign = DSS.new(private_key, 'fips-186-3')
    signature = sign.sign(h)
    return signature


def write(file, signature):
    with open(file, 'w') as output:
        output.write(signature.hex())


def read(file):
    with open(file, 'rb') as input:
        message = input.read()
    return message


def verify_certificate(public_key, message, signature):
    message = SHA256.new(message)
    verifier = DSS.new(public_key, 'fips-186-3')

    try:
        verifier.verify(message, signature)
        print("Correct signature")
    except ValueError:
        print("Incorrect signature")
    pass


if __name__ == '__main__':
    key = ''
    public_key = ''
    while 1:
        print("1.Generate keys")
        print("2.Use Existing keys")
        print("3.Sign message from console")
        print("4.Sign message from file")
        print("5.Verify message")
        print("6.Exit")
        choice = int(input("Choose"))
        if choice == 1:
            bits = int(input('Input num of bits '))
            pb = input('Input name of file to save public key ')
            pr = input('Input name of file to save private key ')
            key, public_key = generate_keys(bits, pr, pb)
        if choice == 2:
            pb = input('Input name of file to save public key ')
            pr = input('Input name of file to save private key ')
            key, public_key = get_existing_keys(pr, pb)
        if choice == 3:
            message = str.encode(input('Input message '))
            signature = sign_message(key, message)
            file_choice = input("Want write to file?[y,n]")
            file = input("Input name of file: ")
            write(file, signature)
        if choice == 4:
            file = input('Input name of file ')
            message = read(file)
            signature = sign_message(key, message)
            file_choice = input("Want write to file?[y,n]")
            file = input("Input name of file: ")
            write(file, signature)
        if choice == 5:
            message = str.encode(input('Input message '))
            signature = input('Input name of file of sign ')
            with open(signature, 'r') as file:
                sign = file.read()
            verify_certificate(public_key, message, bytes.fromhex(sign))
        if choice == 6:
            break