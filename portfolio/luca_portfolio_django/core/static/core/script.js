function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme');
    
    if (currentTheme === 'dark') {
        body.removeAttribute('data-theme');
    } else {
        body.setAttribute('data-theme', 'dark');
    }
}

// CV Download Functionality
function downloadCV() {
    const cvContent = `CURRÍCULUM VITAE

LUCA VIGNA
Estudiante de Informática & Desarrollador Web

INFORMACIÓN PERSONAL
• Edad: 16 años
• Residencia: San Telmo, CABA
• Teléfono: +54 11 2345-6789
• GitHub: @lucavigna
• Instagram: @lucavigna

HABILIDADES TÉCNICAS
• Lenguajes: Python, HTML5, CSS3, QBasic
• Herramientas: Git, GitHub, Pygame, Tkinter
• Bases de datos: JSON

PROYECTOS DESTACADOS
• Space Invaders - Juego desarrollado en Python con Pygame
• Preguntados - Aplicación de trivia con interfaz gráfica

OBJETIVOS
Convertirme en Desarrollador Full-Stack y seguir 
aprendiendo nuevas tecnologías.`;

    // Crear un blob con el contenido
    const blob = new Blob([cvContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    
    // Crear un enlace temporal para descargar
    const a = document.createElement('a');
    a.href = url;
    a.download = 'CV_Luca_Vigna.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    // Mostrar mensaje de confirmación
    alert('descargaste mi CV bro!');
}

// navegacion
document.addEventListener('DOMContentLoaded', function() {
    // scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});