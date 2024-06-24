/**
 * Creates an event handler for scroll events to lazy load list elements and save them to memory.
 * @param element {HTMLElement}
 */
function createListObserver(element) {
    const option = element.id.substring(0, element.id.indexOf("-container"));
    const observer = new IntersectionObserver((entries) => {
        console.log("Called observer", option)
        if (entries[0].intersectionRatio <= 0) {
            return;
        }

        observer.unobserve(document.getElementById(`${option}-eol`));
        loadItems(option, element, 50);

        const eol = document.getElementById(`${option}-eol`);
        if (eol) {
            observer.observe(eol);
        }
    });

    const eol = document.getElementById(`${option}-eol`);
    if (eol) {
        observer.observe(eol);
    }
}

function loadItems(option, element, number) {
    console.log(option, number, element);
    /** @type {number} */
    const loaded = options[option]["loaded"];
    /** @type {number} */
    const length = options[option]["valid_keys"].length;

    // All items are already loaded, return.
    if (loaded >= length) {
        return;
    }

    // Remove the "load-more" element.
    if (element.children.length !== 0) {
        element.children[element.children.length - 1].remove();
    }

    const max = Math.min(loaded + 50, length);

    /** @type {string[]} */
    const keys = options[option]["valid_keys"].slice(loaded, max);

    options[option]["loaded"] = max;
    // TODO: If you see this in version control for the PR, reject it and dunk on me to do this properly. I only used
    // this for testing and I better not have left it in. -Phar
    let html = "";
    for (const value of keys) {
        html += `
            <div class="option-entry">
                <input
                    type="checkbox"
                    id="${option}-${value}"
                    name="${option}"
                    value="${value}"
                    ${options[option]["default"].includes(value) ? "checked" : ""}
                >
                <label for="${option}-${value}">${value}</label>
            </div>
        `;
    }

    if (options[option]["loaded"] < length) {
        html += `<div id="${option}-eol">Loading...</div>`;
    }

    element.innerHTML += html;
    console.log(`Loaded: ${options[option]["loaded"]}`, `Children: ${element.children.length}`);
}
