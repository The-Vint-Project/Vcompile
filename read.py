class VINTFile():

    def __init__(self, fileName: str) -> None:
        self.__fileName = fileName
        self.__fileObject = open(fileName, "a+")
        self.__fileObject.seek(0)
        self.__fileContentsI = self.__fileObject.read()
        self.fileContents = self.__fileContentsI
        self.__options = {
            "CATCODES": [
                ["\\"],  # Start Command
                ["{"],  # Start Group
                ["}"],  # End Group
                ["@"],  # Mode Switch
                ["\n", "\r"],  # End Of Line
                [" ", "\t"],  # Spacer
                ["&"],  # Alignment char
                ["$"],  # Variable marker
                [],  # Short Command - langauge defined
                ["%"],  # Comment
                [],  # Other
                [],  # Invalid
                [],
                []
            ],
            "COMMANDCODES": [  # Langauge defined, in VINT =-+^_()[]:|<>~-≈#*`
            ],
            "age": 18,
            "name": "Luca Di Bona"
        }

    def parse(self) -> None:

        def parseStatement(self, statement: str) -> int:
            pass

            def getCatCode(self, char: str) -> int:
                """
                Generates the category code of a character

                Args:
                    char (char): the character analysed

                Returns:
                    int: the category code of the character

                """

                for i,val in enumerate(self.__options["CATCODES"]):
                    for j in val:
                        if char == j:
                            return(i)

            curCatCode = 0
            curStatement = ""
            curSpacer = ""
            statementMode = True #statement mode or spacer mode

            for i in self.fileContents:
                prevCatCode = curCatCode
                curCatCode = getCatCode(self,i)
                if statementMode:
                    if i in self.__options["CATCODES"][5]: #Spacer
                        statementMode = False
                        curSpacer += i
