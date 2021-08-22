
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
                [],  # Letter 12
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
            mode = "statement" #statement/spacer/[pre]command/comment
            ifStatementMode = True #statement mode or spacer mode
            ifCommandMode = False #true if in command
            groupLevel = 0
            line = 0
            groupings = [[]]

            self.fileContents += "X" #adds an extra character to text that will be processed
            for i in self.fileContents:

                prevCatCode = curCatCode
                curCatCode = getCatCode(self,i)

                if mode == "command":

                    if len(curStatement) > 1:

                        if i in self.__options["CATCODES"][0]:

                            #TODO flag as command

                            self.__statements.append([curStatement,""])
                            curStatement = i

                        elif i in self.__options["CATCODES"][1]: #Start Group
                            groupings[groupLevel].append([len(self.__statements)+1])
                            self.__statements.append([curStatement,""])
                            curStatement = i
                            curSpacer = ''
                            groupLevel += 1
                            if len(groupings) <= groupLevel:
                                groupings.append([])

                        elif i in self.__options["CATCODES"][2]: #End Group
                            groupLevel -= 1
                            groupings[groupLevel][-1].append(len(self.__statements)+1)
                            if groupLevel < 0:
                                raise Exception(f"Closing brace without matching opening brace on line {line}")
                            else:
                                self.__statements.append([curStatement,""])
                                curStatement = i
                                curSpacer = ''

                                #TODO error on \test{}}

                        elif i in (self.__options["CATCODES"][5] + self.__options["CATCODES"][4]):
                            if i in self.__options["CATCODES"][4]:
                                line += 1
                            mode = spacer
                            curSpacer += i

                        elif curCatCode == prevCatCode:
                            curStatement += i

                        else:
                            self.__statements.append([curStatement,""])
                            curStatement = i
                            curSpacer = ""

                    else:

                        if i in (self.__options["CATCODES"][0] + self.__options["CATCODES"][1] +
                        self.__options["CATCODES"][2] + self.__options["CATCODES"][3] +
                        self.__options["CATCODES"][4] + self.__options["CATCODES"][5] +
                        self.__options["CATCODES"][6] + self.__options["CATCODES"][7] +
                        self.__options["CATCODES"][9]):

                            if i in self.__options["CATCODES"][4]:
                                line += 1

                            curStatement += i
                            mode = "statement"
                            self.__statements.append([curStatement,""])
                            curStatement = ""

                        else:
                            curStatement += i

                elif mode == "statement":

                    if i in (self.__options["CATCODES"][5] + self.__options["CATCODES"][4]): #Spacer or new line
                        if i in self.__options["CATCODES"][4]:
                            line += 1
                        mode = "spacer"
                        curSpacer += i

                    elif i in self.__options["CATCODES"][0]:
                        mode = "precommand"
                        self.__statements.append([curStatement,""])
                        curStatement = i
                        curSpacer = ""

                    elif i in self.__options["CATCODES"][1]: #Start Group
                        groupings[groupLevel].append([len(self.__statements)+1])
                        self.__statements.append([curStatement,""])
                        curStatement = i
                        curSpacer = ''
                        groupLevel += 1
                        if len(groupings) <= groupLevel:
                            groupings.append([])

                    elif i in self.__options["CATCODES"][2]: #End Group
                        groupLevel -= 1
                        groupings[groupLevel][-1].append(len(self.__statements)+1)
                        if groupLevel < 0:
                            raise Exception(f"Closing brace without matching opening brace on line {line}")
                        else:
                            self.__statements.append([curStatement,""])
                            curStatement = i
                            curSpacer = ''

                    elif curCatCode == prevCatCode:
                        curStatement += i

                    else:
                        self.__statements.append([curStatement,""])
                        curStatement = i
                        curSpacer = ''

                else:

                    if i in self.__options["CATCODES"][5]: #Spacer
                        curSpacer += i

                    elif i in self.__options["CATCODES"][0]:
                        mode = "precommand"
                        self.__statements.append([curStatement,curSpacer])
                        curStatement = i
                        curSpacer = ""

                    elif i in self.__options["CATCODES"][4]: #New line
                        curSpacer += i
                        line += 1

                    elif i in self.__options["CATCODES"][1]: #Start Group
                        groupings[groupLevel].append([len(self.__statements)+1])
                        mode = "statement"
                        groupLevel += 1
                        if len(groupings) <= groupLevel:
                            groupings.append([])
                        self.__statements.append([curStatement,curSpacer])
                        curStatement = i
                        curSpacer = ''

                    elif i in self.__options["CATCODES"][2]: #End Group
                        mode = "statement"
                        groupLevel -= 1
                        groupings[groupLevel][-1].append(len(self.__statements)+1)
                        if groupLevel < 0:
                            raise Exception(f"Closing brace without matching opening brace on line {line}")
                        else:
                            self.__statements.append([curStatement,curSpacer])
                            curStatement = i
                            curSpacer = ''

                    elif curCatCode == prevCatCode:
                        mode = "statement"
                        curStatement += i

                    else:
                        mode = "statement"
                        self.__statements.append([curStatement,curSpacer])
                        curStatement = i
                        curSpacer = ''

            #check that there are no missing }s
            for i in groupings:
                if len(i) == 0:
                    groupings.remove(i)
                for j in i:
                    if len(j) != 2:
                        raise Exception("Missing closing brace")
            print("here")


        parseStatement(self,self.fileContents)
