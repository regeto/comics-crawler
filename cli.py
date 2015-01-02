pre = dict(
    de="comics-crawler:> ",
    check="checking:> ",
    update="updating:> ",
    download="downloading:> ",
    help="help:> "
)


def prnt(stuff):
    print(stuff, end="")


def wait_for_argument(prefix='de'):
    return input(pre[prefix])


def respond_to_argument(argument):
    # do stuff
    return


print("Welcome to the comics-crawler command-line interface!")
arg = wait_for_argument()
while arg != "exit":
    respond_to_argument(arg)
    arg = wait_for_argument()
