from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed
from pathlib import Path
import os
import requests
import json

#IPFS IMAGES ALREADY UPLOADED...MY IPFS WASNT RUNNING
breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    print("Wokring on" + network.show_active())
    advanced_collectible=AdvancedCollectible[len(AdvancedCollectible)-1]
    number_of_tokens= advanced_collectible.tokenCounter()
    print("The number of tokens youve deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata= sample_metadata.metadata_template
        breed= get_breed(nft_contract.tokenIdToBreed(token_id))
        metadata_file_name=(
            "./metadata/{}/".format(network.show_active())+str(token_id)
            + "-"+breed+ ".json"
        )
        # an example of what this file would be called is:
        # metadata/rinkeby/0-shiba_inu.json
        if Path(metadata_file_name).exists():
            print("{} already found!".format(metadata_file_name))
        else:
            print("Creating Metadata File {}".format(metadata_file_name))
            collectible_metadata["name"]= get_breed(
                nft_contract.tokenIdToBreed(token_id)
            )
            collectible_metadata["desciption"]="An adorable {} pup!".format(
                collectible_metadata["name"]
            )
            print(collectible_metadata)

            #THIS IS WHERE THE IPFS WASNT WORKING...
            #NEED TO FIX THE PORT I THINK TO RUN IPFS DAEMON CORRECTLY

            #temporary used existing ipfs images... changed
            #image_to_upload = upload_to_ipfs(image_path) to as shown in script

            image_to_upload = None
            if os.getenv("UPLOAD_IPFS")=="true":
                image_path = "./img/{}.png".format(
                    breed.lower().replace('_', '-'))
                image_to_upload=upload_to_ipfs(image_path)    
            image_to_upload = (
                breed_to_image_uri[breed] if not image_to_upload else image_to_upload
            )
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)
                

def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(image_uri)
        return image_uri
    return None
                
                

