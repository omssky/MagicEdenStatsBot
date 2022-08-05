# MagicEdenStatsBot

This repository contains the source code for a small telegram bot designed to make it easier to check the basic collection parameters on the Solana NFT marketplace MagicEden.
You can use it here: https://t.me/MagicEdenStatsBot (Not yet launched)

### Features
* `/fp *collecion_name*` - command to gather collection info by name or symbol;  
Bot works with MagicEden API, for the most correct work it is recommended to use the **symbol** of the collection instead of the name to search.;  
* `/fp_link *collecion_me_link*` - command to gather collection info by it's MagicEden's link;
* For ease of use of the bot with collections with a complex/long character is implemented functionality of favorite collections.
* `/favorites*` - command to check and manage your favorite collection; 
* `/reload` - command to reset user data, in case of unexpected errors in the database;  
* Just a little functionality for the administration: `/stats` - statistics, `/notify` - broadcaster 

### Requirements
* Python 3.9 and above;
* Tested on Windows 11, no platform-specific code is used, so it should work on any platform;

### Installation  
1. Go to [@BotFather](https://t.me/telegram), create a new bot, write down its token.  
2. Clone this repo and `cd` into it;  
3. Copy `env_dist` to `.env`. **Warning**: files starting with dot may be hidden in Linux, 
so don't worry if you stop seeing this file, it's still here! 
4. Replace default values with your own;  
5. Instal packages: `pip install --pre -r requirements.txt`
6. It's ready to use! Start point: `__main__.py`
