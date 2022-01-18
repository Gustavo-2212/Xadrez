class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.enPassantPossible = ()
        self.enPassantPossibleLog = [self.enPassantPossible]
        self.checkMate = False
        self.staleMate = False  
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        '''Advanced Solution: Check, Checkmate, Stalemate
        self.inCheck = False
        self.pins = []
        self.checks = []'''


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # Pawn Promotion
        if move.isPawnPromotion:
            '''print("Select one of the letters (Q, B, K, R) to promove your pawn:\nQ - Queen\nB - Bishop\nK - Knight\nR - Rook")
            piece = str(input('Chosen piece: '))'''
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # En Passant Move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"

        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible = ()

        # Castle move
        if move.isCastle:
            if move.endCol - move.startCol == 2: # King side castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            else: # Queen side castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        self.enPassantPossibleLog.append(self.enPassantPossible)

        # Castling Rights update
        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                
            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]
        
            # undo castling rights
            self.castleRightLog.pop()
            self.currentCastlingRight = self.castleRightLog[-1]

            # undo the castle moves
            if move.isCastle:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

            self.checkMate = False
            self.staleMate = False
    
    
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False

        #if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
            elif move.pieceCaptured == 'bR':
                if move.endRow == 0:
                    if move.endCol == 0:
                        self.currentCastlingRight.bqs = False
                    elif move.endCol == 7:
                        self.currentCastlingRight.bks = False

    '''Advanced Solution: Check, Checkmate, Stalemate
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        tipo = endPiece[1]

                        if (0 <= j <= 3 and tipo == 'R') or (4 <= j <= 7 and tipo == 'B') or (i == 1 and tipo == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or (tipo == 'Q') or (i == 1 and tipo == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] ==  enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks'''


    ''' Naive Solution: Check, Checkmate, Stalemate'''
    def getValidMoves(self):
        tempEnPassantPossible = self.enPassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range(len(moves) - 1, -1, -1): # Percorrendo a lista de trás p frente para evitar bugs na hora de remover elementos da lista
            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove 
            self.undoMove()
        if len(moves) == 0: # checkmate or stalemate (Rei afogado)
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate, self.staleMate = False, False
        
        self.enPassantPossible = tempEnPassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    def inCheck(self): # Determina se o atual jogador está em check
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, l, c): # Determina se o inimigo pode atacar o quadrado l, c
        self.whiteToMove = not self.whiteToMove # Troca o ponto de vista do jogo
        oppMoves = self.getAllPossibleMoves() # Movimentos do oponente
        self.whiteToMove = not self.whiteToMove # Troca o ponto de vista do jogo para a real perspectiva
        for move in oppMoves:
            if move.endRow == l and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        DIMENSION = len(self.board)
        for l in range(DIMENSION):
            for c in range(DIMENSION): # len(self.board[l])
                turn = self.board[l][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[l][c][1]
                    self.moveFunctions[piece](l, c, moves) 
        return moves

    def getPawnMoves(self, l, c, moves):
        '''Advanced Solution: Check, Checkmate, Stalemate
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == l and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        # Fim do Advanced Solution update'''
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
            enemyColor = "b"
            if self.board[l-1][c] == "--":
                moves.append(Move((l, c), (l-1, c), self.board))
                if l == 6 and self.board[l-2][c] == "--":
                    moves.append(Move((l, c), (l-2, c), self.board))
            if c - 1 >= 0:
                if self.board[l-1][c-1][0] == 'b':
                    moves.append(Move((l, c), (l-1, c-1), self.board))
                elif (l-1, c-1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == l:
                        if kingCol < c:
                            #inside - entre peão e rei; outside - peão e borda
                            insideRange = range(kingCol + 1, c-1)
                            outsideRange = range(c+1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c-2, -1, -1)
                        for i in insideRange:
                            if self.board[l][i] != "--": # something between blocking
                                blockingPiece = True
                        
                        for i in outsideRange:
                            square = self.board[l][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((l, c), (l-1, c-1), self.board, enpassant=True))
            if c + 1 <= 7:
                if self.board[l-1][c+1][0] == 'b':
                    moves.append(Move((l, c), (l-1, c+1), self.board))
                elif (l-1, c+1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == l:
                        if kingCol < c:
                            #inside - entre peão e rei; outside - peão e borda
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c+2, 8)
                        else:
                            insideRange = range(kingCol - 1, c+1, -1)
                            outsideRange = range(c-1, -1, -1)
                        for i in insideRange:
                            if self.board[l][i] != "--": # something between blocking
                                blockingPiece = True
                        
                        for i in outsideRange:
                            square = self.board[l][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((l, c), (l-1, c+1), self.board, enpassant=True))
        else:
            kingRow, kingCol = self.blackKingLocation
            enemyColor = "w"
            if self.board[l+1][c] == "--":
                moves.append(Move((l, c), (l+1, c), self.board))
                if l == 1 and self.board[l+2][c] == "--":
                    moves.append(Move((l, c), (l+2, c), self.board))
            if c - 1 >= 0:
                if self.board[l+1][c-1][0] == 'w':
                    moves.append(Move((l, c), (l+1, c-1), self.board))
                elif (l+1, c-1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == l:
                        if kingCol < c:
                            #inside - entre peão e rei; outside - peão e borda
                            insideRange = range(kingCol + 1, c-1)
                            outsideRange = range(c+1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c-2, -1, -1)
                        for i in insideRange:
                            if self.board[l][i] != "--": # something between blocking
                                blockingPiece = True
                        
                        for i in outsideRange:
                            square = self.board[l][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((l, c), (l+1, c-1), self.board, enpassant=True))
            if c + 1 <= 7:
                if self.board[l+1][c+1][0] == 'w':
                    moves.append(Move((l, c), (l+1, c+1), self.board))
                elif (l+1, c+1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == l:
                        if kingCol < c:
                            #inside - entre peão e rei; outside - peão e borda
                            insideRange = range(kingCol + 1, c-1)
                            outsideRange = range(c+1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c-2, -1, -1)
                        for i in insideRange:
                            if self.board[l][i] != "--": # something between blocking
                                blockingPiece = True
                        
                        for i in outsideRange:
                            square = self.board[l][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((l, c), (l+1, c+1), self.board, enpassant=True))


    def getRookMoves(self, l, c, moves):
        '''Advanced Solution: Check, Checkmate, Stalemate
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == l and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])   
                if self.board[l][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break'''
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = l + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((l, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((l, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, l, c, moves):
        '''Advanced Solution: Check, Checkmate, Stalemate
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == l and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break'''
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = l + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((l, c), (endRow, endCol), self.board))

    def getBishopMoves(self, l, c, moves):
        '''Advanced Solution: Check, Checkmate, Stalemate
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == l and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break'''
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = l + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((l, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((l, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, l, c, moves):
        self.getRookMoves(l, c, moves)
        self.getBishopMoves(l, c, moves)

    def getKingMoves(self, l, c, moves):
       kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
       allyColor = "w" if self.whiteToMove else "b"
       for i in range(8):
           endRow = l + kingMoves[i][0]
           endCol = c + kingMoves[i][1]
           if 0 <= endRow < 8 and 0 <= endCol < 8:
               endPiece = self.board[endRow][endCol]
               if endPiece[0] != allyColor:
                   moves.append(Move((l, c), (endRow, endCol), self.board))
    
    def getCastleMoves(self, l, c, moves):
        if self.squareUnderAttack(l, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(l, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(l, c, moves)
    
    def getKingSideCastleMoves(self, l, c, moves):
        if self.board[l][c+1] == '--' and self.board[l][c+2] == '--':
            if not self.squareUnderAttack(l, c+1) and not self.squareUnderAttack(l, c+2):
                moves.append(Move((l, c), (l, c+2), self.board, castle=True))

    def getQueenSideCastleMoves(self, l, c, moves):
        if self.board[l][c-1] == '--' and self.board[l][c-2] == '--' and self.board[l][c-3] == '--':
            if not self.squareUnderAttack(l, c-1) and not self.squareUnderAttack(l, c-2):
                moves.append(Move((l, c), (l, c-2), self.board, castle=True))


class CastleRights():
    def __init__(self, wKingSide, bKingSide, wQueenSide, bQueenSide):
        self.wks = wKingSide
        self.bks = bKingSide
        self.wqs = wQueenSide
        self.bqs = bQueenSide


class Move():
    rankToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in rankToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enpassant=False, castle=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        self.isEnpassantMove = enpassant
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        self.isCastle = castle
        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, l, c):
        return self.colsToFiles[c] + self.rowsToRanks[l]


    def __str__(self):
        if self.isCastle:
            # "O-O" king side castle
            # "O-O-O" queen side castle
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare



    


