<template>
  <div class="empty-bottles-container" v-if="count > 0">
    <div class="bottles-header">
      <span>&gt; EMPTY BOTTLES: {{ count }}</span>
    </div>
    <div class="bottles-grid">
      <div 
        v-for="index in displayCount" 
        :key="index"
        class="empty-bottle"
        :class="{ 'animate-in': index === count }"
      >
        <div class="empty-cap"></div>
        <div class="empty-body"></div>
      </div>
      <div v-if="count > maxDisplay" class="overflow-indicator">
        +{{ count - maxDisplay }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EmptyBottles',
  props: {
    count: {
      type: Number,
      default: 0
    },
    maxDisplay: {
      type: Number,
      default: 10
    }
  },
  computed: {
    displayCount() {
      return Math.min(this.count, this.maxDisplay)
    }
  }
}
</script>

<style scoped>
.empty-bottles-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  background: rgba(0, 255, 0, 0.05);
  border: 2px solid #00ff00;
  border-radius: 8px;
  padding: 12px;
  max-width: 250px;
  box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
}

.bottles-header {
  color: #00ff00;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 10px;
  text-align: center;
  letter-spacing: 1px;
  text-shadow: 0 0 5px rgba(0, 255, 0, 0.8);
  font-family: 'IBM Plex Mono', monospace;
}

.bottles-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  align-items: end;
  justify-items: center;
}

.empty-bottle {
  width: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.6;
  transition: opacity 0.3s, transform 0.3s;
}

.empty-bottle:hover {
  opacity: 1;
  transform: scale(1.2);
}

.empty-bottle.animate-in {
  animation: bottleDrop 0.5s ease-out;
}

@keyframes bottleDrop {
  0% {
    transform: translateY(-50px) scale(0.5);
    opacity: 0;
  }
  60% {
    transform: translateY(5px) scale(1.1);
  }
  100% {
    transform: translateY(0) scale(1);
    opacity: 0.6;
  }
}

.empty-cap {
  width: 8px;
  height: 4px;
  background: transparent;
  border: 1px solid #00ff00;
  border-radius: 2px 2px 0 0;
}

.empty-body {
  width: 18px;
  height: 45px;
  background: transparent;
  border: 1px solid #00ff00;
  border-radius: 0 0 4px 4px;
  position: relative;
  box-shadow: inset 0 0 5px rgba(0, 255, 0, 0.2);
}

.overflow-indicator {
  grid-column: span 5;
  color: #00ff00;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  margin-top: 5px;
  text-shadow: 0 0 8px rgba(0, 255, 0, 0.8);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .empty-bottles-container {
    bottom: 10px;
    right: 10px;
    max-width: 200px;
    transform: scale(0.9);
  }
  
  .bottles-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
  }
}
</style>
