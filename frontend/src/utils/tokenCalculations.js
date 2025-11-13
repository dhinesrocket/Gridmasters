// Token Tracking Calculation Tests
// Run this in browser console to verify calculations

console.log('=== Token Tracking Calculation Tests ===\n');

const ML_PER_TOKEN = 0.003816;
const BOTTLE_CAPACITY = 500;

function calculateBottleStats(tokensUsed) {
  const totalMl = tokensUsed * ML_PER_TOKEN;
  const bottlesConsumed = Math.floor(totalMl / BOTTLE_CAPACITY);
  const currentMl = BOTTLE_CAPACITY - (totalMl % BOTTLE_CAPACITY);
  const waterPercentage = (currentMl / BOTTLE_CAPACITY) * 100;
  
  return { totalMl, bottlesConsumed, currentMl, waterPercentage };
}

// Test cases
const testCases = [
  { tokens: 0, description: 'No tokens used' },
  { tokens: 1000, description: 'Small usage' },
  { tokens: 10000, description: 'Medium usage' },
  { tokens: 131000, description: 'Almost one bottle' },
  { tokens: 131100, description: 'Just over one bottle' },
  { tokens: 262000, description: 'Almost two bottles' },
  { tokens: 400000, description: 'Three bottles' },
  { tokens: 1000000, description: 'Large usage' }
];

testCases.forEach(test => {
  const stats = calculateBottleStats(test.tokens);
  console.log(`${test.description} (${test.tokens.toLocaleString()} tokens):`);
  console.log(`  Total ML: ${stats.totalMl.toFixed(3)} ml`);
  console.log(`  Bottles Consumed: ${stats.bottlesConsumed}`);
  console.log(`  Current Level: ${stats.currentMl.toFixed(3)} ml (${stats.waterPercentage.toFixed(2)}%)`);
  console.log('');
});

// Verify: How many tokens to empty one bottle?
const tokensPerBottle = BOTTLE_CAPACITY / ML_PER_TOKEN;
console.log(`\n=== Key Metric ===`);
console.log(`Tokens to empty one bottle: ${Math.ceil(tokensPerBottle).toLocaleString()} tokens`);
console.log(`Exact value: ${tokensPerBottle.toFixed(2)} tokens\n`);
