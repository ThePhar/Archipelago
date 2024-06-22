let game = '';
let presets = {};

window.addEventListener('load', async () => {
     game = document.getElementById('player-options').getAttribute('data-game')

    // Load settings from localStorage, if available.
    loadSettings();

    // Fetch presets, if available.
    try {
        await fetchPresets();
    } catch (error) {
        console.error('Failed to fetch presets.', error);
    }

    // Keep validation of player name.
    document.getElementById('player-name').addEventListener('input', (event) => {
        if (!event.target.value.trim()) {
            event.target.setCustomValidity('You must enter a player name!');
        } else {
            event.target.setCustomValidity('');
        }
    });

    /** @type {NodeListOf<HTMLInputElement>} */
    const ranges = document.querySelectorAll('[data-option-type=range], [data-option-type=named-range]');
    for (const range of ranges) {
        const isNamedRange = range.getAttribute('data-option-type') === 'named-range';
        const option = range.id;

        /** @type {HTMLInputElement} */
        const slider = document.getElementById(`${option}-range`);

        if (isNamedRange) {
            setNamedRange(option, range.value);
            slider.value = range.value;

            range.addEventListener('change', (event) => {
                range.setCustomValidity('');
                slider.value = event.target.value;
                validateNamedRange(option);
            });
            slider.addEventListener('change', (event) => {
                range.setCustomValidity('');
                range.value = event.target.value;
            });

            /** @type {HTMLSelectElement} */
            const select = document.getElementById(`${option}-select`);
            select.addEventListener('change', (event) => {
                range.setCustomValidity('');
                slider.value = event.target.value;
                range.value = event.target.value;
            });
        } else {
            slider.value = range.value;

            range.addEventListener('change', (event) => {
                range.setCustomValidity('');
                slider.value = event.target.value;
            });
            slider.addEventListener('change', (event) => {
                range.setCustomValidity('');
                range.value = event.target.value;
            });
        }
    }

    /** @type {NodeListOf<HTMLInputElement>} */
    const randomButtons = document.querySelectorAll('.randomize-checkbox');
    for (const button of randomButtons) {
        button.addEventListener('change', (event) => {
            setRandomization(event.target.getAttribute('data-option-name'), event.target.checked);
        });

        // Set current status.
        console.log(button);
        console.log(button.getAttribute('data-option-name'))
        setRandomization(button.getAttribute('data-option-name'), button.checked);
    }

    /** @type {NodeListOf<HTMLInputElement>} */
    const customTextChoices = document.querySelectorAll('[data-option-type=text-choice]');
    for (const input of customTextChoices) {
        const option = input.getAttribute('data-option-name');
        /** @type {HTMLSelectElement} */
        const select = document.getElementById(option);
        input.addEventListener('input', (event) => {
            const optionValues = [];
            select.childNodes.forEach((option) => optionValues.push(option.value));
            select.value = optionValues.includes(event.target.value) ? event.target.value : 'custom';
        });
        select.addEventListener('change', () => {
            input.value = '';
        });
    }

    // Update the "Option Preset" select to read "custom" when changes are made to relevant inputs.
    /** @type {HTMLSelectElement} */
    const presetSelect = document.getElementById('game-options-preset');
    document.querySelectorAll('input, select').forEach((input) => {
        if ( // Ignore inputs which have no effect on yaml generation
            (input.id === 'player-name') ||
            (input.id === 'game-options-preset') ||
            (input.classList.contains('group-toggle')) ||
            (input.type === 'submit')
        ) {
            return;
        }
        input.addEventListener('change', () => {
            presetSelect.value = 'custom';
        });
    });

    // Handle changes to presets select
    presetSelect.addEventListener('change', choosePreset);

    // Perform validation and save settings to localStorage when form is submitted.
    document.getElementById('options-form').addEventListener('submit', (event) => {
        /** @type {HTMLInputElement} */
        const playerName = document.getElementById('player-name');
        if (!playerName.checkValidity()) {
            event.preventDefault();
            return;
        }

        /** @type {NodeListOf<HTMLInputElement>} */
        const namedRanges = document.querySelectorAll('[data-option-type=named-range]');
        for (const namedRange of namedRanges) {
            if (!namedRange.checkValidity()) {
                event.preventDefault();
                return;
            }
        }

        saveSettings();
    });
});

/**
 * Saves the user's current player options to localStorage.
 */
const saveSettings = () => {
    const options = {
        inputs: {},
        checkboxes: {},
    };

    /** @type {NodeListOf<HTMLInputElement|HTMLSelectElement>} */
    const inputElements = document.querySelectorAll('input, select');
    for (const input of inputElements) {
        // Ignore submit inputs.
        if (input.type === 'submit') {
            continue;
        }

        if (input.type === 'checkbox' && input.checked) {
            options.checkboxes[input.id] = input.checked;
        } else if (input.type !== 'checkbox') {
            options.inputs[input.id] = input.value;
        }
    }

    localStorage.setItem(game, JSON.stringify(options));
};

/**
 * Loads the user's last known player options from localStorage, if available.
 */
const loadSettings = () => {
    const options = JSON.parse(localStorage.getItem(game));
    if (options) {
        // Clear invalid options from localStorage.
        if (!options.inputs || !options.checkboxes) {
            localStorage.removeItem(game);
            return;
        }

        // Restore value-based inputs and selects.
        for (const key in options.inputs) {
            try {
                document.getElementById(key).value = options.inputs[key];
            } catch {
                console.error(`Unable to load value to input with id: ${key}`);
            }
        }

        // Restore checkboxes.
        for (const option in options.checkboxes) {
            try {
                if (option.startsWith('random-')) {
                    setRandomization(option, true);
                } else {
                    document.getElementById(option).checked = true;
                }
            } catch {
                console.error(`Unable to load value to input with id: ${option}`);
            }
        }
    }
};

/**
 * Fetch the preset data for this game and apply the presets if localStorage indicates one was previously chosen.
 *
 * @returns {Promise<void>}
 */
const fetchPresets = async () => {
    const response = await fetch('option-presets');
    presets = await response.json();
    const presetSelect = document.getElementById('game-options-preset');

    const game = document.getElementById('player-options').getAttribute('data-game');
    const presetToApply = localStorage.getItem(`${game}-preset`);
    const playerName = localStorage.getItem(`${game}-player`);
    if (presetToApply) {
        localStorage.removeItem(`${game}-preset`);
        presetSelect.value = presetToApply;
        applyPreset(presetToApply);
    }

    if (playerName) {
        document.getElementById('player-name').value = playerName;
        localStorage.removeItem(`${game}-player`);
    }
};

/**
 * Clear the localStorage for this game and set a preset to be loaded upon page reload
 * @param event {InputEvent} Event fired from changing the option preset value.
 */
const choosePreset = (event) => {
    // Ignore "custom" presets, as it's set automatically by changing any other inputs.
    if (event.target.value === 'custom') {
        return;
    }

    localStorage.removeItem(game);
    localStorage.setItem(`${game}-player`, document.getElementById('player-name').value);
    if (event.target.value !== 'default') {
        localStorage.setItem(`${game}-preset`, event.target.value);
    }

    document.querySelectorAll('#options-form input, #options-form select').forEach((input) => {
        if (input.id === 'player-name' || input.type === 'submit') {
            return;
        }

        input.removeAttribute('value');
    });

    window.location.replace(window.location.href);
};

/**
 * Apply preset values from a given preset to all values, and set any value not in the preset to their defaults.
 * @param presetName {string}
 */
const applyPreset = (presetName) => {
    // Ignore the "default" preset, because it gets set automatically by Jinja.
    if (presetName === 'default') {
        saveSettings();
        return;
    }

    if (!presets[presetName]) {
        console.error(`Unknown preset ${presetName} chosen.`);
        return;
    }

    const preset = presets[presetName];
    for (const optionName in preset) {
        const optionValue = preset[optionName];

        // Handle list and set options.
        if (Array.isArray(optionValue)) {
            /** @type {NodeListOf<HTMLInputElement>} */
            const checkboxes = document.querySelectorAll(`input[type=checkbox][name=${optionName}]`);
            for (const checkbox of checkboxes) {
                checkbox.checked = optionValue.includes(checkbox.value);
            }

            continue;
        }

        // Handle item dictionaries.
        if (typeof optionValue === 'object' && optionValue !== null) {
            const items = Object.keys(optionValue);
            /** @type {NodeListOf<HTMLInputElement>} */
            const inputs = document.querySelectorAll(`input[type=checkbox][name=${optionName}]`);
            for (const input of inputs) {
                const itemName = input.getAttribute('data-item-name');
                input.value = items.includes(itemName) ? optionValue[itemName] : 0;
            }

            continue;
        }

        /** @type {HTMLInputElement | HTMLSelectElement} */
        const input = document.getElementById(optionName);
        /** @type {HTMLSelectElement | null} */
        const namedRangeInput = document.getElementById(`${optionName}-select`);

        // It is possible for named ranges to use the special name for a value rather than the value itself.
        // This is accounted for here.
        let trueValue = optionValue;
        if (namedRangeInput) {
            for (const option of namedRangeInput.querySelectorAll('option')) {
                if (option === optionValue) {
                    trueValue = optionValue;
                    break;
                }
            }
            namedRangeInput.value = trueValue;
        }

        // Handle options whose presets are "random".
        if (trueValue === 'random') {
            setRandomization(optionName, true);
            continue;
        }

        // Handle normal (text, number, select, etc.) and custom (TextChoice) inputs.
        input.value = trueValue;
        setRandomization(optionName, false);
    }

    saveSettings();
};

/**
 * Displays a message to the user in an alert-style box near the top and scroll to the top of the page to ensure it's
 * viewed. Can be cleared by clicking on the message box.
 * @param text {string} The message to display.
 */
const showUserMessage = (text) => {
    const userMessage = document.getElementById('user-message');
    userMessage.innerText = text;
    userMessage.addEventListener('click', clearUserMessage);
    window.scrollTo(0, 0);
};

/**
 * Clears the inner message, which causes the alert-style box to disappear.
 */
const clearUserMessage = () => {
    const userMessage = document.getElementById('user-message');
    userMessage.removeEventListener('click', clearUserMessage);
    userMessage.innerHTML = '';
};

/**
 * Sets the disabled state of various option inputs depending on the value of the "randomize-checkbox" input.
 * @param option The option to change randomization state for.
 * @param setRandom Whether to disable all inputs depending on the "randomize-checkbox" value. Enables all inputs if
 * `false`.
 */
const setRandomization = (option, setRandom) => {
    /** @type {HTMLInputElement | HTMLSelectElement} */
    const primaryInput = document.getElementById(option);
    /** @type {HTMLInputElement | null} */
    const randomizeInput = document.getElementById(`random-${option}`);
    /** @type {HTMLInputElement | null} */
    const customInput = document.getElementById(`${option}-custom`);
    /** @type {HTMLInputElement | null} */
    const rangeInput = document.getElementById(`${option}-range`);
    /** @type {HTMLSelectElement | null} */
    const namedRangeInput = document.getElementById(`${option}-select`);

    // Don't change anything if the option cannot be randomized (e.g., FreeText, OptionSets, OptionLists, OptionDicts).
    if (!randomizeInput) {
        return
    }

    randomizeInput.checked = setRandom;
    primaryInput.disabled = setRandom;
    if (customInput) {
        customInput.disabled = setRandom;
    }
    if (rangeInput) {
        rangeInput.disabled = setRandom;
    }
    if (namedRangeInput) {
        namedRangeInput.disabled = setRandom;
    }
};

/**
 * Sets the select element associated with the given NamedRange option and sets its value.
 * @param option {string} The name of the NamedRange option.
 * @param value {string} The desired value. If it doesn't exist in the special range names, this select element will
 * display the "Custom" value.
 */
const setNamedRange = (option, value) => {
    // Ignore invalid inputs.
    if (isNaN(parseInt(value))) {
        return;
    }

    /** @type {HTMLSelectElement} */
    const select = document.getElementById(`${option}-select`);
    for (/** @type {HTMLOptionElement} */ const option of select.options) {
        if (option.value === value) {
            select.value = value;
            return;
        }
    }

    // Didn't find the option, set to custom.
    select.value = 'custom';
};

/**
 * Validates if named range is within the min/max or one of the special named values.
 * @param option {string} The name of the option to validate.
 * @return {boolean} Returns `true` if named range value is valid.
 */
const validateNamedRange = (option) => {
    /** @type {HTMLInputElement} */
    const input = document.getElementById(option);
    /** @type {HTMLInputElement} */
    const range = document.getElementById(`${option}-range`);
    /** @type {HTMLSelectElement} */
    const select = document.getElementById(`${option}-select`);

    const value = parseInt(input.value);
    /** @type {number[]} */
    const specialValues = [];
    select.childNodes.forEach((option) => specialValues.push(parseInt(option.value)));

    if (value >= parseInt(range.min) && value <= parseInt(range.max) && Number.isInteger(value)) {
        input.setCustomValidity('');
    } else if (!Number.isInteger(value)) {
        input.setCustomValidity('Only integer values are allowed.');
    } else if (!specialValues.includes(value)) {
        input.setCustomValidity(
            `Only values between ${range.min} and ${range.max}, as well as the defined custom values are allowed.`
        );
    } else {
        input.setCustomValidity('');
    }

    return input.validity.valid;
};
