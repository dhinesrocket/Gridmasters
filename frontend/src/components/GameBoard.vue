<template>
  <div class="game-board-container">
    <div class="board-controls">
      <button @click="$emit('hint')" class="control-btn" :disabled="loading">
        [?] GET HINT
      </button>
      <button @click="$emit('validate')" class="control-btn" :disabled="loading">
        [✓] VALIDATE
      </button>
      <button @click="$emit('reset')" class="control-btn">
        [↻] NEW GAME
      </button>
    </div>
    
    <div :class="['sudoku-board', gameMode === 'hex' ? 'hex-board' : 'standard-board']">
      <div
        v-for="(row, rowIndex) in puzzle"
        :key="'row-' + rowIndex"
        class="board-row"
      >
        <div
          v-for="(cell, colIndex) in row"
          :key="'cell-' + rowIndex + '-' + colIndex"
          :class="[
            'board-cell',
            isInitialCell(rowIndex, colIndex) ? 'initial-cell' : 'editable-cell',
            getCellBorderClass(rowIndex, colIndex)
          ]"
        >
          <input
            v-if="!isInitialCell(rowIndex, colIndex)"
            type="text"
            :value="getCellDisplay(cell)"
            @input="handleInput($event, rowIndex, colIndex)"
            maxlength="1"
            class="cell-input"
            :disabled="loading"
          />
          <span v-else class="cell-value">{{ getCellDisplay(cell) }}</span>
        </div>
      </div>
    </div>
    
    <!-- Legend moved to App.vue terminal section -->
  </div>
</template>

<script>
export default {
  name: 'GameBoard',
  props: {
    puzzle: {
      type: Array,
      required: true
    },
    initialPuzzle: {
      type: Array,
      required: true
    },
    gameMode: {
      type: String,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  emits: ['cell-update', 'validate', 'hint', 'reset'],
  methods: {
    isInitialCell(row, col) {
      return this.initialPuzzle[row][col] !== -1
    },
    
    getCellDisplay(cell) {
      if (cell === -1) return ''
      return cell
    },
    
    handleInput(event, row, col) {
      const value = event.target.value.toUpperCase()
      
      if (this.gameMode === 'standard') {
        // Standard mode: only accept 1-9
        if (value === '') {
          this.$emit('cell-update', { row, col, value: -1 })
        } else if (/^[1-9]$/.test(value)) {
          this.$emit('cell-update', { row, col, value: parseInt(value) })
        } else {
          event.target.value = this.getCellDisplay(this.puzzle[row][col])
        }
      } else {
        // Hex mode: accept 0-9, A-F
        if (value === '') {
          this.$emit('cell-update', { row, col, value: -1 })
        } else if (/^[0-9A-F]$/.test(value)) {
          this.$emit('cell-update', { row, col, value: value })
        } else {
          event.target.value = this.getCellDisplay(this.puzzle[row][col])
        }
      }
    },
    
    getCellBorderClass(row, col) {
      const classes = []
      const boxSize = this.gameMode === 'standard' ? 3 : 4
      
      // Right border for box boundaries
      if ((col + 1) % boxSize === 0 && col < this.puzzle[0].length - 1) {
        classes.push('border-right-thick')
      }
      
      // Bottom border for box boundaries
      if ((row + 1) % boxSize === 0 && row < this.puzzle.length - 1) {
        classes.push('border-bottom-thick')
      }
      
      return classes.join(' ')
    }
  }
}
</script>

<style scoped>
.game-board-container {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.board-controls {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.control-btn {
  background: transparent;
  border: 1px solid #00ff00;
  color: #00ff00;
  padding: 10px 18px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 1px;
}

.control-btn:hover:not(:disabled) {
  background: #00ff00;
  color: #0a0e14;
  box-shadow: 0 0 15px #00ff00;
  transform: translateY(-2px);
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.sudoku-board {
  display: inline-block;
  border: 2px solid #00ff00;
  background: #0d1117;
  padding: 2px;
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
}

.board-row {
  display: flex;
}

.board-cell {
  width: 40px;
  height: 40px;
  border: 1px solid #1a4d1a;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.hex-board .board-cell {
  width: 35px;
  height: 35px;
}

.border-right-thick {
  border-right: 2px solid #00ff00;
}

.border-bottom-thick {
  border-bottom: 2px solid #00ff00;
}

.initial-cell {
  background: #0a3d0a;
}

.initial-cell .cell-value {
  color: #00ff00;
  font-weight: 600;
  font-size: 16px;
  text-shadow: 0 0 5px #00ff00;
}

.editable-cell {
  background: #0a0e14;
}

.cell-input {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  color: #66ff66;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 16px;
  text-align: center;
  outline: none;
  caret-color: #00ff00;
}

.hex-board .cell-input,
.hex-board .cell-value {
  font-size: 14px;
}

.cell-input:focus {
  background: rgba(0, 255, 0, 0.05);
  box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.2);
}

.cell-input:disabled {
  cursor: not-allowed;
}

.board-legend {
  margin-top: 15px;
  padding: 10px;
  border-left: 2px solid #00ff00;
  background: rgba(0, 255, 0, 0.03);
  text-align: center;
  max-width: 500px;
}

.board-legend p {
  color: #00cc00;
  font-size: 12px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .board-cell {
    width: 32px;
    height: 32px;
  }
  
  .hex-board .board-cell {
    width: 25px;
    height: 25px;
  }
  
  .cell-input,
  .cell-value {
    font-size: 14px;
  }
  
  .hex-board .cell-input,
  .hex-board .cell-value {
    font-size: 11px;
  }
}
</style>
