
import discord, asyncio, json, emoji

client = discord.Client()

def get_bindings():
    with open('bindings.json', 'r') as f:
        return json.load(f)

def emoji_equal(_emoji, compare, custom):
    if custom:
        return _emoji.name == compare
    elif emoji.demojize(_emoji) == compare:
        return True
    return False

@client.event
async def on_ready():
    print('Logged in as {}#{}.'.format(client.user.name, client.user.id))
    client.loop.create_task(on_update())

# async def add(reaction, user):
#     if user.id != client.user.id:
#         for bind in bindings:
#             if emoji_equal(reaction.emoji, bind, reaction.custom_emoji):
#                 await client.add_roles(user, discord.utils.get(user.server.roles, name=bindings[bind]))

# async def remove(reaction, user):
#     if user.id != client.user.id:
#         for bind in bindings:
#             if emoji_equal(reaction.emoji, bind, reaction.custom_emoji):
#                 await client.remove_roles(user, discord.utils.get(user.server.roles, name=bindings[bind]))

# @client.event
# async def on_message(message):
#     if message.content.startswith('!role'):
#         msg = await client.send_message(message.channel, "Please select your role.")
#         for binding in bindings:
#             await client.add_reaction(msg, discord.utils.get(client.get_all_emojis(), name=binding))

async def on_update():
    while True:
        # Reset bindings,
        bindings = get_bindings()

        # Iterate through each message bind,
        for message in bindings['locations']:
            all_users, channel, roles = [member for member in [server for server in client.servers if server.id == bindings['locations'][message]['server']][0].members], bindings['locations'][message]['channel'], bindings['locations'][message]['roles']

            # Find actual message,
            msg = await client.get_message(client.get_channel(channel), int(message))

            # Add some starter emojis,
            for role in roles:
                get = discord.utils.get(client.get_all_emojis(), name=role)
                if get == None:
                    get = emoji.emojize(role)
                await client.add_reaction(msg, get)

            for reaction in msg.reactions:
                print(reaction.emoji)
                reactors = []
                after = None
                while True:
                    count = 0
                    for user in await client.get_reaction_users(reaction, limit=100, after=after):
                        reactors.append(user)
                        after = user
                        count += 1
                    
                    if count < bindings['settings']['chunk']:
                        break
                for user in all_users:
                    for role in roles:
                        role_obj = discord.utils.get(reaction.message.server.roles, name=roles[role])
                        # print(reaction.emoji, role, reaction.custom_emoji, emoji_equal(reaction.emoji, role, reaction.custom_emoji))
                        if emoji_equal(reaction.emoji, role, reaction.custom_emoji):
                            if user in reactors:
                                if role_obj not in user.roles:
                                    print('GIVE: {} to {}.'.format(role, user))
                                    await client.add_roles(reaction.message.server.get_member(user.id), role_obj)
                            else:
                                if role_obj in user.roles:
                                    print('TAKE: {} from {}.'.format(role, user))
                                    await client.remove_roles(user, role_obj)
            
            # for reaction in msg.reactions:
            #     for role in roles:
            #         ignore_total = []

            #         role_obj = discord.utils.get(reaction.message.server.roles, name=roles[role])

            #         if emoji_equal(reaction.emoji, role, reaction.custom_emoji):

            #             while True:
            #                 ignore = []
            #                 after = None
            #                 for user in await client.get_reaction_users(reaction, limit=100, after=after):
            #                     after = user
            #                     ignore.append(user.id)
            #                     ignore_total.append(user.id)
            #                     await client.add_roles(reaction.message.server.get_member(user.id), role_obj)
                        
            #                 print(len(ignore))

            #                 if len(ignore) < 100:
            #                     break

            #         for user in all_users:
            #             if user.id not in ignore_total:
            #                 print(role)
            #                 await client.remove_roles(user, role_obj)

        # Give bot/discord a rest,
        print("Before")
        await asyncio.sleep(bindings['settings']['refresh'])
        print("After")

client.run('NTIwMTY5NTI1OTIxMTg1ODAz.Dup9SQ.e36bawPIMfsHXCyRrBCSBKrOXhM')
