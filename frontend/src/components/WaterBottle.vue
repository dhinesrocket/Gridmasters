<template>
  <div class="water-bottle-container">
    <div class="water-bottle">
      <div class="bottle-cap"></div>
      <div class="bottle-body">
        <div class="water-level" :style="{ height: waterPercentage + '%' }">
          <div class="water-wave"></div>
        </div>
        <div class="bottle-label">
          <span class="label-text">{{ currentMl.toFixed(1) }} ml</span>
          <span class="label-subtext">{{ tokensUsed }} tokens</span>
        </div>
      </div>
    </div>
    <div class="bottle-stats">
      <p class="stats-line">&gt; TOKENS: {{ tokensUsed }}</p>
      <p class="stats-line">&gt; WATER: {{ currentMl.toFixed(1) }}/{{ bottleCapacity }} ml</p>
      <p class="stats-line">&gt; BOTTLES: {{ bottlesConsumed }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WaterBottle',
  props: {
    tokensUsed: {
      type: Number,
      default: 0
    },
    mlPerToken: {
      type: Number,
      default: 0.03816
    },
    bottleCapacity: {
      type: Number,
      default: 100
    }
  },
  computed: {
    totalMlUsed() {
      return this.tokensUsed * this.mlPerToken
    },
    bottlesConsumed() {
      return Math.floor(this.totalMlUsed / this.bottleCapacity)
    },
    currentMl() {
      const remaining = this.bottleCapacity - (this.totalMlUsed % this.bottleCapacity)
      return remaining === this.bottleCapacity ? this.bottleCapacity : remaining
    },
    waterPercentage() {
      return (this.currentMl / this.bottleCapacity) * 100
    }
  }
}
</script>

<style scoped>
.water-bottle-container {
  position: static;
  margin-top: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  width: 100%;
}

.water-bottle {
  width: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  filter: drop-shadow(0 0 10px rgba(0, 255, 0, 0.3));
}

.bottle-cap {
  width: 30px;
  height: 15px;
  background: #00ff00;
  border: 2px solid #00ff00;
  border-radius: 5px 5px 0 0;
  box-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
}

.bottle-body {
  width: 70px;
  height: 180px;
  background: rgba(0, 150, 255, 0.05);
  border: 2px solid #00ff00;
  border-radius: 0 0 15px 15px;
  position: relative;
  overflow: hidden;
  box-shadow: 
    0 0 10px rgba(0, 255, 0, 0.3),
    inset 0 0 20px rgba(0, 150, 255, 0.1);
}

.water-level {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(
    to top,
    rgba(0, 150, 255, 0.7),
    rgba(0, 180, 255, 0.5)
  );
  transition: height 0.8s ease-out;
  box-shadow: 
    0 0 20px rgba(0, 150, 255, 0.5),
    inset 0 0 10px rgba(0, 180, 255, 0.3);
}

.water-wave {
  position: absolute;
  top: -10px;
  left: -50%;
  right: -50%;
  height: 20px;
  background: rgba(0, 180, 255, 0.4);
  border-radius: 50%;
  animation: wave 3s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% {
    transform: translateX(0) translateY(0);
  }
  50% {
    transform: translateX(20px) translateY(-5px);
  }
}

.bottle-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  z-index: 10;
  pointer-events: none;
}

.label-text {
  color: #00ff00;
  font-size: 12px;
  font-weight: 600;
  text-shadow: 
    0 0 5px rgba(0, 0, 0, 0.8),
    0 0 10px rgba(0, 255, 0, 0.8);
  letter-spacing: 0.5px;
}

.label-subtext {
  color: #00cc00;
  font-size: 9px;
  text-shadow: 
    0 0 5px rgba(0, 0, 0, 0.8),
    0 0 8px rgba(0, 255, 0, 0.6);
}

.bottle-stats {
  background: rgba(0, 255, 0, 0.05);
  border: 1px solid #00ff00;
  padding: 8px 12px;
  border-radius: 4px;
  min-width: 150px;
  box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
}

.stats-line {
  color: #00ff00;
  font-size: 10px;
  margin: 3px 0;
  letter-spacing: 0.5px;
  font-family: 'IBM Plex Mono', monospace;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .water-bottle-container {
    top: 60px;
    right: 10px;
    transform: scale(0.8);
  }
}
</style>
