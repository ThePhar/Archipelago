const game = document.getElementById("options-game").innerHTML;
const options = document.getElementById("options");

for (const option of options.querySelectorAll(".option-container")) {
    const type = option.getAttribute("data-type");
    if (!type) {
        // Ignore "meta" options.
        continue;
    }

    const default_ = option.getAttribute("data-default");
    const randomElement = option.querySelector(".option-random input");

    if (randomElement) {
        linkRandomButton(randomElement, type);
    }

    if (type.includes("range")) {
        linkRangeSlider(option);
    } else if (type === "text_choice") {
        linkTextChoice(option);
    }
}

/**
 * Adds an event listener to the random button to toggle the `disabled` property for all linked inputs when toggled.
 * @param randomElement {HTMLInputElement}
 * @param type {string}
 */
function linkRandomButton(randomElement, type) {
    /**
     * @param {HTMLInputElement | HTMLSelectElement} element
     * @param {Event & {target: HTMLInputElement}} event
     */
    const toggleDisabled = (element, event) => {
        // Special handling for text choice...
        if (type === "text_choice" && !event.target.checked && element.hasAttribute("data-linked")) {
            /** @type {HTMLSelectElement} */
            const valueInput = document.getElementById(element.getAttribute("data-linked"));
            if (!!valueInput.value) {
                return;
            }
        }

        element.disabled = event.target.checked;
    };

    for (const id of randomElement.getAttribute("data-linked").split(" ")) {
        const element = document.getElementById(id)
        randomElement.addEventListener("change", toggleDisabled.bind(null, element));

        element.disabled = randomElement.checked;
    }
}

/**
 * Adds an event listener between the range and value input boxes to link interactivity. If a preset box is also
 * present, will link that as well.
 * @param option {HTMLElement}
 */
function linkRangeSlider(option) {
    /** @type {HTMLInputElement} */
    const valueInput = document.getElementById(`${option.id}-value`);
    /** @type {HTMLInputElement} */
    const rangeInput = document.getElementById(`${valueInput.id}-range`);
    /** @type {HTMLSelectElement | null} */
    const presetSelect = document.getElementById(`${valueInput.id}-preset`);


    /** @param event {Event & {target: HTMLInputElement}} */
    const updateValue = (event) => {
        valueInput.value = event.target.value;
        rangeInput.value = event.target.value;

        if (presetSelect) {
            updatePreset(presetSelect, event.target.value);
        }
    };

    /**
     * @param element {HTMLInputElement | HTMLSelectElement}
     * @param value {string | number}
     */
    const updatePreset = (element, value) => {
        const presetOption = element.querySelector(`option[value="${value}"]`);
        if (presetOption) {
            element.value = value;
            return;
        }

        // Changes to '-- Custom --' hidden field.
        element.value = "";
    }

    valueInput.addEventListener("input", updateValue);
    rangeInput.addEventListener("input", updateValue);
    if (presetSelect) {
        presetSelect.addEventListener("change", updateValue);
        updatePreset(presetSelect, valueInput.value);
    }

    rangeInput.value = valueInput.value;
}

/**
 * Adds an event listener between the range and value input boxes to link interactivity.
 * @param option {HTMLElement}
 */
function linkTextChoice(option) {
    /** @type {HTMLSelectElement} */
    const valueInput = document.getElementById(`${option.id}-value`);
    /** @type {HTMLInputElement} */
    const customInput = document.getElementById(`${option.id}-custom_value`);

    /**
     * @param event {Event & {target: HTMLInputElement}}
     */
    const setCustomDisabled = (event) => {
        customInput.disabled = !!(event.target.value);
    };

    valueInput.addEventListener("change", setCustomDisabled);
    customInput.disabled = !!(valueInput.value);
}
