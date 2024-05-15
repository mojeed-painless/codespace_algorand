from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
#print(dispenser.address) 

creator = algorand.account.random()
#print(creator.address)

algorand.send.payment (
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

#print(algorand.account.get_information(creator.address))

send_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=750,
        asset_name="PAINLESS",
        unit_name="MJD"
    )
)

asset_id = send_txn["confirmation"]["asset-index"]
#print(asset_id)

receiver_accounts = []

for i in range(3):  # Change 3 to the number of receiver accounts you want
    receiver = algorand.account.random()
    receiver_accounts.append(receiver)

for receiver_acct in receiver_accounts:
    algorand.send.payment (
        PayParams(
            sender=dispenser.address,
            receiver=receiver_acct.address,
            amount=10_000_000
        )
    )

    algorand.send.asset_opt_in(
        AssetOptInParams(
            sender=receiver_acct.address,
            asset_id=asset_id
        )
    )

    asset_transfer = algorand.send.asset_transfer(
        AssetTransferParams(
            sender=creator.address,
            receiver=receiver_acct.address,
            asset_id=asset_id,
            amount=50 * (receiver_accounts.index(receiver_acct) + 1),  # Change amount as needed
            last_valid_round=700
        )
    )

    print(algorand.account.get_information(receiver_acct.address))

