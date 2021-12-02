import cbpro
from cbpro_client import cbpro_client
from logger import logger

@cbpro_client
def get_deposit_account(cbpro_client):

    bank_accounts = cbpro_client.get_payment_methods()

    for account in bank_accounts:
        if account['type'] == 'ach_bank_account':
            return account

@cbpro_client
@logger
def deposit_funds(cbpro_client, deposit_amount = 10): 
    logger.info("Getting account ID")
    deposit_account_id = get_deposit_account()['id']
    logger.info("Account ID: {}".format(deposit_account_id))

    resp = cbpro_client.deposit(deposit_amount, 'USD', deposit_account_id)
    if 'message' in resp.keys():
        logger.warning("In sandbox mode, unable to make deposit")
    else:
        logger.info("Deposit Response: {}".format(resp))
        
    return resp