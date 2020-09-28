import os




def is_owner(ctx):
    return ctx.message.author.id == int(os.environ["OWNER_ID"])


def is_mod(ctx):
    return ctx.message.author.is_mod == 1


def is_psuedo(ctx):
    return ctx.message.author.name == "psuedoo"

def is_psuedoos_channel(ctx):
    return ctx.channel.name == "psuedoo"

def is_lettrebags_channel(ctx):
    return ctx.channel.name == "lettrebag"

def is_arrowspices_channel(ctx):
    return ctx.channel.name == "arrowspice"
