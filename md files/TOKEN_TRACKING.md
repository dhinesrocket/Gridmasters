# Token Tracking and Water Bottle Visualization

## Overview
This feature tracks the number of tokens used per LLM request and visualizes this usage as a draining water bottle. When a bottle is empty, it's displayed in the bottom-right corner of the screen.

## Implementation Details

### Constants
- **ML_PER_TOKEN**: 0.003816 ml of water per token
- **BOTTLE_CAPACITY**: 500 ml per bottle

### Components

#### 1. WaterBottle.vue
Located in: `frontend/src/components/WaterBottle.vue`

A visual component that displays:
- Current water level in the bottle (animated)
- Remaining water in ml
- Total tokens used
- Number of bottles consumed

**Props:**
- `tokensUsed`: Number of tokens consumed
- `mlPerToken`: Water amount per token (default: 0.003816)
- `bottleCapacity`: Capacity of one bottle (default: 500)

**Features:**
- Animated water draining effect
- Wave animation on water surface
- Real-time stats display
- Terminal-themed styling matching the app

#### 2. EmptyBottles.vue
Located in: `frontend/src/components/EmptyBottles.vue`

Displays empty bottles in the bottom-right corner after they've been fully consumed.

**Props:**
- `count`: Number of empty bottles to display
- `maxDisplay`: Maximum bottles to show (default: 10, overflow shows "+N")

**Features:**
- Grid layout for multiple bottles
- Drop animation when new bottle is added
- Overflow indicator for large quantities
- Hover effects on bottles

### State Management (App.vue)

#### Token Tracking State
```javascript
const tokensUsed = ref(0)
const ML_PER_TOKEN = 0.003816
const BOTTLE_CAPACITY = 500

const bottlesConsumed = computed(() => {
  const totalMl = tokensUsed.value * ML_PER_TOKEN
  return Math.floor(totalMl / BOTTLE_CAPACITY)
})

const addTokens = (count) => {
  tokensUsed.value += count
}
```

### LLM Integration (Future)

When implementing LLM for hints, update the `getHintLocal` method:

```javascript
const getHintLocal = async () => {
  loading.value = true
  message.value = 'Generating hint...'
  messageType.value = 'info'
  
  try {
    // Call your LLM API
    const llmResponse = await callLLMApi({
      puzzle: puzzle.value,
      solution: solution.value,
      gameMode: gameMode.value
    })
    
    // Track tokens from the LLM response
    addTokens(llmResponse.tokensUsed)
    
    // Display the hint
    message.value = `💡 HINT: ${llmResponse.hint}`
    messageType.value = 'hint'
  } catch (error) {
    message.value = `Error getting hint: ${error.message}`
    messageType.value = 'error'
  } finally {
    loading.value = false
  }
}
```

### Current Behavior

**Temporary Simulation:**
For demonstration purposes, the system currently simulates token usage (50-150 tokens per hint request). This should be removed when actual LLM integration is implemented.

```javascript
// REMOVE THIS WHEN IMPLEMENTING REAL LLM
const simulatedTokens = Math.floor(Math.random() * 100) + 50
addTokens(simulatedTokens)
```

## Visual Design

### Water Bottle (Top Right)
- Position: Fixed at top-right (80px from top, 20px from right)
- Features terminal-style green glow effects
- Displays real-time water level with smooth animations
- Shows stats panel below the bottle

### Empty Bottles (Bottom Right)
- Position: Fixed at bottom-right (20px from bottom and right)
- Displays up to 10 bottles in a 5-column grid
- Shows overflow count for more than 10 bottles
- Animated drop effect when new bottles are added

## Calculations

### Water Usage
```
Total ML Used = Tokens Used × 0.003816
```

### Bottles Consumed
```
Bottles Consumed = floor(Total ML Used / 500)
```

### Current Bottle Level
```
Current ML = 500 - (Total ML Used % 500)
Water Percentage = (Current ML / 500) × 100
```

## Example Scenarios

### Scenario 1: Small Token Usage
- **Tokens Used**: 1000
- **ML Used**: 3.816 ml
- **Bottles Consumed**: 0
- **Current Level**: 496.184 ml (99.2% full)

### Scenario 2: One Bottle Consumed
- **Tokens Used**: 131,000
- **ML Used**: 499.896 ml
- **Bottles Consumed**: 0
- **Current Level**: 0.104 ml (0.02% full)

### Scenario 3: Multiple Bottles
- **Tokens Used**: 400,000
- **ML Used**: 1526.4 ml
- **Bottles Consumed**: 3
- **Current Level**: 473.6 ml (94.7% full)
- **Empty Bottles Display**: Shows 3 empty bottles

## Future Enhancements

1. **Persist token count** across sessions using localStorage
2. **Add achievement system** for token milestones
3. **Implement token limits** or warnings at certain thresholds
4. **Add sound effects** when bottle empties
5. **Include token cost estimates** before requesting hints
6. **Export usage statistics** for analysis

## Styling

All components use the terminal theme with:
- Primary color: #00ff00 (bright green)
- Background: rgba(0, 255, 0, 0.05) for subtle effects
- Glow effects: box-shadow with green color
- Font: IBM Plex Mono (monospace)
- Animations: Smooth transitions with ease-out timing
