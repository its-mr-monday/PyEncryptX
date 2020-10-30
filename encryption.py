#
#
#   EncryptX encryption module v1.1
#
#
#

salt = b'\xbe\x82aH\xfa\xc8\x8d_2\x91\xbe~a\x9e7X'
import base64
import lib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def encode_passw(passw):    #encode passw for key creation
    return passw.encode()

def make_kdf():     #generate kdf salt
    return PBKDF2HMAC(algorithm=hashes.SHA256, length=32,salt=salt, iterations=100000, backend=default_backend())

def generateKey(password, kdf):     #generate a key from passw and kdf salt
    key_b64 = base64.urlsafe_b64encode(kdf.derive(password)).decode()
    #print(key_b64)
    return Fernet(key_b64)

def encryptFile(filename, file_path, full_filepath, key):   #encrypt a file with a key
    if lib.checkExistance(filename) is True:
        try:
            with open(full_filepath, 'rb') as f:
                e_file = f.read()
            encrypted_file = key.encrypt(e_file)
            with open(file_path+"/encrypted_"+filename, 'wb') as ef:
                ef.write(encrypted_file)
            f.close()
            ef.close()
            return 0
        except BaseException as e:
            return 1
    else:
        return 1

def decryptFile(filename, file_path, full_filepath, key):   #decrypt a file with a key
    if lib.checkExistance(full_filepath) is True:
        try:
            with open(full_filepath, 'rb') as f:
                ef_file = f.read()
            decrypted_file = key.decrypt(ef_file)
            with open(file_path+"/decrypted_"+filename, 'wb') as ed:
                ed.write(decrypted_file)
            f.close()
            ed.close()
            return 0
        except BaseException as e:
            return 1
    else:
        return 1
    