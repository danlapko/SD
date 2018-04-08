import unittest
from cli import *

class TestCLIClases(unittest.TestCase):
    def test_cat(self):
        cat = Cat()
        cat.argsFromInput = ["example"]
        self.assertEqual(cat.run(), '1. example text\n')
        cat.argsFromInput.append("example")
        self.assertEqual(cat.run(), '1. example text\n2. example text\n')

    def test_pwd(self):
        pwd = Pwd()
        self.assertTrue(pwd.run(), os.getcwd())
        pwd.argsFromInput = ["ex"]
        with self.assertRaises(Exception):
           pwd.run()

    def test_echo(self):
        echo = Echo()
        self.assertTrue(echo.run() == "\n")
        echo.argsFromInput = ["hello", "world"]
        self.assertTrue(echo.run(), "hello world\n")
        echo.argsFromInput = ["'hello world'"]
        self.assertTrue(echo.run(), "hello world\n")
        echo.argsFromInput = ['"hello world"']
        self.assertTrue(echo.run(), "hello world\n")
        echo.argsFromInput = ['a', '!', 'b', '#']
        self.assertTrue(echo.run(), "a ! b #\n")

    def test_wc(self):
        wc = Wc()
        wc.argsFromInput = ["asdf asdf"]
        self.assertTrue(wc.run(), "1 2 9\n")

        wc.argsFromInput.append("asdf asdf\n")
        self.assertTrue(wc.run(), "1 2 9\n1 2 9\n2 4 18 total\n")

    def test_assignment(self):
        assignment = Assignment()
        assignment.argsFromInput = ["file", "example"]
        assignment.run()

        self.assertIn("file", variabls)
        self.assertTrue(variabls["file"], "example")
        assignment.argsFromInput.append("asdf")
        with self.assertRaises(Exception):
            assignment.run()


    def test_others(self):
        other = Others()
        other.argsFromInput = ["ls"]
        other.run()


    def test_lexer(self):
        global variabls
        variabls["replace"] = "text"
        lexer = Lexer()
        lexer.launch("$som $replace$replace")
        self.assertTrue(lexer.show(), "texttext")
        lexer.launch("$som $replac'e$replace'")
        self.assertTrue(lexer.show(), "e$replace")
        lexer.launch("$replace asdf")
        self.assertTrue(lexer.show(), "text asdf")
        self.assertTrue(lexer.show(), "text asdf")
        lexer.launch("$replaceasdf")
        self.assertTrue(lexer.show, "")

    def test_parser(self):
        parser = Parser()
        cat = Cat()
        cat.argsFromInput = ["example"]
        wc = Wc()
        wc.argsFromInput = []
        other = Others()
        other.argsFromInput = ["ls"]
        assignment = Assignment()
        assignment.argsFromInput = ["file", "example"]
        parser.launch("cat example | wc")
        self.assertTrue(parser.parserOut, [cat, wc])
        parser.launch("file = example")
        self.assertTrue(parser.parserOut, [assignment])
        with self.assertRaises(Exception):
            pasrser.launch("file= example")

    def test_executor(self):
        executor = Executor()
        cat = Cat()
        cat.argsFromInput = ["example"]
        wc = Wc()
        wc.argsFromInput = []
       # print(executor.launch([cat]))
        self.assertTrue(executor.launch([cat]), '1. example text\n')
        self.assertTrue(executor.launch([wc]), '0 0 0\n')
        self.assertTrue(executor.launch([cat, wc]), '0 0 0\n')
        with self.assertRaises(Exception):
            executor.launch([wc, cat])

if __name__ == '__main__':
    run = 0
    unittest.main()