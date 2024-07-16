function showNextQuestion() {
    const currentQuestion = document.getElementById('question-' + currentQuestionIndex);
    currentQuestion.classList.remove('active');
    currentQuestionIndex++;

    if (currentQuestionIndex <= totalQuestions) {
        const nextQuestion = document.getElementById('question-' + currentQuestionIndex);
        nextQuestion.classList.add('active');
        document.getElementById('prev-btn').style.display = 'block';
    }

    if (currentQuestionIndex === totalQuestions) {
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'block';
    }
}

function showPreviousQuestion() {
    const currentQuestion = document.getElementById('question-' + currentQuestionIndex);
    currentQuestion.classList.remove('active');
    currentQuestionIndex--;

    if (currentQuestionIndex > 0) {
        const prevQuestion = document.getElementById('question-' + currentQuestionIndex);
        prevQuestion.classList.add('active');
        document.getElementById('next-btn').style.display = 'block';
        document.getElementById('submit-btn').style.display = 'none';
    }

    if (currentQuestionIndex === 1) {
        document.getElementById('prev-btn').style.display = 'none';
    }
}

// Show the first question initially
document.getElementById('question-' + currentQuestionIndex).classList.add('active');

// Countdown timer
function updateTimer() {
    const currentTime = Date.now();
    const elapsedTime = currentTime - examStartTime;
    const remainingTime = examDuration - elapsedTime;
    const minutes = Math.floor((remainingTime / 1000) / 60);
    const seconds = Math.floor((remainingTime / 1000) % 60);
    const timerElement = document.querySelector('.progress-text');
    timerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

    if (remainingTime <= 0) {
        timerElement.textContent = '0:00';
        submitExam(); // Submit exam when time limit is reached
    } else {
        setTimeout(updateTimer, 1000); // Update every second
    }
}

// Start the countdown timer
updateTimer();

// Function to submit the exam
function submitExam() {
    document.getElementById('exam-form').submit();
}
