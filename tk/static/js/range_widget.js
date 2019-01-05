// On an event of kind, for els, call fn
const on = (...kinds) => (...els) => (fn) =>
  kinds.forEach(kind =>
    els.forEach(el => el.addEventListener(kind, fn))
  )

range_widget = function(a, b, o) {
  // 'mousedown' because otherwise you can "lock" the other slider in place at min=max=value
  on('input', 'mousedown')(a, b)(update);

  if (!a.hasAttribute('value')) {
    a.value = a.min;
  }
  if (!b.hasAttribute('value')) {
    b.value = b.max;
  }

  update(); // 1x

  // As the user drags on input, update the available range and visual space for both inputs
  function update({target} = {}) {
    let pivot; // unless otherwise acted on
    
    if (target === a) {
      if (a.valueAsNumber >= Number(a.max)) {
        pivot = Math.min(b.max - 1, Number(a.max) + 2);
      }
    }
    
    if (target === b) {
      if (b.valueAsNumber <= Number(b.min)) {
        pivot = Math.max(a.min, Number(b.min) - 2);
      }
    }
    
    if (pivot != null) {
      a.max = pivot;
      b.min = pivot + 1;
    }
    
    a.style.flexGrow = stepsIn(a);
    b.style.flexGrow = stepsIn(b);
    
    // Print selected range
    o.innerText = `${a.value} - ${b.value}`;
  }

  // Number of discrete steps in an input range
  function stepsIn(el) {
    return Number(el.max) - Number(el.min) + 1;
  }
}
