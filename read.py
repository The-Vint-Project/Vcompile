class VINTFile():

    def __init__(self, fileName: str) -> None:
        self.__fileName = fileName
        self.__fileObject = open(fileName, "a+")
        self.__fileObject.seek(0)
        self.__fileContentsI = self.__fileObject.read()
        self.fileContents = self.__fileContentsI
        self.__options = {
            "CATCODES": [
                ["\\"],  # Start Command 0
                ["{"],  # Start Group 1
                ["}"],  # End Group 2
                ["@"],  # Mode Switch 3
                ["\n", "\r"],  # End Of Line 4
                [" ", "\t"],  # Spacer 5
                ["&"],  # Alignment char 6
                ["$"],  # Variable marker 7
                [],  # Short Command - langauge defined 8
                ["%"],  # Comment 9
                [],  # Other 10
                [],  # Invalid 11
                [],
                []
            ],
            "COMMANDCODES": [  # Langauge defined, in VINT =-+^_()[]:|<>~-≈#*`
            ],
            "age": 18,
            "name": "Luca Di Bona"
        }
        self.__statements = []

    def parse(self) -> None:

        def parseStatement(self, statement: str, spacer: str = "") -> None:
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
            groupLevel = 0

            for i in self.fileContents:

                prevCatCode = curCatCode
                curCatCode = getCatCode(self,i)

                if statementMode:

                    if i in self.__options["CATCODES"][5]: #Spacer
                        statementMode = False
                        curSpacer += i

                    elif i in self.__options["CATCODES"][1]: #Start Group
                        groupLevel += 1
                        curStatement += i

                    elif i in self.__options["CATCODES"][2]: #End Group
                        groupLevel -= 1
                        if groupLevel == 0:
                            pass
                        else:
                            pass

                    elif curCatCode == prevCatCode:
                        curStatement += i

                    else:
                        self.__statements.append([curStatement,""])
                        curStatement = i

        parseStatement(self,self.fileContents)

