import asyncio
import config
from bscscan import BscScan
from datetime import datetime


scans = []

async def get_transactions(address=config.address, val=1):
    global scans
    async with BscScan(config.API_KEY) as client:
        info = await client.get_bep20_token_transfer_events_by_address(
            address=address,
            startblock=0,
            endblock=999999999,
            sort='asc'
        )
        scans = []
        for x in info:
            from_adr = str(x['from'])
            value = str(int(x['value']) / 1000000000000000000)
            tokenSymbol = x['tokenSymbol']
            date = str(datetime.utcfromtimestamp(int(x['timeStamp'])))
            if float(value) >= float(val):
                # scans.append(f'{from_adr} {value} {tokenSymbol} {date}')
                scan = [from_adr, value, tokenSymbol, date]
                scans.append(scan)

async def get_fails(address=config.address, val=1):
    global scans
    async with BscScan(config.API_KEY) as client:
        info = await client.get_bep20_token_transfer_events_by_address(
            address=address,
            startblock=0,
            endblock=999999999,
            sort='asc'
        )
        scans = []
        for x in info:
            from_adr = str(x['from'])
            value = str(int(x['value']) / 1000000000000000000)
            tokenSymbol = x['tokenSymbol']
            date = str(datetime.utcfromtimestamp(int(x['timeStamp'])))
            if float(value) < float(val):
                # scans.append(f'{from_adr} {value} {tokenSymbol} {date}')
                scan = [from_adr, value, tokenSymbol, date]
                scans.append(scan)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_transactions())


    for i in scans:
        print(i)
    # print('\nКол-во пользователей:', users)
