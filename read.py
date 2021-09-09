
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
        self.__commands = []

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

            def getEndGroup(self, begin: int, groupings: list) -> int:
                """
                Gets the position of the corresponding end statement from a start statement

                Args:
                    begin (int): the position of the start statement

                Exceptions:
                    start not found: the start is not the begining of a group
                    end not found: the start has no corresponding end

                Returns:
                    int: the position of the end statement
                """
                for i in groupings:
                    for j in i:
                        if begin == j[0]:
                            if len(j) == 2:
                                return(j[1])
                            else:
                                raise Exception("End not found")
                raise Exception("Start not found")

            curCatCode = 0
            curStatement = ""
            curSpacer = ""
            mode = "statement" #statement/spacer/[pre]command/comment
            ifStatementMode = True #statement mode or spacer mode
            ifCommandMode = False #true if in command
            groupLevel = 0
            line = 0
            groupings = [[]]
            commands = []

            self.fileContents += "X" #adds an extra character to text that will be processed
            for i in self.fileContents:

                prevCatCode = curCatCode
                curCatCode = getCatCode(self,i)


                if ifStatementMode:

                    if i in (self.__options["CATCODES"][5] + self.__options["CATCODES"][4]): #Spacer or new line
                        if i in self.__options["CATCODES"][4]:
                            line += 1
                        mode = "spacer"
                        curSpacer += i

                    elif i in self.__options["CATCODES"][0]:
                        mode = "command"
                        self.__statements.append([curStatement,""])
                        curStatement = i
                        curSpacer = ""
                        commands.append(len(self.__statements))
                        curCommand = Command("",i)

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
                        mode = "command"
                        self.__statements.append([curStatement,curSpacer])
                        curStatement = i
                        commands.append(len(self.__statements))
                        curCommand = Command("",i)
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

            #creates lists of opening and closing groups
            groupBegins = []
            groupEnds = []
            for i in groupings:
                for j in i:
                    groupBegins.append(j[0])
                    groupEnds.append(j[1])

            #processes commands
            for i in commands:
                #creates command
                curCommand = Command(self.__statements[i+1][0],(self.__statements[i][0]+self.__statements[i+1][0]))
                #checks if command has arguments
                if self.__statements[i+1][0] == "" and (i+2) in groupBegins:
                    curCommand.ad
                self.__commands.append(curCommand)


            print("here")


        parseStatement(self,self.fileContents)
        print("here")
class Command():

    def __init__(self,name:str,text:str,arguments:list = []) -> None:
        self.name = name
        self.__fullText = text
        self.arguments = arguments

    def setFullText(self, text:str) -> None:
        self.__fullText = text

    def addArgument(self, openText:str, innerStatements:list, endText:str) -> None:
        """
        adds a new argument to the end of the current argument

        Args:
            openText (str): the indicator that argument begins
            innerStatements (list): the statements inside the argument
            endText (str): the indicator that the argument ends
        """
        #deduces inner text
        innerText = ""
        for i in innerStatements:
            innerText += i[0]
            innerText += i[1]
        self.__fullText += (openText + innerText + endText)
        self.arguments.append(innerStatements)
