bl_info = {
    "name" : "Telescope-Blender Metaverse",
    "author" : "Yevgeniy Stolyarenko",
    "version" : (1,0),
    "blender" : (3,4,0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "Add Mesh",
}


import bpy
import os
import sys
import requests
import json 


# web3 dependency support
#lib_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib1")
#sys.path += [lib_dir]
from web3 import Web3

# Contract ABI definition
contract_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "approved",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "operator",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "ApprovalForAll",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newMember",
                "type": "address"
            }
        ],
        "name": "addNewMember",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "contractOwner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllTokenIds",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "getApproved",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "getTokenURI",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "operator",
                "type": "address"
            }
        ],
        "name": "isApprovedForAll",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "tokenURI",
                "type": "string"
            }
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "ownerOf",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "postingCost",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "recepient",
        "outputs": [
            {
                "internalType": "address payable",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "oldMember",
                "type": "address"
            }
        ],
        "name": "removeMember",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "operator",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "interfaceId",
                "type": "bytes4"
            }
        ],
        "name": "supportsInterface",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "telescopeAdmin",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "telescopeFee",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "tokenByIndex",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "tokenOfOwnerByIndex",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "tokenURI",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

class DesignerPanel(bpy.types.Panel):
    bl_label = "Meta World Designer"
    bl_idname = "OBJECT_PT1_my_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Telescope"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.label(text="Enter Meta World Credentials:")
        col.prop(context.scene, "Infura", icon="MESH_ICOSPHERE")
        col.prop(context.scene, "Pinata_key", icon="KEY_HLT")
        col.prop(context.scene, "Pinata_secret_key", icon="KEY_HLT") 
        col.prop(context.scene, "World_address", icon="WORLD")   
            
        col.label(text="Enter Your Credentials:")
        col.prop(context.scene, "My_address", icon="COLORSET_05_VEC")
        col.prop(context.scene, "My_key", icon="COLORSET_04_VEC")        
        
        col.operator("myaddon.process_load_world")
        col.operator("myaddon.process_designer_text")
        
class CreatorPanel(bpy.types.Panel):
    bl_label = "Meta World Creator"
    bl_idname = "OBJECT_PT2_my_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Telescope"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        
        col.label(text="Enter Meta World Credentials:")
        col.prop(context.scene, "Infura", icon="MESH_ICOSPHERE")
        col.prop(context.scene, "World_address", icon="WORLD")
        
        col.label(text="Enter your credentials:")
        col.prop(context.scene, "My_address", icon="COLORSET_05_VEC")
        col.prop(context.scene, "My_key", icon="COLORSET_04_VEC")
        
        col.prop(context.scene, "Add_designer", icon="ADD")
        col.prop(context.scene, "Delete_designer", icon="GHOST_DISABLED")
        
        col.operator("myaddon.process_add_user")
        col.operator("myaddon.process_del_user")
 
class ProcessWorldLoaderOperator(bpy.types.Operator):
    bl_idname = "myaddon.process_load_world"
    bl_label = "Load Meta World"
    
    def execute(self, context):
        
        # Connect to Mainnet/Testnet
        infura = str(context.scene.Infura)
        w3 = Web3(Web3.HTTPProvider(infura))
        
        # Pinata Credentials
        pinata_api_key = str(context.scene.Pinata_key)
        pinata_secret_key = str(context.scene.Pinata_secret_key)
        headers = {
                'pinata_api_key': pinata_api_key,
                'pinata_secret_api_key': pinata_secret_key
            }
        
        # Getting contract address
        contract_address = str(context.scene.World_address)
        
        # Retrieving all minted object ids
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        total_tokens = contract.functions.totalSupply().call()
        for i in range(total_tokens):
            token_id = contract.functions.tokenByIndex(i).call()
            token_owner = contract.functions.ownerOf(token_id).call()
            if token_owner != '0x000000000000000000000000000000000000dEaD':
                token_uri = contract.functions.getTokenURI(token_id).call()  
                # Send a GET request to the Pinata API to retrieve the file
                response = requests.get(token_uri, headers=headers)
                # Check if the request was successful
                if response.status_code == 200:
                    # Extract the file content from the response
                    file_content = response.content
                    # Create a json file and save pinata json data in the file
                    filepath = bpy.data.filepath
                    path_without_file = os.path.dirname(os.path.dirname(filepath))
                    full_filepath = path_without_file.replace("/", "\\")
                    saved_path = full_filepath + "\\" + str(token_id) + ".json"
                    with open(saved_path, "wb") as f:
                        f.write(file_content)
                    # Get .obj URL from the file
                    with open(saved_path, 'r') as f:
                        data = json.load(f)
                        obj_uri = data['model']['url']
                    # Get .obj file from pinata
                    response = requests.get(obj_uri, headers=headers)
                    file_content = response.content

                    # Create a new .obj file and save the loaded object in the file
                    filepath = bpy.data.filepath
                    path_without_file = os.path.dirname(filepath)
                    full_filepath = path_without_file.replace("/", "\\")
                    saved_path = full_filepath + "\\" + str(token_id) + ".obj"
                    with open(saved_path, "wb") as f:
                        f.write(file_content)
                    
                    # Loading object into the current .blend file    
                    bpy.ops.import_scene.obj(filepath=saved_path)
        return {"FINISHED"}
                           
        
class ProcessMintOperator(bpy.types.Operator):
    bl_idname = "myaddon.process_designer_text"
    bl_label = "Mint 3D Object"
    
    def execute(self, context):
        
        # Connect to Mainnet/Testnet
        infura = str(context.scene.Infura)
        w3 = Web3(Web3.HTTPProvider(infura))
        
        # Pinata Credentials
        pinata_api_key = str(context.scene.Pinata_key)
        pinata_secret_key = str(context.scene.Pinata_secret_key)
        headers = {
                'pinata_api_key': pinata_api_key,
                'pinata_secret_api_key': pinata_secret_key
            }
        endpoint = "https://gateway.pinata.cloud/ipfs/"
        
        designer_address = context.scene.My_address
        designer_key = context.scene.My_key
        contract_address = context.scene.World_address
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Select active object
        keep_object = bpy.context.object
        # Rename to add id to the name
        new_object_name = str(contract.functions.totalSupply().call())
        keep_object.name = new_object_name

        # Iterate over all objects in the scene and remove them except for keep_object
        for obj in bpy.context.scene.objects:
            if obj != keep_object:
                bpy.data.objects.remove(obj, do_unlink=True)
        
        # Save obj file
        # Set the path to the output .obj file
        output_path = os.path.dirname(os.path.dirname(__file__)) + "\\" + "addons\\" + new_object_name + ".obj"

        # Get the selected object in the scene
        selected_objects = bpy.context.selected_objects

        # Export the selected objects as .obj
        bpy.ops.export_scene.obj(filepath=output_path, use_selection=True, 
                                  use_materials=False, 
                                  use_normals=True)
        
        # Upload the .obj file to Pinata
        with open(output_path, 'rb') as obj_file:
            url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
            data = {
                'file': obj_file
            }
            response = requests.post(url, headers=headers, files=data)
        
        response_json = json.loads(response.text)
        pinata_hash = response_json['IpfsHash']
        file_location = endpoint + pinata_hash
        
        # Update template with .obj file location
        json_template = os.path.dirname(os.path.dirname(__file__)) + "\\addons" + "\\template.json"        
        with open(json_template, 'r') as f:
            data = json.load(f)
            #data['image'] = file_location
            nft_name = "Telescope " + new_object_name 
            data['name'] = nft_name
            data['model']['url'] = file_location
        with open(json_template, 'w') as f:
            json.dump(data, f)
        
        # Upload json to IPFS
        with open(json_template, 'rb') as f:
            url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
            data = {
                'file': f
                }
            response = requests.post(url, headers=headers, files=data)
        response_json = json.loads(response.text)
        pinata_hash = response_json['IpfsHash']
        file_location = endpoint + pinata_hash
        
        # Getting total posting fee
        postingCost = contract.functions.postingCost().call()
        telescopeFee = contract.functions.telescopeFee().call()
        totalCost = postingCost + telescopeFee

        
        # Minting new object
        transaction = contract.functions.mint(designer_address, file_location).build_transaction({
        'nonce': w3.eth.get_transaction_count(designer_address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'value': totalCost})

        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=designer_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)                
        
        self.report({'INFO'}, "3D Object has been minted successfully!")
        
        return {"FINISHED"}
    

class ProcessAdminAddUserOperator(bpy.types.Operator):
    bl_idname = "myaddon.process_add_user"
    bl_label = "Add Designer"
    
    def execute(self, context):
        # Connect to Mainnet/Testnet
        infura = str(context.scene.Infura)
        w3 = Web3(Web3.HTTPProvider(infura))
        
        creator_address = str(context.scene.My_address)
        creator_key = str(context.scene.My_key)
        add_designer = str(context.scene.Add_designer)
        
        contract_address = str(context.scene.World_address)
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        transaction = contract.functions.addNewMember(add_designer).build_transaction({
        'nonce': w3.eth.get_transaction_count(creator_address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price})

        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=creator_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)         
       
        self.report({'INFO'}, "Designer has been successfully added to the World!")
        
        return {"FINISHED"}   

class ProcessAdminDelUserOperator(bpy.types.Operator):
    bl_idname = "myaddon.process_del_user"
    bl_label = "Remove Designer"
    
    def execute(self, context):
        # Connect to Mainnet/Testnet
        infura = str(context.scene.Infura)
        w3 = Web3(Web3.HTTPProvider(infura))
        
        creator_address = str(context.scene.My_address)
        creator_key = str(context.scene.My_key)
        del_designer = str(context.scene.Delete_designer)
        
        contract_address = str(context.scene.World_address)
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        transaction = contract.functions.removeMember(del_designer).build_transaction({
        'nonce': w3.eth.get_transaction_count(creator_address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price})

        # Sign and send the transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=creator_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)         
       
        self.report({'INFO'}, "Designer has been successfully removed!")
        
        
        return {"FINISHED"} 

def register():
    bpy.types.Scene.Infura = bpy.props.StringProperty()
    bpy.types.Scene.Pinata_key = bpy.props.StringProperty()
    bpy.types.Scene.Pinata_secret_key = bpy.props.StringProperty()
    bpy.types.Scene.My_address = bpy.props.StringProperty()
    bpy.types.Scene.My_key = bpy.props.StringProperty()
    bpy.types.Scene.World_address = bpy.props.StringProperty()
    bpy.types.Scene.Add_designer = bpy.props.StringProperty()
    bpy.types.Scene.Delete_designer = bpy.props.StringProperty()
    bpy.utils.register_class(DesignerPanel)
    bpy.utils.register_class(CreatorPanel)
    bpy.utils.register_class(ProcessMintOperator)
    bpy.utils.register_class(ProcessWorldLoaderOperator)
    bpy.utils.register_class(ProcessAdminAddUserOperator)
    bpy.utils.register_class(ProcessAdminDelUserOperator)

def unregister():
    del bpy.types.Scene.Infura
    del bpy.types.Scene.Pinata_key
    del bpy.types.Scene.Pinata_secret_key
    del bpy.types.Scene.My_address
    del bpy.types.Scene.My_key
    del bpy.types.Scene.World_address
    del bpy.types.Scene.Add_designer
    del bpy.types.Scene.Delete_designer
    bpy.utils.unregister_class(DesignerPanel)
    bpy.utils.unregister_class(CreatorPanel)
    bpy.utils.unregister_class(ProcessMintOperator)
    bpy.utils.unregister_class(ProcessWorldLoaderOperator)
    bpy.utils.unregister_class(ProcessAdminAddUserOperator)
    bpy.utils.unregister_class(ProcessAdminDelUserOperator)
    
    
if __name__ == "__main__":
    register()
