import aiohttp
import logging
import aiogram.utils.markdown as fmt

# This fuction formats json responce into text message
async def format_info(info_json) -> str:
    return fmt.text(fmt.text("Name:", fmt.hbold(info_json['name']), '📊'),
                    fmt.text("Floor price:", info_json.get('floorPrice', 0)/10**9, "◎"),
                    fmt.text("Listings:", info_json.get('listedCount', 0)),
                    fmt.text("Avg. sale (24h):", round(info_json.get('avgPrice24hr', 0)/10**9, 3), "◎"),
                    fmt.text("Total volume:", info_json.get('volumeAll', 0)//10**9, "◎"),
                    sep='\n')

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