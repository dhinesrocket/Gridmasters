/**
 * Tests for GameBoard component
 */
import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import GameBoard from '../src/components/GameBoard.vue'

describe('GameBoard.vue', () => {
  let wrapper
  const mockPuzzle = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8]
  ]

  const mockInitialPuzzle = JSON.parse(JSON.stringify(mockPuzzle))
  mockInitialPuzzle[0][0] = -1 // Make one cell editable

  beforeEach(() => {
    wrapper = mount(GameBoard, {
      props: {
        puzzle: mockPuzzle,
        initialPuzzle: mockInitialPuzzle,
        gameMode: 'standard',
        loading: false
      }
    })
  })

  it('should render the game board', () => {
    expect(wrapper.find('.game-board-container').exists()).toBe(true)
    expect(wrapper.find('.sudoku-board').exists()).toBe(true)
  })

  it('should render control buttons', () => {
    const buttons = wrapper.findAll('.control-btn')
    expect(buttons.length).toBe(3)
    expect(buttons[0].text()).toContain('HINT')
    expect(buttons[1].text()).toContain('VALIDATE')
    expect(buttons[2].text()).toContain('NEW GAME')
  })

  it('should render 9x9 grid for standard mode', () => {
    const rows = wrapper.findAll('.board-row')
    expect(rows.length).toBe(9)
    
    const cells = wrapper.findAll('.board-cell')
    expect(cells.length).toBe(81)
  })

  it('should distinguish initial cells from editable cells', () => {
    const initialCells = wrapper.findAll('.initial-cell')
    const editableCells = wrapper.findAll('.editable-cell')
    
    expect(initialCells.length).toBeGreaterThan(0)
    expect(editableCells.length).toBeGreaterThan(0)
    expect(initialCells.length + editableCells.length).toBe(81)
  })

  it('should emit cell-update when input changes', async () => {
    const input = wrapper.find('.cell-input')
    await input.setValue('5')
    
    expect(wrapper.emitted('cell-update')).toBeTruthy()
    expect(wrapper.emitted('cell-update')[0]).toEqual([
      { row: 0, col: 0, value: 5 }
    ])
  })

  it('should emit hint event when hint button clicked', async () => {
    const hintButton = wrapper.findAll('.control-btn')[0]
    await hintButton.trigger('click')
    
    expect(wrapper.emitted('hint')).toBeTruthy()
  })

  it('should emit validate event when validate button clicked', async () => {
    const validateButton = wrapper.findAll('.control-btn')[1]
    await validateButton.trigger('click')
    
    expect(wrapper.emitted('validate')).toBeTruthy()
  })

  it('should emit reset event when reset button clicked', async () => {
    const resetButton = wrapper.findAll('.control-btn')[2]
    await resetButton.trigger('click')
    
    expect(wrapper.emitted('reset')).toBeTruthy()
  })

  it('should disable buttons when loading', async () => {
    await wrapper.setProps({ loading: true })
    
    const buttons = wrapper.findAll('.control-btn')
    expect(buttons[0].attributes('disabled')).toBeDefined()
    expect(buttons[1].attributes('disabled')).toBeDefined()
  })

  it('should handle empty cell input', async () => {
    const input = wrapper.find('.cell-input')
    await input.setValue('')
    
    expect(wrapper.emitted('cell-update')).toBeTruthy()
    const lastEmit = wrapper.emitted('cell-update').slice(-1)[0]
    expect(lastEmit[0].value).toBe(-1)
  })

  it('should only accept valid numbers in standard mode', async () => {
    const input = wrapper.find('.cell-input')
    
    // Try invalid input
    await input.setValue('A')
    // Should not emit for invalid input
    const emitCount = wrapper.emitted('cell-update')?.length || 0
    
    // Try valid input
    await input.setValue('5')
    expect(wrapper.emitted('cell-update').length).toBeGreaterThan(emitCount)
  })

  it('should render hex board class for hex mode', async () => {
    await wrapper.setProps({ gameMode: 'hex' })
    
    expect(wrapper.find('.hex-board').exists()).toBe(true)
    expect(wrapper.find('.standard-board').exists()).toBe(false)
  })

  it('should show correct legend for standard mode', () => {
    const legend = wrapper.find('.board-legend p')
    expect(legend.text()).toContain('1-9')
  })

  it('should show correct legend for hex mode', async () => {
    await wrapper.setProps({ gameMode: 'hex' })
    
    const legend = wrapper.find('.board-legend p')
    expect(legend.text()).toContain('0-9, A-F')
  })
})

