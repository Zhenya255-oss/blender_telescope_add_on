import bpy
import sys
import requests
import json
import pickle 
import os

import subprocess
import sys

# web3 dependency support
lib_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib")
sys.path += [lib_dir]

#sys.path += [r"C:\Users\stoly\AppData\Local\Programs\Python\Python310\Lib\site-packages"]

from web3 import Web3
import pinata
# Connect to a local Ganache blockchain
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# Define the contract ABI and address
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
headers = {
                'pinata_api_key': 'e3c4a8f9959c5bc970e3',
                'pinata_secret_api_key': '06dbaccac51438159d5f9be50be03ea67eb9b0cb8dec0cec978cc4e6482cefa0'
            }

class DesignerPanel(bpy.types.Panel):
    bl_label = "Designer"
    bl_idname = "OBJECT_PT1_my_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Telescope"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()

        col.label(text="Enter your credentials:")
        col.prop(context.scene, "my_addr", icon="COLORSET_05_VEC")
        col.prop(context.scene, "my_key", icon="COLORSET_04_VEC")
        
        col.label(text="Enter smart contract")
        col.prop(context.scene, "addr", icon="WORLD_DATA")
        
        col.operator("myaddon.process_load_world")
        col.operator("myaddon.process_designer_text")
 
class ProcessWorldLoaderOperator(bpy.types.Operator):
    bl_idname = "myaddon.process_load_world"
    bl_label = "Load Meta World"
    
    def execute(self, context):
        contract_address = context.scene.addr
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        all_token_ids = contract.functions.getAllTokenIds().call()
        for token_id in all_token_ids:
            token_uri = contract.functions.getTokenURI(token_id).call()
            # Send a GET request to the Pinata API to retrieve the file
            response = requests.get(token_uri, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the file content from the response
                file_content = response.content

                # Save the file to a local file
                filepath = bpy.data.filepath
                path_without_file = os.path.dirname(filepath)
                full_filepath = path_without_file.replace("/", "\\")
                saved_path = full_filepath + "\\" + str(token_id) + ".json"
                with open(saved_path, "wb") as f:
                    f.write(file_content)
                with open(saved_path, 'r') as f:
                    data = json.load(f)
                    obj_uri =  data['image']
                response = requests.get(obj_uri, headers=headers)
                    
                file_content = response.content

                # loading the obj file
                filepath = bpy.data.filepath
                path_without_file = os.path.dirname(filepath)
                full_filepath = path_without_file.replace("/", "\\")
                saved_path = full_filepath + "\\" + str(token_id) + ".obj"
                with open(saved_path, "wb") as f:
                    f.write(file_content)
                    
                bpy.ops.import_scene.obj(filepath=saved_path)
                    # Append the object from the source file to the current blendfile
                    #with bpy.data.libraries.load(saved_path) as (data_from, data_to):
                    #    data_to.objects = data_from.objects

                    # Link the appended object to the current scene
                    #for obj in data_to.objects:
                    #    bpy.context.collection.objects.link(obj)       
        
class ProcessMintOperator(bpy.types.Operator):
    bl_idname = "myaddon.process_designer_text"
    bl_label = "Mint 3D Object"
    
    def execute(self, context):
        contract_address = context.scene.addr
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        endpoint = "https://gateway.pinata.cloud/ipfs/"
        
        # Select active object
        keep_object = bpy.context.object

        # Iterate through all objects in the scene and remove them if they are not the keep_object
        for obj in bpy.context.scene.objects:
            if obj != keep_object:
                bpy.data.objects.remove(obj, do_unlink=True)
        
        # Save Blend file
        filepath = bpy.data.filepath
        full_filepath = filepath.replace("/", "\\")
        
        # Save obj file
        # Set the path to the output .obj file
        output_path = os.path.dirname(os.path.dirname(__file__)) + "\\template.obj"

        # Get the selected objects in the scene
        selected_objects = bpy.context.selected_objects

        # Export the selected objects as .obj
        bpy.ops.export_scene.obj(filepath=output_path, use_selection=True, 
                                  use_materials=False, 
                                  use_normals=True)
        
        # Upload file to Pinata
        with open(output_path, 'rb') as f:
            url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
            headers = {
                'pinata_api_key': 'e3c4a8f9959c5bc970e3',
                'pinata_secret_api_key': '06dbaccac51438159d5f9be50be03ea67eb9b0cb8dec0cec978cc4e6482cefa0'
            }
            data = {
                'file': f
            }
            response = requests.post(url, headers=headers, files=data)
        
        response_json = json.loads(response.text)
        pinata_hash = response_json['IpfsHash']
        file_location = endpoint + pinata_hash
        
        #update template with location of a 3d model
        output_path = "C://Users//stoly//Desktop//Blender" + "//template.json"

        with open(output_path, 'r') as f:
            data = json.load(f)
            data['image'] = file_location

        with open(output_path, 'w') as f:
            json.dump(data, f)
        
        #upload json to ipfs
        with open(output_path, 'rb') as f:
            url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
            headers = {
                'pinata_api_key': 'e3c4a8f9959c5bc970e3',
                'pinata_secret_api_key': '06dbaccac51438159d5f9be50be03ea67eb9b0cb8dec0cec978cc4e6482cefa0'
            }
            data = {
                'file': f
            }
            response = requests.post(url, headers=headers, files=data)
        response_json = json.loads(response.text)
        pinata_hash = response_json['IpfsHash']
        file_location = endpoint + pinata_hash
        
        postingCost = contract.functions.postingCost().call()
        telescopeFee = contract.functions.postingCost().call()
        
        totalCost = postingCost + telescopeFee
        
        tx_hash = contract.functions.mint(str(context.scene.my_addr), file_location).transact({'from': str(context.scene.my_addr),"value": totalCost})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.report({'INFO'}, "3D Object has been minted successfully!")
        
        return {"FINISHED"}

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
        col.label(text="Enter your credentials:")
        col.prop(context.scene, "my_addr", icon="COLORSET_05_VEC")
        col.prop(context.scene, "my_key", icon="COLORSET_04_VEC")
        
        col.label(text="Enter smart contract")
        col.prop(context.scene, "addr", icon="WORLD_DATA")
        
        col.prop(context.scene, "add_user")
        col.prop(context.scene, "del_user")
        
        col.operator("myaddon.process_add_user")
        col.operator("myaddon.process_del_user")

class ProcessAdminAddUserOperator(bpy.types.Operator):
    bl_idname = "myaddon.process_add_user"
    bl_label = "Add Designer"
    
    def execute(self, context):
        my_addr = context.scene.my_addr
        contract_address = context.scene.addr
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        tx_hash = contract.functions.addNewMember(str(context.scene.add_user)).transact({"from": str(context.scene.my_addr)})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.report({'INFO'}, "Designer has been successfully added to the World!")
        
        return {"FINISHED"}   

class ProcessAdminDelUserOperator(bpy.types.Operator):
    bl_idname = "myaddon.process_del_user"
    bl_label = "Remove Designer"
    
    def execute(self, context):
        my_addr = context.scene.my_addr
        contract_address = context.scene.addr
        
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)

        tx_hash = contract.functions.removeMember(str(context.scene.del_user)).transact({"from": str(context.scene.my_addr)})
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        self.report({'INFO'}, "Designer has been successfully removed from the community!")
        
        return {"FINISHED"} 

def register():
    bpy.types.Scene.my_addr = bpy.props.StringProperty()
    bpy.types.Scene.my_key = bpy.props.StringProperty()
    bpy.types.Scene.addr = bpy.props.StringProperty()
    bpy.types.Scene.add_user = bpy.props.StringProperty()
    bpy.types.Scene.del_user = bpy.props.StringProperty()
    bpy.utils.register_class(DesignerPanel)
    bpy.utils.register_class(CreatorPanel)
    bpy.utils.register_class(ProcessMintOperator)
    bpy.utils.register_class(ProcessWorldLoaderOperator)
    bpy.utils.register_class(ProcessAdminAddUserOperator)
    bpy.utils.register_class(ProcessAdminDelUserOperator)

def unregister():
    del bpy.types.Scene.my_addr
    del bpy.types.Scene.my_key
    del bpy.types.Scene.addr
    del bpy.types.Scene.add_user
    del bpy.types.Scene.del_user
    bpy.utils.unregister_class(DesignerPanel)
    bpy.utils.unregister_class(CreatorPanel)
    bpy.utils.unregister_class(ProcessMintOperator)
    bpy.utils.unregister_class(ProcessWorldLoaderOperator)
    bpy.utils.unregister_class(ProcessAdminAddUserOperator)
    bpy.utils.unregister_class(ProcessAdminDelUserOperator)
    
    
if __name__ == "__main__":
    register()