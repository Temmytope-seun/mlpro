function syncRange(rangeId, inputId, labelId) {
  const range = document.getElementById(rangeId);
  const input = document.getElementById(inputId);
  const label = document.getElementById(labelId);
  if (!range || !input) return;

  range.value = input.value;

  range.addEventListener('input', function () {
    input.value = range.value;
    if (label) label.textContent = range.value;
  });

  input.addEventListener('input', function () {
    let val = Math.max(0, Math.min(100, Number(input.value) || 0));
    range.value = val;
    if (label) label.textContent = val;
  });
}

function gradeFor(score) {
  if (score >= 90) return { letter: 'A', cls: 'grade-a', tone: 'success' };
  if (score >= 75) return { letter: 'B', cls: 'grade-b', tone: 'primary' };
  if (score >= 60) return { letter: 'C', cls: 'grade-c', tone: 'warning' };
  return { letter: 'D', cls: 'grade-d', tone: 'danger' };
}

function animateGauge(score) {
  const ring = document.getElementById('gaugeRing');
  const scoreEl = document.getElementById('gaugeScore');
  const pillEl = document.getElementById('gradePill');
  const insightEl = document.getElementById('insightList');
  if (!ring || !scoreEl) return;

  const grade = gradeFor(score);
  ring.style.setProperty('--pct', 0);
  scoreEl.textContent = '0';

  requestAnimationFrame(function () {
    ring.style.setProperty('--pct', score);
  });

  let current = 0;
  const duration = 900;
  const start = performance.now();

  function step(ts) {
    const progress = Math.min(1, (ts - start) / duration);
    current = Math.round(progress * score);
    scoreEl.textContent = current;
    if (progress < 1) {
      requestAnimationFrame(step);
    }
  }
  requestAnimationFrame(step);

  if (pillEl) {
    pillEl.innerHTML = `<span class="grade-pill ${grade.cls}">Grade ${grade.letter}</span>`;
  }

  if (insightEl) {
    let message;
    if (score >= 90) {
      message = 'Outstanding performance predicted — this student is on track to excel.';
    } else if (score >= 75) {
      message = 'Solid performance predicted — above-average outcome expected.';
    } else if (score >= 60) {
      message = 'Average performance predicted — some additional support could help.';
    } else {
      message = 'Below-average performance predicted — this student may benefit from extra support.';
    }
    insightEl.innerHTML = `<div class="insight-line"><i class="bi bi-lightbulb-fill"></i><span>${message}</span></div>`;
  }
}
