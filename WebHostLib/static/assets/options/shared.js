/**
 * Creates an event handler for scroll events to lazy load elements and save them to memory.
 * @param element {HTMLElement}
 * @param type {'list' | 'dict'}
 */
function createListObserver(element, type) {
    if (type !== 'list' && type !== 'dict') {
        console.error(`Invalid container type: ${type}`);
        return;
    }

    const option = element.id.substring(0, element.id.indexOf("-container"));
    const observer = new IntersectionObserver((entries) => {
        if (entries[0].intersectionRatio <= 0) {
            return;
        }

        observer.unobserve(document.getElementById(`${option}-eol`));
        if (type === 'list') {
            loadListItems(option, element, 50);
        } else {
            loadDictItems(option, element, 50);
        }

        const eol = document.getElementById(`${option}-eol`);
        if (eol) {
            observer.observe(eol);
        }
    });

    element.innerHTML = `<div id="${option}-eol">&nbsp;</div>`;
    observer.observe(document.getElementById(`${option}-eol`));
}

function loadListItems(option, element, number) {
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

    // End of list target. Don't create if we are at the end of our list.
    if (options[option]["loaded"] < length) {
        html += `<div id="${option}-eol">&nbsp;</div>`;
    }

    element.innerHTML += html;
}

function loadDictItems(option, container, number) {
    /** @type {number} */
    const loaded = options[option]["loaded"];
    /** @type {number} */
    const length = options[option]["valid_keys"].length;

    // All items are already loaded, return.
    if (loaded >= length) {
        return;
    }

    // Remove the "load-more" element.
    if (container.children.length !== 0) {
        container.children[container.children.length - 1].remove();
    }

    const max = Math.min(loaded + 50, length);

    /** @type {string[]} */
    const keys = options[option]["valid_keys"].slice(loaded, max);

    options[option]["loaded"] = max;
    let html = "";
    for (const value of keys) {
        html += `
            <div class="option-entry">                
                <label for="${option}-${value}-qty">${value}</label>
                <input
                    type="number"
                    id="${option}-${value}-qty"
                    name="${option}||${value}||qty"
                    placeholder="0"
                >
            </div>
        `;
    }

    // End of list target. Don't create if we are at the end of our list.
    if (options[option]["loaded"] < length) {
        html += `<div id="${option}-eol">&nbsp;</div>`;
    }

    container.innerHTML += html;
}
