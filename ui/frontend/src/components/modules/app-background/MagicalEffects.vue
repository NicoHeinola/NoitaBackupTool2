<script lang="ts" setup>
const particleColors = ["#6366f1", "#a855f7", "#ec4899", "#0ea5e9", "#06b6d4"];

// Generate magical particles
const particles = ref<
  Array<{
    id: number;
    left: number;
    top: number;
    size: number;
    duration: number;
    delay: number;
    color: string;
  }>
>([]);

const generateParticles = () => {
  particles.value = Array.from({ length: 15 }, (_, i) => ({
    id: i,
    left: Math.random() * 100,
    top: Math.random() * 100 + 50, // Start below the image area
    size: Math.random() * 4 + 2,
    duration: Math.random() * 8 + 6,
    delay: Math.random() * 2,
    color:
      particleColors[Math.floor(Math.random() * particleColors.length)] ||
      "#6366f1",
  }));
};

onMounted(() => {
  generateParticles();
});
</script>

<template>
  <!-- Magical Effects Layer -->
  <div class="magical-effects">
    <!-- Mystical glow -->
    <div class="mystical-glow"></div>

    <!-- Magical particles -->
    <div
      v-for="particle in particles"
      :key="particle.id"
      class="magical-particle"
      :style="{
        left: particle.left + '%',
        top: particle.top + '%',
        '--particle-size': particle.size + 'px',
        '--particle-duration': particle.duration + 's',
        '--particle-delay': particle.delay + 's',
        '--particle-color': particle.color,
      }"
    ></div>

    <!-- Mystical waves -->
    <div class="mystical-wave wave-1"></div>
    <div class="mystical-wave wave-2"></div>
  </div>

  <!-- Floating orbs (separate to prevent animation reset) -->
  <div class="floating-orbs-container">
    <div class="floating-orb orb-1"></div>
    <div class="floating-orb orb-2"></div>
    <div class="floating-orb orb-3"></div>
  </div>
</template>

<style scoped>
/* Magical Effects */
.magical-effects {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  overflow: hidden;
  pointer-events: none;
}

/* Floating Orbs Container (separate to prevent animation reset) */
.floating-orbs-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  overflow: hidden;
  pointer-events: none;
}

/* Mystical Glow Background */
.mystical-glow {
  position: absolute;
  width: 150%;
  height: 150%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    ellipse at center,
    rgba(167, 139, 250, 0.15) 0%,
    rgba(168, 85, 247, 0.1) 25%,
    rgba(236, 72, 153, 0.05) 50%,
    transparent 70%
  );
  animation: mysticalPulse 8s ease-in-out infinite;
}

/* Magical Particles */
.magical-particle {
  position: absolute;
  width: var(--particle-size);
  height: var(--particle-size);
  background: radial-gradient(
    circle at 30% 30%,
    rgba(255, 255, 255, 0.8),
    var(--particle-color)
  );
  border-radius: 50%;
  filter: blur(1px);
  box-shadow: 0 0 var(--particle-size) var(--particle-color),
    inset 0 0 calc(var(--particle-size) / 2) rgba(255, 255, 255, 0.5);
  animation: floatUp var(--particle-duration) ease-in infinite;
  animation-delay: var(--particle-delay);
}

/* Floating Orbs */
.floating-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(20px);
  opacity: 0.6;
  animation: float 12s ease-in-out infinite;
}

.orb-1 {
  width: 100px;
  height: 100px;
  bottom: 5%;
  left: 15%;
  background: radial-gradient(circle, rgba(167, 139, 250, 0.8), transparent);
  animation-delay: 0s;
}

.orb-2 {
  width: 120px;
  height: 120px;
  bottom: 10%;
  right: 20%;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.7), transparent);
  animation-delay: 4s;
}

.orb-3 {
  width: 80px;
  height: 80px;
  bottom: 15%;
  left: 50%;
  background: radial-gradient(circle, rgba(236, 72, 153, 0.6), transparent);
  animation-delay: 8s;
}

/* Mystical Waves */
.mystical-wave {
  position: absolute;
  width: 100%;
  height: 2px;
  bottom: 25%;
  left: 0;
  background: linear-gradient(
    to right,
    transparent,
    rgba(167, 139, 250, 0.4),
    transparent
  );
  animation: wavePulse 6s ease-in-out infinite;
}

.wave-1 {
  animation-delay: 0s;
  bottom: 30%;
}

.wave-2 {
  animation-delay: 3s;
  bottom: 20%;
  background: linear-gradient(
    to right,
    transparent,
    rgba(168, 85, 247, 0.3),
    transparent
  );
}

/* Animations */
@keyframes mysticalPulse {
  0%,
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.8;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
    opacity: 1;
  }
}

@keyframes floatUp {
  0% {
    transform: translateY(0) translateX(0);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-300px) translateX(20px);
    opacity: 0;
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px) translateX(0px);
  }
  25% {
    transform: translateY(-20px) translateX(10px);
  }
  50% {
    transform: translateY(-40px) translateX(-15px);
  }
  75% {
    transform: translateY(-20px) translateX(15px);
  }
}

@keyframes wavePulse {
  0%,
  100% {
    opacity: 0;
    transform: scaleX(0.5);
  }
  50% {
    opacity: 1;
    transform: scaleX(1);
  }
}
</style>
