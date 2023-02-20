import random
import math
from decimal import Decimal
import time
from tkinter import *
from tkinter import ttk
import tkinter as tk
from functools import partial
import web3
import hashlib
import string
from random import choice
import smtplib


# Helper function
#-------------------------large prime---------------------------------------------
# first few primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]

# finding a prime candidate for a given bit size but larger one


def nBitRandom(n):
    return random.randrange(2**(n-1)+1, 2**n - 1)

# finding a coprime to all the gievn primes (n bit)


def getLowLevelPrime(n):
    while True:
        # large random number
        pcandidate = nBitRandom(n)

        # Test divisibility with the gievn prime list
        for divisor in first_primes_list:
            if pcandidate % divisor == 0 and divisor**2 <= pcandidate:
                break
        else:
            return pcandidate

#rabin miller primarlity test


def isMillerRabinPassed(mrcandidate):
    maxDivisionsByTwo = 0
    ecandidate = mrcandidate-1
    while ecandidate % 2 == 0:
        ecandidate >>= 1
        maxDivisionsByTwo += 1
    assert (2**maxDivisionsByTwo * ecandidate == mrcandidate-1)

    def trialComposite(round_tester):
        if pow(round_tester, ecandidate, mrcandidate) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ecandidate, mrcandidate) == mrcandidate-1:
                return False
        return True

    # number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrcandidate)
        if trialComposite(round_tester):
            return False
    return True


def largePrime():
    while True:
        n = 32
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate
            break


def find_generator(prime, prime_factors):
    for i in range(1000):
        generator = random.randrange(1, prime-1)
        for p_factor in prime_factors:  # check for each prime factor of Euler Totient of prime
            # divide Euler Totient of p by prime factor
            j = int((prime-1)/p_factor)
            e = pow(generator, j, prime)  # (generator**j)%prime
            if e == 1:  # if e=1 not a generator
                break
        else:
            return generator


def prime_factors(n):
    prime_factors_set = set()

    # Print the number of two's that divide n
    while n % 2 == 0:
        prime_factors_set.add(2)
        n = n / 2

    # n must be odd at this point
    for i in range(3, int(math.sqrt(n))+1, 2):

        # while i divides n , print i and divide n
        while n % i == 0:
            prime_factors_set.add(i)
            n = n / i

    # if n is a prime number greater than 2
    if n > 2:
        prime_factors_set.add(int(n))

    return prime_factors_set
#-------------------------end large prime-----------------------------------------


def isprime(n):
    if n == 2:
       return True
    if n == 1 or n % 2 == 0:
        return False
    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            return False
        i = i + 2
    return True


def initial(Z_lower=100):
    #generate q bigger than z_lower
    q = largePrime()

    print("q = " + str(q))
    print("\nq is prime\n")

    # Find p and r
    r = 1
    while True:
        p = r*q + 1
        if isprime(p):
            print("r = " + str(r))
            print("p = " + str(p))
            print("\np is prime\n")
            break
        r = r + 1

    g = find_generator(p, prime_factors(p-1))

    print("\ng = " + str(g) + "\n")

    return p, q, r, g


def generate_shares(n, t, secret, p, q, r, g):
    FIELD_SIZE = q
    coefficients = coeff(t, secret, FIELD_SIZE)

    shares = []
    for i in range(1, n+1):
        f_i = f(i, coefficients, q)
        shares.append((i, f_i))

    commitments = commitment(coefficients, g, p)
    verifications = []
    for i in range(1, n+1):
        #check1 = g ** shares[i-1][1] % p
        check1 = pow(g, shares[i-1][1], p)
        check2 = verification(g, commitments, i, p)
        verifications.append(check2)
        print("i-th share:", check1)
        print("i-th verification:", check2)

    return shares, commitments, verifications


def coeff(t, secret, FIELD_SIZE):
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t-1)]
    coeff.append(secret)  # a0 is secret
    return coeff


def f(x, coefficients, q):
    y = 0
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        y += (x ** coefficient_index * coefficient_value)
    return y


def commitment(coefficients, g, p):
    commitments = []
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        #c = g ** coefficient_value % p
        c = pow(g, coefficient_value, p)
        commitments.append(c)
    return commitments


def verification(g, commitments, i, p):
    v = 1
    for k, c in enumerate(commitments):
        #v = v * (c) ** (i ** k) % p
        v = v * pow(c, i ** k, p) % p
    return v


def quick_pow(a, b, q):
    temp = 1
    for i in range(1, b+1):
        temp = temp * a % q
    return temp % q


def reconstruct_secret(pool, q):
    sums = 0

    for j, share_j in enumerate(pool):
        xj, yj = share_j
        prod = Decimal(1)

        for i, share_i in enumerate(pool):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi)/(xi-xj))

        prod *= yj
        sums += Decimal(prod)
    return int(Decimal(sums))
    # return int(round(Decimal(sums)))


#-----OTP------
def random_OTP():
    chars = string.digits
    random_str = ''.join(choice(chars) for _ in range(4))
    return random_str


def convert_Hash(str_val):
    message = str_val.encode()
    return ("SHA-256:", hashlib.sha256(message).hexdigest())


#--------------------------smart contract----------------------------------------
w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:8545'))
abi = "[ { \"inputs\": [ { \"internalType\": \"uint256[]\", \"name\": \"share_value\", \"type\": \"uint256[]\" } ], \"name\": \"add_share\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [], \"name\": \"give_share\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"address\", \"name\": \"to\", \"type\": \"address\" } ], \"name\": \"set_share\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [ { \"internalType\": \"string\", \"name\": \"value_str\", \"type\": \"string\" } ], \"name\": \"store_hash\", \"outputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"function\" }, { \"inputs\": [], \"stateMutability\": \"nonpayable\", \"type\": \"constructor\" }, { \"inputs\": [], \"name\": \"get\", \"outputs\": [ { \"internalType\": \"uint256[]\", \"name\": \"\", \"type\": \"uint256[]\" } ], \"stateMutability\": \"view\", \"type\": \"function\" }, { \"inputs\": [], \"name\": \"return_hash\", \"outputs\": [ { \"internalType\": \"string\", \"name\": \"\", \"type\": \"string\" } ], \"stateMutability\": \"view\", \"type\": \"function\" } ]"
contract_addr = '0x2e169D7e39789D1a0d47EeD58A140D78A1D9B39d'
owner_addr = '0x3Efdd722056D61C7A77619e2D556927a5467D30D'
p_key = 'a0809ede87de80864e3aaad330d8ae0129a454c9c16000003e1ddc80df960cf3'
c = w3.eth.contract(address=contract_addr, abi=abi)

#sending the shares to the smart contract


def send_shares_smartContact(shares):
    nonce = w3.eth.getTransactionCount(owner_addr)
    store_contact = c.functions.add_share(shares).buildTransaction(
        {"from": owner_addr, "gasPrice": w3.eth.gas_price, "nonce": nonce})
    # Sign the transaction
    sign_store_contact = w3.eth.account.sign_transaction(
        store_contact, private_key=p_key)
    # Send the transaction
    send_store_contact = w3.eth.send_raw_transaction(
        sign_store_contact.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(
        send_store_contact)
    print("shares send to the smart contract")

#set the hash value in the smart contract


def set_hash(hash_str):
    nonce = w3.eth.getTransactionCount(owner_addr)
    store_contact = c.functions.store_hash(hash_str).buildTransaction(
        {"from": owner_addr, "gasPrice": w3.eth.gas_price, "nonce": nonce})
    # Sign the transaction
    sign_store_contact = w3.eth.account.sign_transaction(
        store_contact, private_key=p_key)
    # Send the transaction
    send_store_contact = w3.eth.send_raw_transaction(
        sign_store_contact.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(
        send_store_contact)
    print("Hash send to the smart contract")

#request shares from the smart contract


def get_shares():
    rtn = c.caller().get()
    share_list = rtn
    collected_shares = []
    #generate a list of tuples
    for i in range(0, len(share_list)-1, 2):
        temp_tuple = tuple((share_list[i], share_list[i+1]))
        collected_shares.append(temp_tuple)
    print("shares retrieved")
    print("collected_shares:", collected_shares)
    return collected_shares

#check whether the string provided is equal to the hash in the smart contract


def check_hash(str):
    rtn_hash = c.caller().return_hash()
    hash_str = convert_Hash(str)
    if rtn_hash == hash_str[1]:
        return True
    else:
        False

#secret reconstructed using gathered shares


def final_reconstruction(str_OTP):
    OTP = str_OTP.get()
    print(OTP)
    if OTP:
        if check_hash(OTP):
            collected_shares = get_shares()
            # Phase II: Secret Reconstruction
            pool = random.sample(collected_shares, t)
            i = 0
            for p in pool:
                labelResult = tk.Label(root)
                labelResult.config(text="%s" % str(p))
                labelResult.grid(row=11+i, column=4)
                i += 1
            secret_reconstructed = reconstruct_secret(pool, q)
            print(secret_reconstructed)
            labelResult = tk.Label(root)
            labelResult.config(text="Recovered value: %s" %
                               str(secret_reconstructed))
            labelResult.grid(row=15, column=4)
        else:
            open_popup("wrong OTP !")
    else:
        open_popup("Enter OTP !")

#making shares and sending them to the smart contract


def generate_and_send_shares(n, t, secret, p, q, r, g, label, str_email):
    secret = secret.get()
    email = str_email.get()
    shares, commitments, verifications = generate_shares(
        n, t, secret, p, q, r, g)

    #add these in smart contract
    if email:
        i = 0
        for share in shares:
            #print(share)
            label[i].config(text="%s" % str(share))
            i += 1
        print(
            f'Commitments: {", ".join(str(commitment) for commitment in commitments)}')
        print(
            f'verifications: {", ".join(str(verification) for verification in verifications)}')
        #shares as a list
        store_shares = []
        for i, share_i in enumerate(shares):
            x = share_i[0]
            y = share_i[1]
            store_shares.append(x)
            store_shares.append(y)
        send_shares_smartContact(store_shares)
        otp = random_OTP()
        otp_hash = convert_Hash(otp)
        set_hash(str(otp_hash[1]))
        #open_popup(otp)
        sendEmail(email, str(otp))
    else:
        open_popup("Enter an email !")

#-----------------email------------------------------------------


def sendEmail(receiverEmail, message):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("fypemail98@gmail.com", "wkfxtfkxgdlhjiaq")
    # sending the mail
    s.sendmail("fypemail98@gmail.com", receiverEmail, message)
    # terminating the session
    s.quit()


#-----------------end of email-----------------------------------
# Driver code
time_start = time.time()

p, q, r, g = initial(10**2)
t, n = 2, 9
root = tk.Tk()
root.geometry('500x300+300+200')

root.title('Secret Sharing')
secret = tk.IntVar()
labelSecret = tk.Label(root, text="Secret:").grid(row=1, column=0)
entrySecret = tk.Entry(root, textvariable=secret).grid(row=1, column=2)
OTP = tk.StringVar()
labelOTP = tk.Label(root, text="OTP:").grid(row=1, column=3)
entryOTP = tk.Entry(root, textvariable=OTP).grid(row=1, column=4)
emailAddr = tk.StringVar()
labelOTP = tk.Label(root, text="Email Address:").grid(row=2, column=0)
entryOTP = tk.Entry(root, textvariable=emailAddr).grid(row=2, column=2)

labelResult = tk.Label(root)
labelResult.grid(row=n, column=2)


label_list = []
for i in range(n):
    labelResult = tk.Label(root)
    labelResult.config(text="<empty>")
    labelResult.grid(row=n+i, column=2)
    label_list.append(labelResult)

#-----popup-----


def open_popup(text_val):
   top = Toplevel(root)
   top.geometry("150x50")
   top.title("Child Window")
   Label(top, text=text_val).grid(row=0, column=0)


call_result = partial(generate_and_send_shares, n, t,
                      secret, p, q, r, g, label_list, emailAddr)
buttonCal = tk.Button(root, text="Generate & send Shares",
                      command=call_result).grid(row=3, column=0)

Rec_result = partial(final_reconstruction, OTP)
buttonRec = tk.Button(root, bg='yellow', text="Reconstruct Shares",
                      command=Rec_result).grid(row=3, column=4)


root.mainloop()
time_end = time.time()
print('time cost in second:', time_end-time_start)
