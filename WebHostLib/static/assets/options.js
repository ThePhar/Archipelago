const game = document.getElementById("options-game").innerHTML;
const options = document.getElementById("options");

for (const option of options.querySelectorAll(".option-container")) {
    const type = option.getAttribute("data-type");
    const default_ = option.getAttribute("data-default");
    const randomElement = option.querySelector(".option-random input");

    if (randomElement) {
        linkRandomButton(randomElement);
    }

    switch (type) {
        case "choice": {

        }
    }
}

/**
 * Adds an event listener to the random button to toggle the `disabled` property for all linked inputs when toggled.
 * @param randomElement {HTMLInputElement}
 */
function linkRandomButton(randomElement) {
    /**
     * @param {HTMLInputElement | HTMLSelectElement} element
     * @param {Event & {target: HTMLInputElement}} event
     */
    const toggleDisabled = (element, event) => {
        element.disabled = event.target.checked;
    };

    for (const id of randomElement.getAttribute("data-linked").split(" ")) {
        console.log(id);
        const element = document.getElementById(id)
        randomElement.addEventListener("change", toggleDisabled.bind(null, element));

        // Set initial value.
        element.disabled = randomElement.checked;
    }
}
