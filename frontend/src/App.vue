<template>
  <div class="terminal-container">
    <div class="terminal-header">
      <span class="terminal-title">GRIDMASTERS v1.0.0</span>
      <span class="terminal-buttons">
        <span class="btn-minimize" @click="toggleCredits">_</span>
        <span class="btn-maximize" @click="toggleFullscreen">□</span>
        <span class="btn-close" @click="resetGame">×</span>
      </span>
    </div>
    
    <div class="terminal-body" v-if="!showCredits">
      <div class="terminal-prompt">
        <span class="prompt-user">user@gridmasters</span>:<span class="prompt-path">~</span>$ 
        <span class="prompt-command">./sudo-ku</span>
      </div>
      
      <div class="terminal-output">
        <div v-if="message" class="terminal-message top-message" :class="messageType">
          <p>&gt; {{ message }}</p>
        </div>
        
        <pre class="ascii-art">
 ██████╗ ██████╗ ██╗██████╗ ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ███████╗
██╔════╝ ██╔══██╗██║██╔══██╗████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝
██║  ███╗██████╔╝██║██║  ██║██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝███████╗
██║   ██║██╔══██╗██║██║  ██║██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗╚════██║
╚██████╔╝██║  ██║██║██████╔╝██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║███████║
 ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝
        </pre>
        
        <div class="game-mode-select" v-if="!gameStarted">
          <div class="api-key-input">
            <p class="terminal-text">&gt; ENTER OPENAI API KEY (for AI hints):</p>
            <input 
              v-model="apiKey" 
              type="password" 
              placeholder="sk-proj-..." 
              class="api-key-field"
            />
          </div>
          
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
            <button @click="loadPuzzle('super_easy')" class="menu-btn">
              [S] SUPER EASY (3-4 blanks)
            </button>
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
      </div>
    </div>
    
    <!-- Credits Screen -->
    <div class="terminal-body credits-screen" v-if="showCredits">
      <div class="credits-content">
        <pre class="ascii-art">
 ██████╗██████╗ ███████╗██████╗ ██╗████████╗███████╗
██╔════╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██╔════╝
██║     ██████╔╝█████╗  ██║  ██║██║   ██║   ███████╗
██║     ██╔══██╗██╔══╝  ██║  ██║██║   ██║   ╚════██║
╚██████╗██║  ██║███████╗██████╔╝██║   ██║   ███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝   ╚═╝   ╚══════╝
        </pre>
        
        <div class="credits-section">
          <p class="credits-title">&gt; DEVELOPMENT TEAM</p>
          <p class="credits-item">Backend Developer: Sebastian Canales</p>
          <p class="credits-item">Backend Developer: Claire Oliver</p>
          <p class="credits-item">QA / Testing: Nathanael McClure</p>
          <p class="credits-item">UI Developer: Dillon Hines</p>
          <p class="credits-item">UI Developer: Kassidy Wall</p>
        </div>
        
        <div class="credits-section">
          <p class="credits-title">&gt; SPECIAL THANKS</p>
          <p class="credits-item">Coffee: For keeping us awake</p>
          <p class="credits-item">Copilot: Did literally everything</p>
          <p class="credits-item">Sudoku: For being an awesome puzzle</p>
        </div>
        
        <div class="credits-section">
          <p class="credits-title">&gt; VERSION</p>
          <p class="credits-item">GRIDMASTERS v1.0.0</p>
          <p class="credits-item">Built with Vue.js + Python Flask</p>
          <p class="credits-item">2025 GridMasters Team</p>
        </div>
        
        <button @click="toggleCredits" class="menu-btn back-btn">
          [ESC] BACK TO GAME
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import GameBoard from './components/GameBoard.vue'
import { sudokuApi, getHint } from './services/api'
import { hideCells, validateBoard, isBoardComplete } from './utils/sudokuUtils'

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
    const solution = ref(null) // Store complete solution for validation
    const loading = ref(false)
    const message = ref('')
    const messageType = ref('info')
    const showCredits = ref(false)
    const apiKey = ref('')
    
    const startGame = (mode) => {
      gameMode.value = mode
    }
    
    const toggleCredits = () => {
      showCredits.value = !showCredits.value
    }
    
    const toggleFullscreen = () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen()
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen()
        }
      }
    }
    
    const loadPuzzle = async (difficulty) => {
      loading.value = true
      message.value = 'Puzzle loading...'
      messageType.value = 'info'
      
      // Show "Puzzle loading..." for a few seconds
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      try {
        const response = gameMode.value === 'standard' 
          ? await sudokuApi.getSudokuPuzzle(difficulty)
          : await sudokuApi.getHexSudokuPuzzle(difficulty)
        
        // Store the complete solution
        solution.value = JSON.parse(JSON.stringify(response.solution))
        
        // Hide cells based on difficulty to create the puzzle
        const hiddenPuzzle = hideCells(response.solution, difficulty, gameMode.value)
        puzzle.value = JSON.parse(JSON.stringify(hiddenPuzzle))
        initialPuzzle.value = JSON.parse(JSON.stringify(hiddenPuzzle))
        
        gameStarted.value = true
        message.value = 'Puzzle loaded! Fill in the empty cells.'
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
    
    const validateSolution = () => {
      loading.value = true
      message.value = 'Validating solution...'
      messageType.value = 'info'
      
      try {
        // Check if board is complete
        if (!isBoardComplete(puzzle.value, gameMode.value)) {
          message.value = '⚠️ Puzzle is not complete. Fill in all empty cells.'
          messageType.value = 'error'
          return
        }
        
        // Validate against the stored solution
        const isValid = validateBoard(puzzle.value, solution.value, gameMode.value)
        
        if (isValid) {
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
    
    const getHintLocal = async () => {
      if (!apiKey.value) {
        message.value = '⚠️ Please enter your OpenAI API key first!'
        messageType.value = 'error'
        return
      }
      
      loading.value = true
      message.value = 'Generating hint...'
      messageType.value = 'info'
      
      try {
        // Get hint from stored solution
        const hint = await getHint(puzzle.value, solution.value, gameMode.value, apiKey.value)
        
        if (hint.row === -1) {
          message.value = `💡 ${hint.message}`
          messageType.value = 'hint'
        } else {
          message.value = `💡 HINT: ${hint.message}`
          messageType.value = 'hint'
          
          // Optionally reveal the cell (uncomment to auto-fill)
          // puzzle.value[hint.row][hint.col] = hint.value
        }
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
      solution.value = null
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
      showCredits,
      apiKey,
      startGame,
      loadPuzzle,
      updateCell,
      validateSolution,
      getHint: getHintLocal,
      resetGame,
      toggleCredits,
      toggleFullscreen
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
  display: flex;
  flex-direction: column;
  align-items: center;
}

.terminal-prompt {
  color: #00ff00;
  margin-bottom: 15px;
  font-size: 14px;
  text-align: left;
  width: 100%;
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
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ascii-art {
  color: #00ff00;
  font-size: 8px;
  line-height: 1.2;
  margin-bottom: 20px;
  text-shadow: 0 0 5px #00ff00;
  overflow-x: auto;
  text-align: center;
  width: 100%;
  display: flex;
  justify-content: center;
}

.game-mode-select {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.api-key-input {
  width: 100%;
  max-width: 500px;
  margin-bottom: 30px;
}

.api-key-field {
  width: 100%;
  padding: 12px 15px;
  background: rgba(0, 255, 0, 0.05);
  border: 1px solid #00ff00;
  color: #00ff00;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 14px;
  margin-top: 10px;
  outline: none;
  transition: all 0.2s;
  text-align: center;
}

.api-key-field::placeholder {
  color: rgba(0, 255, 0, 0.4);
}

.api-key-field:focus {
  background: rgba(0, 255, 0, 0.1);
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.3);
}

.terminal-text {
  color: #00ff00;
  margin: 15px 0;
  font-size: 14px;
  text-align: center;
}

.menu-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 15px auto;
  max-width: 400px;
  width: 100%;
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
  text-align: center;
  letter-spacing: 1px;
}

.menu-btn:hover {
  background: #00ff00;
  color: #0a0e14;
  box-shadow: 0 0 15px #00ff00;
  transform: scale(1.02);
}

.terminal-message {
  margin: 20px auto;
  padding: 15px;
  border-left: 3px solid #00ff00;
  background: rgba(0, 255, 0, 0.05);
  font-size: 14px;
  max-width: 600px;
  width: 100%;
  text-align: center;
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

.terminal-message.top-message {
  margin-bottom: 20px;
  margin-top: 0;
  font-size: 16px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
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

/* Credits Screen */
.credits-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.credits-content {
  max-width: 800px;
  width: 100%;
  text-align: center;
}

.credits-section {
  margin: 30px 0;
  padding: 20px;
  border: 1px solid #00ff00;
  background: rgba(0, 255, 0, 0.03);
}

.credits-title {
  color: #00ff00;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  letter-spacing: 2px;
  text-shadow: 0 0 5px #00ff00;
}

.credits-item {
  color: #00cc00;
  font-size: 14px;
  margin: 10px 0;
  line-height: 1.6;
}

.back-btn {
  margin-top: 30px;
  min-width: 250px;
}
</style>
