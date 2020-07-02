const darkSwitch = document.getElementById('darkSwitch');
window.addEventListener('load', () => {
  if (darkSwitch) {
    darkSwitch.addEventListener('change', () => {
      resetTheme();
    });
  }
});

function resetTheme() {
  if (darkSwitch.checked) {
    document.body.setAttribute('data-theme', 'dark');
    
  } else {
    document.body.removeAttribute('data-theme');
    
  }
}
