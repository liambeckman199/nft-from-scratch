from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_breed, fund_advanced_collectible
import time

#after deploying the nft contract to rinkeby netowrk,
#we use this function bellow to actually create our first collectible,
# which is a true random number using chainlink random number feed 

def main():
    dev=accounts.add(config['wallets']['from_key'])
    advanced_collectible=AdvancedCollectible[len(AdvancedCollectible)-1]
    fund_advanced_collectible(advanced_collectible.address)
    transaction= advanced_collectible.createCollectible(
       "None",{"from":dev})
    print("Waiting on second transaction...")   
    transaction.wait(1)
    time.sleep(55)
    requestId= transaction.events['requestedCollectible']['requestId']
    token_id= advanced_collectible.requestIdToTokenId(requestId)
    breed= get_breed(advanced_collectible.tokenIdToBreed(token_id))
    print("Dog bread of token {} is {}".format(token_id,breed)) #change to species for ours

