import os
import sys
import subprocess
from pathlib import Path


class Lexer:
    '''
    You should first launch instance of lexer on inputString
    from console to proceed all occurrences of variables from environment.
    '''

    def __init__(self):
        self.defaultInitilizate()

    def show(self):
        '''
        :return: result of last processed string by this instance
        '''
        return self.lexerOut

    def defaultInitilizate(self):
        '''
        I am not sure that this method have right to exist but anyway.
        Set default state for instance of Lexer
        '''
        self.lexerOut = ""
        self.skipMode = False
        self.replaceMode = False
        self.curNameOfVariables = ""

    def launch(self, userInput):
        '''
        Take string and replace all occurrences of $name.
        name could include alphabet symbols, numbers, all kind of
        special symbols like !@#$%^&*())_+. Separator for name are
        space, ', '', $
        :param userInput: String
        :return: String
        '''
        self.defaultInitilizate()
        for character in userInput:
            if self.skipMode:  # just skip everything inside of ' '
                if character == '\'':
                    self.skipMode = False

                self.lexerOut += character
                continue

            def dump():
                '''
                Service function. Change variable on it value.
                '''
                if self.curNameOfVariables in variabls:
                    self.lexerOut += variabls[self.curNameOfVariables]
                self.curNameOfVariables = ""
                self.replaceMode = False

            if not character.isspace():
                # get name of variable until next separator
                if self.replaceMode:
                    if character == '$':
                        dump()
                        self.replaceMode = True
                    else:
                        if character == '\'':
                            dump()
                            self.skipMode = True
                            self.lexerOut += character
                        else:
                            self.curNameOfVariables += character
                else:
                    if character == '$':
                        self.replaceMode = True
                    else:
                        if character == '\'':
                            self.skipMode = True
                        self.lexerOut += character
            else:
                if self.replaceMode:
                    dump()
                self.lexerOut += character
        if self.replaceMode:
            if self.curNameOfVariables in variabls:
                self.lexerOut += variabls[self.curNameOfVariables]
            self.replaceMode = False
        if self.skipMode:
            self.skipMode = False
            raise Exception("There is not closing '")


class Token:
    '''
    Abstarct class for diagram
    '''
    pass


class Arguments(Token):  # not used but might be in next version
    pass


class Parametrs(Token):  # not used but might be in next version
    pass


class Command(Token):
    '''
    Abstract class for commands
    All commands use string as interface for communication
    '''

    def __init__(self):
        self.argsFromInput = []
        self.paramsFromInput = []
        self.maxNumberOfArgs = 100
        self.minNumberOfArgs = 0
        self.listOfSupportedParam = {}

    def check(self):
        '''
        command check its parameters before launch
        '''
        if len(self.argsFromInput) > self.maxNumberOfArgs or len(self.argsFromInput) < self.minNumberOfArgs:
            raise Exception("Unsupported numbers of args for command {}".format(self.__class__.__name__))
        for param in self.paramsFromInput:
            if param not in self.listOfSupportedParam:
                raise Exception("Unsupported params for command {}".format(self.__class__.__name__))

    def run(self):
        raise Exception("Unimplemented Command")


class Exit(Command):
    def __init__(self):
        super(Exit, self).__init__()
        self.maxNumberOfArgs = 0
        self.minNumberOfArgs = 0

    def run(self):
        self.check()
        global run
        run = False


class Cat(Command):
    '''
    Cat can only open files by relative name from current directory
    '''

    def __init__(self):
        super(Cat, self).__init__()

    def run(self):
        self.check()
        numberOfRow = 0
        outputString = ""

        for fileName in self.argsFromInput:
            file_in = open(curDir + "/" + fileName, "r")
            for line in file_in.read().splitlines():
                numberOfRow = numberOfRow + 1
                outputString += '{0}. {1}\n'.format(numberOfRow, line)
            file_in.close()

        return outputString


class Wc(Command):
    '''
    Take string for evaluations
    '''

    def __init__(self):
        super(Wc, self).__init__()

    def run(self):
        self.check()
        numberOfLine, numberOfChar, numberOfByte = 0, 0, 0
        outputString = "0 0 0\n"
        for text in self.argsFromInput:
            lineInFile = len(text.splitlines())
            charInFile = len(text.split())
            byteInFile = sys.getsizeof(text) - 49
            outputString += ("{} {} {}\n".format(lineInFile, charInFile, byteInFile))
            numberOfLine, numberOfChar, numberOfByte = numberOfLine + lineInFile, numberOfChar + charInFile, numberOfByte + byteInFile

        if len(self.argsFromInput) > 1:
            outputString += ("{} {} {} {}\n".format(numberOfLine, numberOfChar, numberOfByte, "total"))
        return outputString


class Echo(Command):
    '''
    Just remove '' and ""
    '''

    def run(self):
        self.check()
        output = ""
        for word in self.argsFromInput:
            output += word
            output += " "
        output += "\n"
        return output


class Pwd(Command):
    def __init__(self):
        super(Pwd, self).__init__()
        self.maxNumberOfArgs = 0
        self.minNumberOfArgs = 0

    def run(self):
        self.check()
        return curDir + "\n"


class Assignment(Command):
    '''
    Always execute first.
    '''

    def __init__(self):
        super(Assignment, self).__init__()
        self.maxNumberOfArgs = 2
        self.minNumberOfArgs = 2

    def run(self):
        self.check()
        variabls[self.argsFromInput[0]] = self.argsFromInput[1]


class Cd(Command):
    def __init__(self):
        super(Cd, self).__init__()
        self.maxNumberOfArgs = 1
        self.minNumberOfArgs = 0

    def run(self):
        self.check()

        global curDir
        cur_path = Path(curDir)

        if len(self.argsFromInput) == 0:
            cur_path = Path.home()
        else:
            path_to = Path(self.argsFromInput[0])

            if path_to.is_absolute():
                cur_path = path_to
            else:
                cur_path = cur_path.joinpath(path_to)

        os.chdir(str(cur_path.absolute()))
        curDir = str(Path.cwd())


class Ls(Command):
    def __init__(self):
        super(Ls, self).__init__()
        self.maxNumberOfArgs = 100
        self.minNumberOfArgs = 0

    def _chdir(self, dir=""):

        global curDir
        cur_path = Path(curDir)

        if dir == "":
            cur_path = Path.home()
        else:
            path_to = Path(dir)

            if path_to.is_absolute():
                cur_path = path_to
            else:
                cur_path = cur_path.joinpath(path_to)

        os.chdir(str(cur_path.absolute()))
        curDir = str(Path.cwd())

    def run(self):
        self.check()
        cur_path = Path(curDir)
        output = ""

        if len(self.argsFromInput) == 0:
            output = " ".join(map(lambda path: str(path.relative_to(cur_path)), cur_path.glob("*")))
        elif len(self.argsFromInput) == 1:
            arg = self.argsFromInput[0]

            # print(Path(".").glob("*"))
            arg_path = Path(arg)
            parts = arg_path.parts
            if arg_path.name == "":
                arg += "*"
            output = " ".join(map(str, Path(".").glob(arg)))
        else:
            for arg in self.argsFromInput:
                output += "\n" + arg + ": " + " ".join(
                    map(lambda path: str(path.relative_to(cur_path)), cur_path.glob(arg + "/*")))

        output += "\n"
        return output


class Others(Command):
    '''
    try subprocess for every not implemented comand
    '''

    def run(self):
        try:
            unknownOut = subprocess.check_output(self.argsFromInput)
        except:
            raise Exception("Error in unknown command")
        return unknownOut.decode()


class Buffer:
    '''
    Class exist for purpose of polymorphism.
    Parser use it to keep some word.
    '''

    def __init__(self):
        self.value = ""

    def get(self):
        return self.value

    def put(self, value):
        self.value = value

    def clear(self):
        self.value = ""

    def add(self, char):
        self.value += char


class Parser:
    '''
    parser going to work after lexer just to
    split input string on sequence of commands
    bounded by pipeline
    '''

    def __init__(self):
        self.buf = Buffer()
        self.parserOut = []

    def launch(self, inputString):
        '''
        First phase: split by pipeline with consider of '' and ""
        Second phase: create commands from array of strings
        :param inputString:String
        :return: array of commands
        '''
        self.parserOut = []
        stringsSplitByPipe = []
        # flag for consideration of ''
        skip = False

        for char in inputString:
            if char == '\'':
                skip = not skip
            else:
                if not skip and char == '|':
                    stringsSplitByPipe.append(self.buf.get())
                    self.buf.clear()
                else:
                    self.buf.add(char)
        stringsSplitByPipe.append(self.buf.get())
        self.buf.clear()

        for each in stringsSplitByPipe:
            words = []
            self.buf.clear()
            runnable = True  # if sequnce insade of '' it shold not interpritate
            openSpace = False  # considering sequnce insade "" and ''

            def dump(isRunable):
                '''
                Just to eliminate extra code copy/paste
                '''
                words.append((isRunable, self.buf.get()))
                self.buf.clear()

            for char in each:
                if not openSpace:
                    if char.isspace():
                        dump(True)
                    else:

                        if char == "\"":
                            dump(True)
                            openSpace = True
                        else:
                            if char == '\'':
                                dump(True)
                                openSpace = True
                                runnable = False
                            else:
                                self.buf.add(char)
                else:
                    if char == '\'' or char == '\"':
                        dump(runnable)
                        runnable = True
                        openSpace = False
                    else:
                        self.buf.add(char)
            dump(runnable)
            tmp = []
            for word in words:
                if word[1] != "":
                    tmp.append(word)
            words = tmp

            if len(words) > 0:
                if len(words) > 1 and words[1][1] == '=':
                    tmp = words[0]
                    words[0] = words[1]
                    words[1] = tmp

                if words[0][0] == 0:
                    raise Exception("Syntax error")
                if words[0][1] not in listOfCommands:
                    unknownCommand = Others()
                    for word in words:
                        unknownCommand.argsFromInput.append(word[1])
                    self.parserOut.append(unknownCommand)
                else:
                    command = listOfCommands[words[0][1]]()
                    for id in range(1, len(words)):
                        command.argsFromInput.append(words[id][1])
                    self.parserOut.append(command)


class Executor:
    '''
    Run commands one by one. Also transfer output from one to input other.
    After all commands print result of their work.
    '''

    def launch(self, comandsToRun):
        '''
        :param comandsToRun: array for Commands
        :return: string: result of proceeded command
        '''
        result = None
        for comand in comandsToRun:
            if result is not None:
                comand.argsFromInput.append(result)
            result = comand.run()
        return result


curDir = os.getcwd()
listOfCommands = {"exit": Exit, "wc": Wc, "cat": Cat, "echo": Echo, "pwd": Pwd, "cd": Cd, "ls": Ls, "=": Assignment}
executor = Executor()
parser = Parser()
lexer = Lexer()
variabls = {}
run = True


class Control:
    '''
    Wrap up on infinite loop
    '''

    def launch(self):
        '''
        Start of all program
        '''
        while (run):
            try:
                userInput = input()
                lexer.launch(userInput)
                parser.launch(lexer.lexerOut)
                answer = executor.launch(parser.parserOut)
                if answer is not None:
                    print(answer, end="")
            except Exception as  e:
                print(str(e))
