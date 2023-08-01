// JavaScript to show each letter one by one and the full word
const textContainer = document.getElementById('text-container');
const letters = textContainer.getElementsByTagName('span');
const totalLetters = letters.length;
let currentIndex = 0;

function showNextLetter() {
    letters[currentIndex].classList.remove('hidden');
    currentIndex = (currentIndex + 1) % totalLetters;
    if (currentIndex === 0) {
        setTimeout(hideAllLetters, 1000);
    } else {
        setTimeout(showNextLetter, 1000);
    }
}

function hideAllLetters() {
    for (let i = 0; i < totalLetters; i++) {
        letters[i].classList.add('hidden');
    }
    setTimeout(showNextLetter, 1000);
}

showNextLetter(); // Start the sequence
