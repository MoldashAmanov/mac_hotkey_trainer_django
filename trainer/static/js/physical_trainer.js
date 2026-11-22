const items = JSON.parse(document.getElementById('physical-training-data').textContent);

const actionElement = document.getElementById("action");
const pressedKeysElement = document.getElementById("pressed-keys");
const feedbackElement = document.getElementById("feedback");
const correctCountElement = document.getElementById("correct-count");
const wrongCountElement = document.getElementById("wrong-count");
const remainingElement = document.getElementById("remaining");
const skipButton = document.getElementById("skip-button");

const MODIFIERS = new Set([
    "Meta", "Alt", "Control", "Shift",
    "MetaLeft", "MetaRight", "AltLeft", "AltRight",
    "ControlLeft", "ControlRight", "ShiftLeft", "ShiftRight",
]);

const DISPLAY = {
    Meta: "⌘",
    Alt: "⌥",
    Control: "⌃",
    Shift: "⇧",
};

let currentIndex = 0;
let correctCount = 0;
let wrongCount = 0;
let isChecking = false;

function getModifiers(event) {
    const modifiers = [];

    if (event.metaKey) modifiers.push("Meta");
    if (event.altKey) modifiers.push("Alt");
    if (event.ctrlKey) modifiers.push("Control");
    if (event.shiftKey) modifiers.push("Shift");

    return modifiers.sort();
}

function getMainKey(event) {
    return event.code && !MODIFIERS.has(event.code) ? event.code : null;
}

function isSame(expected, actual) {
    return (
        expected.main_key === actual.main_key &&
        expected.modifiers.length === actual.modifiers.length &&
        expected.modifiers.every((m, i) => m === actual.modifiers[i])
    );
}

function formatKeys(item) {
    const modifiers = item.modifiers.map(m => DISPLAY[m]).join(" ");
    const main = item.keys
        .split(" ")
        .filter(part => !["⌘", "⌥", "⌃", "⇧"].includes(part))
        .join(" ");

    return modifiers ? `${modifiers} ${main}` : main;
}

function renderQuestion() {
    const item = items[currentIndex];

    if (!item) {
        actionElement.textContent = "Тренировка завершена!";
        pressedKeysElement.textContent =
            `Верно: ${correctCount}, ошибок: ${wrongCount}`;
        return;
    }

    actionElement.textContent = item.action;
    pressedKeysElement.textContent = "Нажмите сочетание на клавиатуре Mac…";
    feedbackElement.textContent = "";
    feedbackElement.className = "feedback";
    remainingElement.textContent = items.length - currentIndex;
    isChecking = false;
}

async function checkAnswer(item, actual) {
    if (isChecking) return;
    isChecking = true;

    const isCorrect = isSame(item, actual);

    if (isCorrect) {
        correctCount += 1;
        feedbackElement.textContent = "Верно!";
        feedbackElement.classList.add("success");
    } else {
        wrongCount += 1;
        feedbackElement.textContent = `Правильно: ${formatKeys(item)}`;
        feedbackElement.classList.add("error");
    }

    correctCountElement.textContent = correctCount;
    wrongCountElement.textContent = wrongCount;

    await fetch(checkUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            hotkey_id: item.id,
            selected: item.keys,
        }),
    });

    setTimeout(() => {
        currentIndex += 1;
        renderQuestion();
    }, 800);
}

document.addEventListener("keydown", event => {
    const item = items[currentIndex];

    if (!item) return;

    const mainKey = getMainKey(event);

    if (
        (event.metaKey && ["KeyW", "KeyQ", "KeyT", "KeyN", "KeyR"].includes(event.code)) ||
        (event.metaKey && event.shiftKey && ["KeyQ", "KeyT", "KeyR"].includes(event.code))
    ) {
        return;
    }

    if (
        ["Space", "Tab", "Backspace", "ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"]
            .includes(event.code)
    ) {
        event.preventDefault();
    }

    if (!mainKey) {
        pressedKeysElement.textContent =
            getModifiers(event).map(m => DISPLAY[m]).join(" ") || "…";
        return;
    }

    checkAnswer(item, {
        modifiers: getModifiers(event),
        main_key: mainKey,
    });
});

skipButton.addEventListener("click", () => {
    if (!items[currentIndex]) return;

    wrongCount += 1;
    wrongCountElement.textContent = wrongCount;
    currentIndex += 1;
    renderQuestion();
});

function getCookie(name) {
    const match = document.cookie
        .split("; ")
        .find(cookie => cookie.startsWith(`${name}=`));

    return match ? decodeURIComponent(match.split("=")[1]) : null;
}

renderQuestion();