import aiohttp
import logging

# This fuction formats json responce into text message
async def format_info(info_json) -> str:
    info = (f"Name: <b>{info_json['name']}</b> 📊\n"
            f"Floor price: {info_json.get('floorPrice', 0)/10**9} ◎\n"
            f"Listings: {info_json.get('listedCount', 0)}\n"
            f"Avg. sale (24h): {round(info_json.get('avgPrice24hr', 0)/10**9, 3)} ◎\n"
            f"Total volume: {info_json.get('volumeAll', 0)//10**9} ◎\n")
    return info

# This fuction sends requests to MagicEdenAPI for collecion info
async def collecion_info(user_query):
    async with aiohttp.ClientSession() as session:
        for sep in ['_', '']:
            collection_symbol=user_query.replace(' ', sep)
            response = await session.get(f'https://api-mainnet.magiceden.dev/v2/collections/{collection_symbol}')
            response_json = await response.json()
            if response.status != 404:
                logging.info(f"Search [{user_query}:{collection_symbol}] SUCCSESS")
                return response_json
        else:
            logging.error(f"Search [{user_query}:{collection_symbol}] FAILED")
            return None
            