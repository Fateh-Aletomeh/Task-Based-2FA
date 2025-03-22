// static/js/script.js
// Global variables
let selectedCircles = [];
let timerInterval;
let remainingTime = 300; // 5 minutes in seconds
let taskData = null;

// DOM elements
const fetchTaskBtn = document.getElementById("fetch-task");
const taskSection = document.getElementById("task-section");
const circleGrid = document.getElementById("circle-grid");
const timerElement = document.getElementById("timer");
const submitTaskBtn = document.getElementById("submit-task");
const refreshTaskBtn = document.getElementById("refresh-task");
const cancelTaskBtn = document.getElementById("cancel-task");
const resultSection = document.getElementById("result-section");
const resultMessage = document.getElementById("result-message");
const tryAgainBtn = document.getElementById("try-again");

// Event listeners
fetchTaskBtn.addEventListener("click", fetchTask);
submitTaskBtn.addEventListener("click", submitTask);
refreshTaskBtn.addEventListener("click", fetchTask);
cancelTaskBtn.addEventListener("click", cancelTask);
tryAgainBtn.addEventListener("click", resetUI);

// Functions
function fetchTask() {
    // Fetch task data from the server
    fetch('/get-task-data')
        .then(response => response.json())
        .then(data => {
            taskData = data;
            displayTask(data);
            startTimer();
            fetchTaskBtn.classList.add("hidden");
            taskSection.classList.remove("hidden");
            resultSection.classList.add("hidden");
        })
        .catch(error => {
            console.error('Error fetching task:', error);
            alert('Error fetching task data. Please try again.');
        });
}

function displayTask(data) {
    // Clear previous circles and selections
    circleGrid.innerHTML = '';
    selectedCircles = [];
    
    // Create circles based on the task data
    data.circles.forEach(circle => {
        const circleElement = document.createElement("div");
        circleElement.classList.add("circle", `circle-${circle.color}`);
        circleElement.dataset.id = circle.id;
        
        // Add circle number
        const circleNumber = circle.id.split('-')[1];
        circleElement.textContent = circleNumber;
        
        // Add click event to select/deselect circles
        circleElement.addEventListener("click", function() {
            this.classList.toggle("selected");
            
            const circleId = this.dataset.id;
            if (this.classList.contains("selected")) {
                if (!selectedCircles.includes(circleId)) {
                    selectedCircles.push(circleId);
                }
            } else {
                selectedCircles = selectedCircles.filter(id => id !== circleId);
            }
        });
        
        circleGrid.appendChild(circleElement);
    });
    
    // Add empty cells to complete the 4x4 grid if needed
    const remainingCells = 16 - data.circles.length;
    for (let i = 0; i < remainingCells; i++) {
        const emptyCell = document.createElement("div");
        circleGrid.appendChild(emptyCell);
    }
}

function startTimer() {
    // Reset and start the timer
    clearInterval(timerInterval);
    remainingTime = 300; // 5 minutes
    updateTimerDisplay();
    
    timerInterval = setInterval(function() {
        remainingTime--;
        updateTimerDisplay();
        
        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            showResult(false, "Time expired");
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    timerElement.textContent = `Time remaining: ${minutes}:${seconds.toString().padStart(2, '0')}`;
}

function submitTask() {
    clearInterval(timerInterval);
    
    // Send selected circles to server for verification
    fetch('/verify-task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            selectedCircles: selectedCircles
        })
    })
    .then(response => response.json())
    .then(data => {
        showResult(data.success, data.message);
    })
    .catch(error => {
        console.error('Error submitting task:', error);
        showResult(false, "Error submitting task. Please try again.");
    });
}

function showResult(isSuccess, message) {
    taskSection.classList.add("hidden");
    resultSection.classList.remove("hidden");
    resultMessage.textContent = message;
    resultMessage.style.color = isSuccess ? "#4CAF50" : "#F44336";
}

function cancelTask() {
    clearInterval(timerInterval);
    resetUI();
}

function resetUI() {
    fetchTaskBtn.classList.remove("hidden");
    taskSection.classList.add("hidden");
    resultSection.classList.add("hidden");
    circleGrid.innerHTML = '';
    selectedCircles = [];
}