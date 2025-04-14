window.addEventListener("load", () => {
    const optionsElement = document.querySelector("#options");
    const game = optionsElement.getAttribute("data-game");

    // Remove all "Random" options from all select boxes as it's only there for non-JS users.
    for (const element of optionsElement.querySelectorAll("select")) {
        /** @type {HTMLOptionElement} */
        const option = element.querySelector("[data-random]");
        if (!option) {
            continue;
        }

        option.hidden = true;
    }

    for (const option of optionsElement.querySelectorAll(".option-container")) {
        initializeOptionEvents(option);
    }

    /**
     * @param option {HTMLDivElement}
     */
    function initializeOptionEvents(option) {
        const type = option.getAttribute("data-type");
        switch (type) {
            case "choice": {
                /** @type {HTMLInputElement} */
                const randomElement = option.querySelector(".randomize-checkbox input");
                const selectElement = option.querySelector("select");

                selectElement.disabled = randomElement.checked;
                if (selectElement.disabled) {
                    selectElement.value = "random";
                } else {
                    selectElement.value = selectElement.getAttribute("data-default");
                }

                randomElement.addEventListener("change", (e) => {
                    selectElement.disabled = e.target["checked"];
                    if (selectElement.disabled) {
                        selectElement.value = "random";
                    } else {
                        selectElement.value = selectElement.getAttribute("data-default");
                    }
                });
            }
        }
    }
})
