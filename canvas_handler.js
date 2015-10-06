var images = [];
var canvas = document.getElementById('screenshotCanvas');
var context = canvas.getContext('2d');
var image_id = 0;
var interval;
function init()
{
    images[0] = new Image();
    images[1] = new Image();
    images[2] = new Image();
    images[3] = new Image();
    images[0].src = 'screenshots/screenshot1.png';
    images[1].src = 'screenshots/screenshot2.png';
    images[2].src = 'screenshots/screenshot3.png';
    images[3].src = 'screenshots/screenshot4.png';
    draw();
    interval = window.setInterval(draw, 4000);
    canvas.addEventListener('click', canvasClicked);
}

function draw()
{
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(images[(image_id++) % images.length], 0, 0);
}

function canvasClicked(event)
{
    clearInterval(interval);
    draw();
    interval = window.setInterval(draw, 4000);
}

init();