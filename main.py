import unirest

class HangmanGame(object):
    hangmanStates = ["""
   _________
    |/        
    |              
    |                
    |                 
    |               
    |                   
    |___                 
    """,

"""
   _________
    |/   |      
    |              
    |                
    |                 
    |               
    |                   
    |___                 
    """,

"""
   _________       
    |/   |              
    |   (_)
    |                         
    |                       
    |                         
    |                          
    |___                       
    """,

"""
   ________               
    |/   |                   
    |   (_)                  
    |    |                     
    |    |                    
    |                           
    |                            
    |___                    
    """,


"""
   _________             
    |/   |               
    |   (_)                   
    |   /|                     
    |    |                    
    |                        
    |                          
    |___                          
    """,


"""
   _________              
    |/   |                     
    |   (_)                     
    |   /|\                    
    |    |                       
    |                             
    |                            
    |___                          
    """,



"""
   ________                   
    |/   |                         
    |   (_)                      
    |   /|\                             
    |    |                          
    |   /                            
    |                                  
    |___                              
    """,

"""
   ________
    |/   |     
    |   (_)    
    |   /|\           
    |    |        
    |   / \        
    |               
    |___           
    """
                     ]


    def __init__(self):
        self.word = self.randWord()
        self.numLetters = len(self.word)
        self.wordGuessed = self.generateUnderscores()
        self.wrongGuesses = 0
        self.lettersGuessed = []
        print(self.getHangmanString())
        print(self.wordGuessed)

    def getHangmanString(self):
        return self.hangmanStates[self.wrongGuesses]

    def generateUnderscores(self):
        string = ""
        numUnderscores = 0
        while (numUnderscores < self.numLetters):
            if (self.word[numUnderscores] == " "):
                string += " "
            else:
                string += "_"
            numUnderscores += 1
        return string

    def randWord(self):
        response = unirest.get("https://wordsapiv1.p.mashape.com/words/?random=true&lettersMax=6",
                               headers={
                                   "X-Mashape-Key": "6VxNSpyV7cmshytyYUDdpnFon8Vap1OznBPjsnamMMPU7ie8Yg",
                                   "Accept": "application/json"
                               })
        return str(response.body["word"])

    #returns list of all indexes in a str toSearch where a substring sub exists
    #from calls external to the function padding should always equal 0
    def find_all(self, toSearch, sub, padding):
        start = 0
        toReturn = []
        if (sub in toSearch and len(toSearch) > 0):
            start = str.index(toSearch, sub)
            toReturn.append(start + padding)
        else:
            #when all substring instances have been found
            return []
        #adds all other substrings in the word
        toReturn.extend(self.find_all(toSearch[start + 1:], sub, start + 1))        
        return toReturn
        


    def guessLetter(self, letter):
        if (len(letter) != 1):
            print("Please enter a single character")
            return

        if (letter.lower() in self.wordGuessed.lower() or  letter in self.lettersGuessed):
            print("You already guessed that letter")
            return

        if (letter in self.word):
            self.lettersGuessed.append(letter)
            indexes = []
            indexes.extend(self.find_all(self.word, letter, 0))
            print(indexes)
            for i in indexes:
                if (i == 0):
                    self.wordGuessed = letter + self.wordGuessed[i + 1:]
                elif (i == len(self.word) - 1):
                    self.wordGuessed = self.wordGuessed[:i] + letter
                else:
                    self.wordGuessed = self.wordGuessed[:int(i)] + letter + self.wordGuessed[int(i) + 1:]
            print(self.getHangmanString())
            print(self.wordGuessed)
            print("Letters guessed: " + str(self.lettersGuessed))
            return

        else:
            self.wrongGuesses += 1
            print(self.getHangmanString())
            print("Your letter was not a part of the word")
            self.lettersGuessed.append(letter)
            print(self.getHangmanString())
            print(self.wordGuessed)
            print("Letters guessed: " + str(self.lettersGuessed))
            return











if __name__ == '__main__':
    quit = False
    leave = "n"
    while (not quit):
        game = HangmanGame()
        while (game.wrongGuesses < 7 and "_" in  game.wordGuessed):
            game.guessLetter(raw_input("Please guess a letter:\n"))
        leave = ""
        if (game.wrongGuesses >= 7):
            leave = raw_input("You lose. The word was " + game.word + ". Play again? (y/n)\n")
        elif ("_" not in game.wordGuessed):
            leave = raw_input("You win. Play again? (y/n)\n")
        if (leave.lower() == 'n'):
            quit = True

