import web3

class EthClient:
    w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:8545'))
    

    def __init__(self,abi,contractAddr,ownerAddr,privateKey) -> None:
        self.abi=abi
        self.contractAddr=contractAddr
        self.ownerAddr=ownerAddr
        self.privateKey=privateKey
        self.contact = self.__class__.w3.eth.contract(address=contractAddr, abi=abi)

    def set(self,value,functionName):
        nonce = self.__class__.w3.eth.getTransactionCount(self.ownerAddr)
        store_contact = self.contact.functions.store_hash(value).buildTransaction(
            {"from": self.ownerAddr, "gasPrice":  self.__class__.w3.eth.gas_price, "nonce": nonce})
        # Sign the transaction
        sign_store_contact = self.__class__.w3.eth.account.sign_transaction(
            store_contact, private_key=self.privateKey)
        # Send the transaction
        send_store_contact = self.__class__.w3.eth.send_raw_transaction(
            sign_store_contact.rawTransaction)
        transaction_receipt = self.__class__.w3.eth.wait_for_transaction_receipt(
            send_store_contact)
        print("smart contract transaction done")

    def get_shares():
        rtn = self.contact .caller().get()
        share_list = rtn
        collected_shares = []
        #generate a list of tuples
        for i in range(0, len(share_list)-1, 2):
            temp_tuple = tuple((share_list[i], share_list[i+1]))
            collected_shares.append(temp_tuple)
        print("shares retrieved")
        print("collected_shares:", collected_shares)
        return collected_shares
