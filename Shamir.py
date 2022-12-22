import random
from math import ceil
from decimal import Decimal
import tkinter as tk
from functools import partial

from numpy import empty

#limit for generating coefficients
FIELD_SIZE = 10**5

#getting the value of polynomial


def polynom(x, coefficients):

	point = 0

	for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
		point += x ** coefficient_index * coefficient_value
	return point

#generating coefficinets for the polynomial


def coeff(t, secret):

	coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
	coeff.append(secret)
	return coeff

#generating shares for a given random x value to the polynomial


def generate_shares(n, m, secret):

	coefficients = coeff(m, secret)
	shares = []

	for i in range(1, n+1):
		x = random.randrange(1, FIELD_SIZE)
		shares.append((x, polynom(x, coefficients)))

	return shares

#reconstucting the polynomial and get the secret


def reconstruct_secret(shares):

	sums = 0

	for j, share_j in enumerate(shares):
		xj, yj = share_j
		prod = Decimal(1)

		for i, share_i in enumerate(shares):
			xi, _ = share_i
			if i != j:
				prod *= Decimal(Decimal(xi)/(xi-xj))

		prod *= yj
		sums += Decimal(prod)

	return int(round(Decimal(sums), 0))

#phase I generating shares


def callGenerateShares(n, m, secret, label, share_list):
    secret = secret.get()
    shares = generate_shares(n, m, secret)
    i = 0
    if share_list:
        share_list.clear()
    for share in shares:
        #print(share)
        label[i].config(text="%s" % str(share))
        i += 1
        share_list.append(share)


#phase II recovring shares
def callRecover(shares, t):
    #getting random shares form shares
    pool = random.sample(shares, t)
    i = 0
    for p in pool:
        labelResult = tk.Label(root)
        labelResult.config(text="%s" % str(p))
        labelResult.grid(row=7+i, column=4)
        i += 1
    #get the secret recovered
    recovered = reconstruct_secret(pool)
    #UI
    labelResult = tk.Label(root)
    labelResult.config(text="Recovered value: %s" % str(recovered))
    labelResult.grid(row=10, column=4)


#driver code with UI
root = tk.Tk()
root.geometry('400x200+100+200')

root.title('Secret Sharing')
secret = tk.IntVar()
labelSecret = tk.Label(root, text="Secret:").grid(row=1, column=0)
entrySecret = tk.Entry(root, textvariable=secret).grid(row=1, column=2)

labelResult = tk.Label(root)
labelResult.grid(row=7, column=2)


#hard coded t and n values
t, n = 3, 5
#making UI objects
label_list = []
share_list = []
for i in range(n):
    labelResult = tk.Label(root)
    labelResult.config(text="<empty>")
    labelResult.grid(row=7+i, column=0)
    label_list.append(labelResult)

#phase I
call_result = partial(callGenerateShares, n, t,
                      secret, label_list, share_list)
buttonCal = tk.Button(root, bg='green', text="Generate Shares",
                      command=call_result).grid(row=3, column=0)

#phase II
Rec_result = partial(callRecover, share_list, t)
buttonRec = tk.Button(root, bg='yellow', text="Recover Shares",
                      command=Rec_result).grid(row=3, column=4)

root.mainloop()
