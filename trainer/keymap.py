MACOS_SYMBOLS = {
    "⌘": "Meta",
    "⌥": "Alt",
    "⌃": "Control",
    "⇧": "Shift",
}

MACOS_MAIN_KEYS = {
    "A": "KeyA", "B": "KeyB", "C": "KeyC", "D": "KeyD", "E": "KeyE",
    "F": "KeyF", "G": "KeyG", "H": "KeyH", "I": "KeyI", "J": "KeyJ",
    "K": "KeyK", "L": "KeyL", "M": "KeyM", "N": "KeyN", "O": "KeyO",
    "P": "KeyP", "Q": "KeyQ", "R": "KeyR", "S": "KeyS", "T": "KeyT",
    "U": "KeyU", "V": "KeyV", "W": "KeyW", "X": "KeyX", "Y": "KeyY",
    "Z": "KeyZ",

    "0": "Digit0", "1": "Digit1", "2": "Digit2", "3": "Digit3",
    "4": "Digit4", "5": "Digit5", "6": "Digit6", "7": "Digit7",
    "8": "Digit8", "9": "Digit9",

    "Tab": "Tab",
    "Delete": "Backspace",
    "Пробел": "Space",
    "Esc": "Escape",
    "Return": "Enter",

    "←": "ArrowLeft",
    "→": "ArrowRight",
    "↑": "ArrowUp",
    "↓": "ArrowDown",

    ",": "Comma",
    ".": "Period",
    "/": "Slash",
    "\\": "Backslash",
    "`": "Backquote",
    "-": "Minus",
    "=": "Equal",
    "[": "BracketLeft",
    "]": "BracketRight",
    "{": "BracketLeft",
    "}": "BracketRight",
    "|": "Backslash",
    "+": "Equal",
}


def parse_macos_keys(keys: str) -> dict:
    modifiers = []
    main_key = None

    for part in keys.split():
        part = part.strip()

        if part in MACOS_SYMBOLS:
            modifiers.append(MACOS_SYMBOLS[part])
        elif part in MACOS_MAIN_KEYS:
            main_key = MACOS_MAIN_KEYS[part]

    return {
        'modifiers': sorted(modifiers),
        'main_key': main_key,
    }