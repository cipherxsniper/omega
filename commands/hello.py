def register(cmds):
    def hello(args):
        print("🧠 Omega says hello:", args)

    cmds["hello"] = hello
