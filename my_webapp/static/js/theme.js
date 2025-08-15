document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, setting initial theme');
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.getElementById('themeSwitch').checked = savedTheme === 'dark';
});

function toggleTheme() {
    console.log('Toggle clicked');
    const theme = document.getElementById('themeSwitch').checked ? 'dark' : 'light';
    console.log('Switching to', theme);
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
}