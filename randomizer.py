import asyncio
import config
from bscscan import BscScan
from datetime import datetime
import pytz
import random

address = '0x3FD025ac173954778251699dacB2Ca126932841F'
# 0x3FD025ac173954778251699dacB2Ca126932841F

users = 0
scans = []

async def get_transactions(address='0x3FD025ac173954778251699dacB2Ca126932841F', val=1):
    global scans
    global users
    async with BscScan(config.API_KEY) as client:
        info = await client.get_bep20_token_transfer_events_by_address(
            address=address,
            startblock=0,
            endblock=999999999,
            sort='asc'
        )
        users = 0
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
            users += 1


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_transactions())


    for i in scans:
        print(i)
    print('\nКол-во пользователей:', users)
    print(scans[random.randint(0, users)])
