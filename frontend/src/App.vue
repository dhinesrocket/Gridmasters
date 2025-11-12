<template>
  <div class="terminal-container">
    <div class="terminal-header">
      <span class="terminal-title">GRIDMASTERS v1.0.0</span>
      <span class="terminal-buttons">
        <span class="btn-minimize">_</span>
        <span class="btn-maximize">□</span>
        <span class="btn-close">×</span>
      </span>
    </div>
    
    <div class="terminal-body">
      <div class="terminal-prompt">
        <span class="prompt-user">user@gridmasters</span>:<span class="prompt-path">~</span>$ 
        <span class="prompt-command">./sudoku</span>
      </div>
      
      <div class="terminal-output">
        <pre class="ascii-art">
 ██████╗ ██████╗ ██╗██████╗ ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ███████╗
██╔════╝ ██╔══██╗██║██╔══██╗████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝
██║  ███╗██████╔╝██║██║  ██║██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝███████╗
██║   ██║██╔══██╗██║██║  ██║██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗╚════██║
╚██████╔╝██║  ██║██║██████╔╝██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║███████║
 ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝
        </pre>
        
        <div class="game-mode-select" v-if="!gameStarted">
          <p class="terminal-text">&gt; SELECT GAME MODE:</p>
          <div class="menu-options">
            <button @click="startGame('standard')" class="menu-btn">
              [1] STANDARD SUDOKU (9x9)
            </button>
            <button @click="startGame('hex')" class="menu-btn">
              [2] HEX SUDOKU (16x16)
            </button>
          </div>
          
          <p class="terminal-text" v-if="gameMode">&gt; SELECT DIFFICULTY:</p>
          <div class="menu-options" v-if="gameMode">
            <button @click="loadPuzzle('easy')" class="menu-btn">
              [E] EASY
            </button>
            <button @click="loadPuzzle('medium')" class="menu-btn">
              [M] MEDIUM
            </button>
            <button @click="loadPuzzle('hard')" class="menu-btn">
              [H] HARD
            </button>
          </div>
        </div>
        
        <GameBoard
          v-if="gameStarted && puzzle"
          :puzzle="puzzle"
          :initialPuzzle="initialPuzzle"
          :gameMode="gameMode"
          :loading="loading"
          @cell-update="updateCell"
          @validate="validateSolution"
          @hint="getHint"
          @reset="resetGame"
        />
        
        <div v-if="message" class="terminal-message" :class="messageType">
          <p>&gt; {{ message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import GameBoard from './components/GameBoard.vue'
import { sudokuApi } from './services/api'

export default {
  name: 'App',
  components: {
    GameBoard
  },
  setup() {
    const gameMode = ref(null)
    const gameStarted = ref(false)
    const puzzle = ref(null)
    const initialPuzzle = ref(null)
    const loading = ref(false)
    const message = ref('')
    const messageType = ref('info')
    
    const startGame = (mode) => {
      gameMode.value = mode
    }
    
    const loadPuzzle = async (difficulty) => {
      loading.value = true
      message.value = `Loading ${difficulty} ${gameMode.value} puzzle...`
      messageType.value = 'info'
      
      try {
        const response = gameMode.value === 'standard' 
          ? await sudokuApi.getSudokuPuzzle(difficulty)
          : await sudokuApi.getHexSudokuPuzzle(difficulty)
        
        puzzle.value = JSON.parse(JSON.stringify(response.puzzle))
        initialPuzzle.value = JSON.parse(JSON.stringify(response.puzzle))
        gameStarted.value = true
        message.value = 'Puzzle loaded! Fill in the empty cells (0).'
        messageType.value = 'success'
      } catch (error) {
        message.value = `Error loading puzzle: ${error.message}`
        messageType.value = 'error'
      } finally {
        loading.value = false
      }
    }
    
    const updateCell = ({ row, col, value }) => {
      if (puzzle.value) {
        puzzle.value[row][col] = value
      }
    }
    
    const validateSolution = async () => {
      loading.value = true
      message.value = 'Validating solution...'
      messageType.value = 'info'
      
      try {
        const response = gameMode.value === 'standard'
          ? await sudokuApi.validateSudokuSolution(initialPuzzle.value, puzzle.value)
          : await sudokuApi.validateHexSudokuSolution(initialPuzzle.value, puzzle.value)
        
        if (response.valid) {
          message.value = '🎉 CONGRATULATIONS! Solution is correct!'
          messageType.value = 'success'
        } else {
          message.value = '❌ Solution is incorrect. Keep trying!'
          messageType.value = 'error'
        }
      } catch (error) {
        message.value = `Error validating solution: ${error.message}`
        messageType.value = 'error'
      } finally {
        loading.value = false
      }
    }
    
    const getHint = async () => {
      loading.value = true
      message.value = 'Generating hint...'
      messageType.value = 'info'
      
      try {
        const response = gameMode.value === 'standard'
          ? await sudokuApi.getSudokuHint(puzzle.value)
          : await sudokuApi.getHexSudokuHint(puzzle.value)
        
        message.value = `💡 HINT: ${response.hint}`
        messageType.value = 'hint'
      } catch (error) {
        message.value = `Error getting hint: ${error.message}`
        messageType.value = 'error'
      } finally {
        loading.value = false
      }
    }
    
    const resetGame = () => {
      gameMode.value = null
      gameStarted.value = false
      puzzle.value = null
      initialPuzzle.value = null
      message.value = ''
    }
    
    return {
      gameMode,
      gameStarted,
      puzzle,
      initialPuzzle,
      loading,
      message,
      messageType,
      startGame,
      loadPuzzle,
      updateCell,
      validateSolution,
      getHint,
      resetGame
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'IBM Plex Mono', monospace;
  background: #0a0e14;
  color: #00ff00;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

#app {
  width: 100%;
  max-width: 1400px;
  height: 95vh;
  display: flex;
  flex-direction: column;
}

.terminal-container {
  background: #1a1d24;
  border: 2px solid #00ff00;
  border-radius: 8px;
  box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.terminal-header {
  background: #0d1117;
  padding: 10px 15px;
  border-bottom: 1px solid #00ff00;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.terminal-title {
  color: #00ff00;
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 2px;
}

.terminal-buttons {
  display: flex;
  gap: 10px;
}

.terminal-buttons span {
  cursor: pointer;
  color: #00ff00;
  font-size: 18px;
  padding: 0 8px;
  transition: color 0.2s;
}

.terminal-buttons span:hover {
  color: #00ff00;
  text-shadow: 0 0 10px #00ff00;
}

.terminal-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #0a0e14;
}

.terminal-prompt {
  color: #00ff00;
  margin-bottom: 15px;
  font-size: 14px;
}

.prompt-user {
  color: #00cc00;
  font-weight: 600;
}

.prompt-path {
  color: #0099ff;
}

.prompt-command {
  color: #ffaa00;
  margin-left: 5px;
}

.terminal-output {
  margin-top: 10px;
}

.ascii-art {
  color: #00ff00;
  font-size: 8px;
  line-height: 1.2;
  margin-bottom: 20px;
  text-shadow: 0 0 5px #00ff00;
  overflow-x: auto;
}

.terminal-text {
  color: #00ff00;
  margin: 15px 0;
  font-size: 14px;
}

.menu-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 15px 0;
}

.menu-btn {
  background: transparent;
  border: 1px solid #00ff00;
  color: #00ff00;
  padding: 12px 20px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
  letter-spacing: 1px;
}

.menu-btn:hover {
  background: #00ff00;
  color: #0a0e14;
  box-shadow: 0 0 15px #00ff00;
  transform: translateX(5px);
}

.terminal-message {
  margin: 20px 0;
  padding: 15px;
  border-left: 3px solid #00ff00;
  background: rgba(0, 255, 0, 0.05);
  font-size: 14px;
}

.terminal-message.success {
  border-left-color: #00ff00;
  color: #00ff00;
}

.terminal-message.error {
  border-left-color: #ff0055;
  color: #ff0055;
}

.terminal-message.hint {
  border-left-color: #ffaa00;
  color: #ffaa00;
}

.terminal-message.info {
  border-left-color: #0099ff;
  color: #0099ff;
}

/* Scrollbar styling */
.terminal-body::-webkit-scrollbar {
  width: 8px;
}

.terminal-body::-webkit-scrollbar-track {
  background: #0a0e14;
}

.terminal-body::-webkit-scrollbar-thumb {
  background: #00ff00;
  border-radius: 4px;
}

.terminal-body::-webkit-scrollbar-thumb:hover {
  background: #00cc00;
}

/* Loading animation */
@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.loading::after {
  content: '▌';
  animation: blink 1s infinite;
}
</style>
