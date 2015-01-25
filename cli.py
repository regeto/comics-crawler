import updater


def wait_for_argument(prefix='de'):
    return input(pre[prefix])


def respond_to_argument(argument):
    if argument == "":
        return
    asplit = argument.split(" ")
    key = asplit[0].lower()
    args = " ".join(asplit[1:]).strip()
    if key in switch:
        if args == '':
            switch[key]()
        else:
            switch[key](args)
    else:
        print(pre['err'] + key + " is not a valid argument!")
    return


def parse_update(argument=""):
    asplit = argument.split(" ")
    key = asplit[0].lower()
    args = " ".join(asplit[1:]).strip()
    if key in switch_update:
        if args == '':
            switch_update[key]()
        else:
            switch_update[key](args)
    else:
        print(pre['err'] + key + " is not a valid argument!")
    return

def show_help(argument=""):
    print()
    if argument == "":
        print(pre['help'] + "usage: argument [params]")
        print()
        print(pre['help'] + "arguments:")
        print("h, help -- show this help message")
        print("h, help [argument] -- show help message for specific argument")
        print("u, update -- update from all crawlers")
        print("u, update [crawler] -- update from specific crawler")
        print()
        print(pre['help'] + "optional parameters will be passed along to the specific method.")
    if argument in ["u", "update"]:
        print(pre['help'] + "usage: update [crawler]")
        print()
        print(pre['help'] + "optional arguments:")
        print()
        print("None, all, any -- update from all crawlers")
        print("bato, batoto, bato.to -- update from batoto")
        print("dynasty, dyasty-reader, dynasty-scans, dynasty-scans.com -- update from dynasty")
        print("eden, mangaeden, mangaeden.com -- update from mangaeden")
        print("kawai, kawaii, kawaii-scans, kawaii-reader, kawaii.ca -- update from kawaii")
        print("oots, giantitp, giantitp.com -- update oots")
        print("smack, smackjeeves, smackjeeves.com -- update from smackjeeves")
    print()

pre = dict(
    de=":> ",
    check="checking:> ",
    update="updating:> ",
    download="downloading:> ",
    help="help:> ",
    err="error:> ",
)

switch = dict()
for x in ["update", "u", "ud"]:
    switch[x] = parse_update
for x in ["h", "help"]:
    switch[x] = show_help

switch_update = dict()
for x in ["", "all", "any"]:
    switch_update[x] = updater.update_all
for x in ["bato", "batoto", "bato.to"]:
    switch_update[x] = updater.update_batoto
for x in ["dynasty", "dynasty-reader", "dynasty-scans", "dynasty-scans.com"]:
    switch_update[x] = updater.update_dynasty
for x in ["eden", "mangaeden", "mangaeden.com"]:
    switch_update[x] = updater.update_eden
for x in ["kawai", "kawaii", "kawaii-scans", "kawaii-reader", "kawaii.ca"]:
    switch_update[x] = updater.update_kawaii
for x in ["oots", "giantitp", "giantitp.com"]:
    switch_update[x] = updater.update_oots
for x in ["smack", "smackjeeves", "smackjeeves.com"]:
    switch_update[x] = updater.update_all


# cli
print("Welcome to the comics-crawler command-line interface!")
arg = wait_for_argument().strip()
while arg != "exit":
    respond_to_argument(arg)
    arg = wait_for_argument().strip()
