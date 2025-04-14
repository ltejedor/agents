document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('characterForm');
  const pointsLeft = document.getElementById('pointsLeft');
  const jsonOutput = document.getElementById('jsonOutput');
  const TOTAL_POINTS = 15;

  // Character bio character count
  document.querySelectorAll('textarea').forEach(textarea => {
    const counter = textarea.parentElement.querySelector('.char-count');
    textarea.addEventListener('input', () => {
      counter.textContent = `${textarea.value.length}/256`;
    });
  });

  // Stat point validation
  function validateStats() {
    const stats = ['stealth', 'strength', 'speed', 'perception', 'cunning'];
    const values = stats.map(stat => parseInt(form[stat].value) || 0);
    const total = values.reduce((sum, val) => sum + val, 0);
    const remaining = TOTAL_POINTS - total;
    pointsLeft.textContent = remaining;
    return remaining >= 0;
  }

  form.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('input', () => {
      if (!validateStats()) {
        input.value = input.dataset.lastValid || 1;
        validateStats();
      } else {
        input.dataset.lastValid = input.value;
      }
    });
  });

  // Stat button handlers
  document.querySelectorAll('.stat-button').forEach(button => {
    button.addEventListener('click', () => {
      const stat = button.dataset.stat;
      const action = button.dataset.action;
      const input = form[stat];
      const currentValue = parseInt(input.value);
      
      if (action === 'increase' && currentValue < 5) {
        input.value = currentValue + 1;
      } else if (action === 'decrease' && currentValue > 1) {
        input.value = currentValue - 1;
      }
      
      input.dispatchEvent(new Event('input'));
    });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!validateStats()) {
      alert('Please make sure your stat points add up to 15!');
      return;
    }

    const characterData = {
      name: form.name.value,
      appearance: `A ${form.material.value} sockpuppet with a ${form.pattern.value} pattern, ${form.eyes.value}${form.accessories.value !== 'none' ? `, and ${form.accessories.value}` : ''}. Dark avatar 3D realistic sockpuppet with haunted gothic background.`,
      bio: {
        tragicBackstory: form.backstory.value,
        strategyForKilling: form.killStyle.value,
        strategyForSurvival: form.catchphrase.value
      },
      stats: {
        stealth: parseInt(form.stealth.value),
        strength: parseInt(form.strength.value),
        speed: parseInt(form.speed.value),
        perception: parseInt(form.perception.value),
        cunning: parseInt(form.cunning.value)
      }
    };

    jsonOutput.style.display = 'block';
    jsonOutput.textContent = JSON.stringify(characterData, null, 2);
  });
});