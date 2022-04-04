# NEVER USE: ECB is not secure!
#this program was made by Tabitha Rowland 
#february 14 2022
#It will swap one or more blocks of ciphertext of a message with the 
# respective blocks from a different ciphertext, demonstrating that when 
# using ECB mode, block ciphers can easily be forged

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import random

# Alice and Bob's Shared Key
test_key = bytes.fromhex('00112233445566778899AABBCCDDEEFF')

aesCipher = Cipher(algorithms.AES(test_key),
                   modes.ECB(),
                   backend=default_backend())
aesEncryptor = aesCipher.encryptor()
aesDecryptor = aesCipher.decryptor()

#hardcoded messages for requirement 2, option 1
#message 1 is old message, message 2 is new
message1 = b"""
FROM: FIELD AGENT ROBIN
TO: FIELD AGENT BOBBY
RE: Meeting
DATE: 2001-01-01

Meet me today at the docks at 1000."""


message2 = b"""
FROM: FIELD AGENT ALICE
TO: FIELD AGENT BOBBY
RE: Meeting
DATE: 2001-11-02

Meet me today at the house at 2000."""
#end of messages for pt2

#alice to bobby 
message3 = b""" 
FROM: FIELD AGENT ALICE
TO: FIELD AGENT BOBBY
RE: Meeting
DATE: 2001-11-02

Meet me today at the house at 2000."""


#SWAPPING SENDER
message4 = b"""
FROM: FIELD AGENT ROBIN
TO: FIELD AGENT BOBBY
RE: Meeting
DATE: 2001-11-02

Meet me today at the house at 2000."""


#SWAPPING RECIEVER
message5 = b"""
FROM: FIELD AGENT ALICE
TO: FIELD AGENT ROBIN
RE: Meeting
DATE: 2001-11-02

Meet me today at the house at 2000."""

#SWAPPING DATE
message6 = b"""
FROM: FIELD AGENT ALICE
TO: FIELD AGENT BOBBY
RE: Meeting
DATE: 2001-20-02

Meet me today at the house at 0600."""

#SWAPPING PLACE
message7 = b"""
FROM: FIELD AGENT ALICE
TO: FIELD AGENT BOBBY
RE: Meeting
DATE: 2001-11-02

Meet me today at the docks at 0600."""


#block1start, block1end, block2start, block2end, block1continued
def change_block(message_old, message_changed, blockNumber):

    message_old += b"E" * (-len(message_old) % 16)
    ciphertext1 = aesEncryptor.update(message_old)
    message_changed += b"E" * (-len(message_changed) % 16)
    ciphertext2 = aesEncryptor.update(message_changed) 
    ciphertext2 = ciphertext2.hex()
    ciphertext1 = ciphertext1.hex() 
    blockStart = (blockNumber * 32 ) - 1
    blockEnd = (blockNumber * 32) + 32
    if blockNumber == 0: #not sure if this is necessary but putting it incase
        finalcipher = ciphertext1[:32] + ciphertext2[32:]
        finalcipher = bytes.fromhex(ciphertext2)
        finalcipher = aesDecryptor.update(finalcipher)
        return finalcipher

    elif blockNumber == 6: 
        finalcipher = ciphertext2[0:blockStart] + ciphertext1[blockStart:]
        finalcipher = bytes.fromhex(ciphertext2)
        finalcipher = aesDecryptor.update(finalcipher)
        return finalcipher
        

    elif blockNumber == 1 or 2 or 3 or 4 or 5:
        finalcipher = ciphertext2[0:blockStart] + ciphertext1[blockStart:blockEnd] + ciphertext2[blockEnd:]
        finalcipher = bytes.fromhex(ciphertext2)
        finalcipher = aesDecryptor.update(finalcipher)
        return finalcipher







if __name__ == "__main__":
    
    

    while True: 
        print("\nAES Encoder/Decoder ")
        print("---------------------- ")
        print("\t1. Print Plaintext, Ciphertext, and Recovered Message1 and then Message2.")
        print("\t2. Change Place")
        print("\t3. Change Sender")
        print("\t4. Change Reciever")
        print("\t5. Change Date")    
        print("\t6. Quit \n")
        choice = input(">> ")
        print()

        if choice == '1':
            message1 += b"E" * (-len(message1) % 16)
            ciphertext = aesEncryptor.update(message1)
            message = message1
            print("plaintext:",message)
            print("ciphertext message 1:",ciphertext.hex())
            recovered = aesDecryptor.update(ciphertext)
            print("recovered:",recovered)
            print("\n")
            message2 += b"E" * (-len(message2) % 16)
            ciphertext = aesEncryptor.update(message2)
            message = message2
            print("plaintext:",message)
            print("ciphertext message 2:",ciphertext.hex())
            recovered = aesDecryptor.update(ciphertext)
            print("recovered:",recovered)
            


        elif choice == '2': #change place
            print("message1 originally says ",message1)
            print("message2 originally says ",message2)
            message1 += b"E" * (-len(message1) % 16)
            ciphertext = aesEncryptor.update(message1)
            ciphertext_altered = change_block(message1, message2, 6)
            print("recovered:",ciphertext_altered)


        elif choice == '3': #changing sender
            print("message originally says ", message3)
            ciphertext_altered = change_block(message3, message4, 1)           
            print("recovered:",ciphertext_altered)



        elif choice == '4': #change recieve
            print("message originally says ", message3)
            ciphertext_altered = change_block(message3, message5, 2)           
            print("recovered:",ciphertext_altered)
            
            

        elif choice == '5':#change date
            print("message originally says ", message3)
            ciphertext_altered = change_block(message3, message6, 4)           
            print("recovered:",ciphertext_altered)



        elif choice == '6':
            print("Goodbye! \n")
            break

        else:
            print("unknown option {}.".format(choice))

