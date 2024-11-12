// static/drawing.js

const canvas = document.getElementById('gridCanvas');
const ctx = canvas.getContext('2d');
const cellSize = 25; // 1 клетка = 1 метр
let points = [];

// Функция рисования сетки на Canvas
function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    for (let x = 0; x <= canvas.width; x += cellSize) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
    }
    for (let y = 0; y <= canvas.height; y += cellSize) {
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
    }
    ctx.strokeStyle = "#ddd";
    ctx.stroke();
}

// Добавление новой точки при клике
canvas.addEventListener('click', (e) => {
    const x = Math.floor(e.offsetX / cellSize) * cellSize;
    const y = Math.floor(e.offsetY / cellSize) * cellSize;
    points.push({ x, y });
    redraw();
});

// Функция для перерисовки линий по точкам
function redraw() {
    drawGrid();
    if (points.length === 0) return;

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);

    for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.closePath();
    ctx.strokeStyle = "#000";
    ctx.stroke();
}

// Расчет периметра и площади
function calculateAreaPerimeter() {
    if (points.length < 3) {
        alert("Для расчета необходимо минимум 3 точки.");
        return;
    }

    let perimeter = 0;
    let area = 0;

    for (let i = 0; i < points.length; i++) {
        const nextIndex = (i + 1) % points.length;
        const dx = points[nextIndex].x - points[i].x;
        const dy = points[nextIndex].y - points[i].y;
        perimeter += Math.sqrt(dx * dx + dy * dy) / cellSize;

        // Используем формулу площади Гаусса
        area += (points[i].x * points[nextIndex].y - points[nextIndex].x * points[i].y);
    }
    area = Math.abs(area) / 2 / (cellSize * cellSize);

    // Обновляем значения в HTML
    document.getElementById('perimeter').textContent = perimeter.toFixed(2);
    document.getElementById('area').textContent = area.toFixed(2);
}

// Очистка canvas и сброс точек
function clearCanvas() {
    points = [];
    drawGrid();
    document.getElementById('perimeter').textContent = "0";
    document.getElementById('area').textContent = "0";
}

// Инициализация сетки при загрузке страницы
drawGrid();