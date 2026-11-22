const items = JSON.parse(document.getElementById('training-data').textContent);

const actionElement = document.getElementById("action");
const optionsElement = document.getElementById("options");
const feedbackElement = document.getElementById("feedback");
const nextButton = document.getElementById("next-button");
const resultCard = document.getElementById("result-card");
const questionCard = document.querySelector(".question-card");
const currentElement = document.getElementById("current");
const totalElement = document.getElementById("total");
const resultText = document.getElementById("result-text");

let currentIndex = 0;
let correctCount = 0;
let answered = false;

totalElement.textContent = items.length;

function shuffle(array) {
    return [...array].sort(() => Math.random() - 0.5);
}

function renderQuestion() {
    answered = false;
    feedbackElement.textContent = "";
    feedbackElement.className = "feedback";
    nextButton.classList.add("hidden");
    optionsElement.innerHTML = "";

    const item = items[currentIndex];
    currentElement.textContent = currentIndex + 1;
    actionElement.textContent = item.action;

    const options = shuffle([
        item.keys,
        ...items
            .filter(other => other.id !== item.id)
            .slice(0, 3)
            .map(other => other.keys),
    ]);

    options.forEach(option => {
        const button = document.createElement("button");
        button.className = "option";
        button.textContent = option;
        button.addEventListener("click", () => selectAnswer(button, option, item));
        optionsElement.appendChild(button);
    });
}

async function selectAnswer(button, selected, item) {
    if (answered) return;
    answered = true;

    const isCorrect = selected === item.keys;

    if (isCorrect) {
        correctCount += 1;
        button.classList.add("correct");
        feedbackElement.textContent = "Верно!";
        feedbackElement.classList.add("success");
    } else {
        button.classList.add("wrong");
        feedbackElement.textContent = `Правильный ответ: ${item.keys}`;
        feedbackElement.classList.add("error");

        [...optionsElement.children].forEach(optionButton => {
            if (optionButton.textContent === item.keys) {
                optionButton.classList.add("correct");
            }
        });
    }

    await fetch(checkUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            hotkey_id: item.id,
            selected: selected,
        }),
    });

    nextButton.classList.remove("hidden");
}

nextButton.addEventListener("click", () => {
    currentIndex += 1;

    if (currentIndex < items.length) {
        renderQuestion();
    } else {
        questionCard.classList.add("hidden");
        resultCard.classList.remove("hidden");

        const percent = Math.round(correctCount / items.length * 100);
        resultText.textContent =
            `Правильно: ${correctCount} из ${items.length} (${percent}%)`;
    }
});

function getCookie(name) {
    const match = document.cookie
        .split("; ")
        .find(cookie => cookie.startsWith(`${name}=`));

    return match ? decodeURIComponent(match.split("=")[1]) : null;
}

renderQuestion();