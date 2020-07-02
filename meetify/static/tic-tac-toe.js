
let cornersOpen = []
let edgesOpen = []
var corners = [1, 3, 7, 9]
var edges = [2, 4, 6, 8]
var boardcopy = []

const X_CLASS = 'x'
const CIRCLE_CLASS = 'circle'
const WINNING_COMBINATIONS = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6]
]
let board_1 = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
const cellElements = document.querySelectorAll('[data-cell]')
const board = document.getElementById('board')
const winningMessageElement = document.getElementById('winningMessage')
const restartButton = document.getElementById('restartButton')
const winningMessageTextElement = document.querySelector('[data-winning-message-text]')
let circleTurn
const choice = ["X", "O"]

startGame()

restartButton.addEventListener('click', startGame)

function startGame() {
  circleTurn = false
  cellElements.forEach(cell => {
    cell.classList.remove(X_CLASS)
    cell.classList.remove(CIRCLE_CLASS)
    board_1 = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    cell.removeEventListener('click', handleClick)
    cell.addEventListener('click', handleClick, { once: true })
  })
  winningMessageElement.classList.remove('show')
}

function handleClick(e) {
  const cell = e.target
  board_1[cell.id - 1] = "X"
  var currentClass = X_CLASS
  placeMark(cell, currentClass)
  if (checkWin(currentClass)) {
    endGame(false, X_CLASS)
  }  
  else if (isDraw()) {
    endGame(true)
  }
  else {    
    var id = computer_move()
    board_1[id - 1] = "O"
    cell_computer = document.getElementById(id)
    
    //Final
    currentClass = CIRCLE_CLASS
    placeMark(cell_computer, currentClass)
    if (checkWin(currentClass)) {
      endGame(false, CIRCLE_CLASS)
    } else if (isDraw()) {
      endGame(true)
    }
  }
}

function endGame(draw, cc) {
  if (draw) {
    console.log("dflkj")
    winningMessageTextElement.innerText = 'Draw!'
  }
  else {
    if(cc == CIRCLE_CLASS)
    {
      winningMessageTextElement.innerText = `Computer Won!`
    }
    else
    {
      winningMessageTextElement.innerText = `You Won!`
    }
  }
  winningMessageElement.classList.add('show')
}

function isDraw() {
  return [...cellElements].every(cell => {
    return cell.classList.contains(X_CLASS) || cell.classList.contains(CIRCLE_CLASS)
  })
}

function placeMark(cell, currentClass) {
  cell.classList.add(currentClass)
}

function computer_move(){
  var move = 0
  
  var posssibleMoves = []
  posssibleMoves.length = 0
  cornersOpen.length = 0
  edgesOpen.length = 0
  for(i in board_1)
  {
    if(board_1[i] == " "){
      posssibleMoves.push(parseInt(parseInt(i)+1))
    }
  }

  var move = 0
      
  for(var i in posssibleMoves){
    boardcopy.length = 0
    Array.prototype.push.apply(boardcopy,board_1)
    boardcopy[posssibleMoves[i] - 1] = "O"
    if (
      ((boardcopy[0] == "O" && boardcopy[1] == "O" && boardcopy[2] == "O") ||
      (boardcopy[3] == "O" && boardcopy[4] == "O" && boardcopy[5] == "O") ||
      (boardcopy[6] == "O" && boardcopy[7] == "O" && boardcopy[8] == "O") ||
      (boardcopy[0] == "O" && boardcopy[3] == "O" && boardcopy[6] == "O") ||
      (boardcopy[1] == "O" && boardcopy[4] == "O" && boardcopy[7] == "O") ||
      (boardcopy[2] == "O" && boardcopy[5] == "O" && boardcopy[8] == "O") ||
      (boardcopy[0] == "O" && boardcopy[4] == "O" && boardcopy[8] == "O") ||
      (boardcopy[2] == "O" && boardcopy[4] == "O" && boardcopy[6] == "O"))
    ){
      move = posssibleMoves[i]
      return move
    }
  }


  for(var i in posssibleMoves){
    boardcopy.length = 0
    Array.prototype.push.apply(boardcopy,board_1)
    boardcopy[posssibleMoves[i] - 1] = "X"
    if (((boardcopy[0] == "X" && boardcopy[1] == "X" && boardcopy[2] == "X") ||
      (boardcopy[3] == "X" && boardcopy[4] == "X" && boardcopy[5] == "X") ||
      (boardcopy[6] == "X" && boardcopy[7] == "X" && boardcopy[8] == "X") ||
      (boardcopy[0] == "X" && boardcopy[3] == "X" && boardcopy[6] == "X") ||
      (boardcopy[1] == "X" && boardcopy[4] == "X" && boardcopy[7] == "X") ||
      (boardcopy[2] == "X" && boardcopy[5] == "X" && boardcopy[8] == "X") ||
      (boardcopy[0] == "X" && boardcopy[4] == "X" && boardcopy[8] == "X") ||
      (boardcopy[2] == "X" && boardcopy[4] == "X" && boardcopy[6] == "X"))
    ){
      move = posssibleMoves[i]
      return move
    }
  }
  
  
  for(i=0; i<posssibleMoves.length; i++){
    var k = posssibleMoves[i]
    if (corners.includes(k)){
      cornersOpen.push(k)
    }
  }

  for(i=0; i<posssibleMoves.length; i++){
    var k = posssibleMoves[i]
    if (edges.includes(k)){
      edgesOpen.push(k)
    }
  }

  let p = posssibleMoves.length
  var c = cornersOpen.length
  let e = edgesOpen.length

  if(!include(posssibleMoves, 5) && p==4 && c==3 && e==1 ){
    if(board_1[1] == "X" && board_1[6] == "X" && board_1[5] == "X"){
      move = 9
      return move
    }
    else if(board_1[1] =="X" && board_1[8] =="X" && board_1[3] =="X"){
      move = 7
      return move
    }
    else if(board_1[7] =="X" && board_1[0] =="X" && board_1[3] =="X"){
      move = 7
      return move
    }
    else if(board_1[7] =="X" && board_1[2] =="X" && board_1[5] =="X"){
      move = 1
      return move
    }
    else if(board_1[3] =="X" && board_1[2] =="X" && board_1[7] =="X"){
      move = 1
      return move
    }
    else if(board_1[5] =="X" && board_1[0] =="X" && board_1[1] =="X"){
      move = 2
      return move
    }
    else if(board_1[5] =="X" && board_1[6] =="X" && board_1[7] =="X"){
      move = 9
      return move
    }

  }
  if(!include(posssibleMoves, 5) && p == 6 && e == 2){
    if (board_1[1] == "X" && board_1[3] == "X"){
      move = 1
      return move
    }
    else if( board_1[1] == "X" &&  board_1[5] == "X"){
      move = 3
      return move
    }
    else if( board_1[7] == "X" && board_1[3] == "X"){
      move = 7
      return move
    }
    else if( board_1[7] == "X" && board_1[5] == "X"){
      move = 9
      return move
    }
  }
//// 5!; p==6 e=3 c=3
  if(!include(posssibleMoves, 5) && p == 6 && e == 3 && c == 3){
    if( board_1[1] =="X" && board_1[6] == "X"){
      move = 4
      return move
    }

    else if( board_1[1] =="X" && board_1[8] == "X"){
      move = 6
      return move
    }
    
    else if( board_1[3] == "X" && board_1[2] == "X"){
      move  = 2
      return move
    }

    else if( board_1[3] == "X" && board_1[8] == "X"){
      move = 8
      return move
    }

    else if( board_1[5] =="X" && board_1[0] == "X"){
      move  = 8
      return move
    }

    else if( board_1[5] =="X" && board_1[6] == "X"){
      move = 2
      return move
    }
    
    else if( board_1[7] =="X" && board_1[0] == "X"){
      move  = 4
      return move
    }

    else if( board_1[7] == "X" && board_1[2] == "X"){
      move = 6
      return move
    }
  }

  if (!include(posssibleMoves, 5)){
    if (cornersOpen.length == 4){
      move = selectRandom(cornersOpen)
      return move
    }
  }

/////Corners = 2 ; 5! p = 6
  if (!include(posssibleMoves,5) && p == 6 && c == 2 ){
    if (board_1[4] == "O"){
      if (edgesOpen.length == 4){
        move = selectRandom(edgesOpen)
        return move
      }
    }
    else{
      if (cornersOpen.length > 0){
        move = selectRandom(cornersOpen)
        return move
      }
    }
  }

//////corners = 3
  if (cornersOpen.length == 3){
    if (include(posssibleMoves, 5)){
        move = 5
        return move
    }
    else{
        if (cornersOpen.length > 0){
            move = selectRandom(cornersOpen)
            return move
        }
    }
  }

  if (include(posssibleMoves, 5)){
    move = 5
    return move
  }
////Random Edge
  if(edgesOpen.length > 0){
    move = selectRandom(edgesOpen)
    return move
  }
  
}

function selectRandom(arr){
  var move_1 = arr[Math.floor(Math.random() * arr.length)]
  return move_1
}

/*function swapTurns() {
  circleTurn = !circleTurn
}*/

function include(arr, k){
  for(i = 0; i<arr.length; i++){
    if(k == arr[i]){
      return true
    }
  }
}



function checkWin(currentClass) {
  return WINNING_COMBINATIONS.some(combination => {
    return combination.every(index => {
      return cellElements[index].classList.contains(currentClass)
    })
  })
}

